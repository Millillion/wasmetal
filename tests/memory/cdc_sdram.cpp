// SPDX-License-Identifier: MIT
// Independent clocks, pin-level SDRAM model and byte oracle. Reset locations
// come from public handshakes and observed device commands/beats, never DUT state.
#include "Vwasmetal_cdc_sdram.h"
#include "sdram_device.hpp"
#include <memory>
#include <numeric>
#include <vector>

struct Pending {Request request;bool activated=false,retired=false;};
class CrossingTest {
public:
    VerilatedContext context;
    Vwasmetal_cdc_sdram dut{&context};
    Request pin_request;
    Sdram memory;
    std::vector<Pending> requests;
    std::unordered_map<uint32_t,uint8_t> oracle;
    unsigned source_half,memory_half,phase;
    uint64_t now=0,source_time=0,pause_source=0,serial=0;
    uint64_t source_edges=0,memory_edges=0,coincident=0;
    uint64_t completed=0,resets=0,cancelled=0,reset_refreshes=0;
    uint64_t observation=1469598103934665603ULL,stimulus=1469598103934665603ULL;
    unsigned coverage[2][15][3]{};
    size_t current=0,physical=0;
    bool active=false,returned=false,backend_completed=false,physical_valid=false,accounted=false;

    CrossingTest(unsigned s,unsigned m,unsigned p,const std::string& mutation):
        memory(pin_request,mutation),source_half(s),memory_half(m),phase(p) {
        dut.s_clk=0;dut.m_clk=0;dut.reset=1;dut.cold_reset=1;
        dut.s_valid=0;dut.s_write=0;dut.s_address=0;dut.s_mask=0;dut.sdram_dq_in=memory.drive;
        for(unsigned n=0;n<4;++n)dut.s_wdata[n]=0;
        idle(10*(s+m));dut.cold_reset=0;dut.reset=0;
        wait([&] {return bool(dut.available);},2*(s+m)*(TEST_POWERUP+TEST_REFRESH+1000));
        require(memory.mode && memory.initial_refreshes==2,"CDC SDRAM initialization incomplete");
    }
    void mix(uint64_t value) {observation^=value;observation*=1099511628211ULL;}
    uint8_t expected(uint32_t address) const {
        auto found=oracle.find(address);return found==oracle.end() ? initial_byte(address) : found->second;
    }
    void account_write() {
        require(physical_valid,"physical write has no source request");
        for(unsigned n=0;n<16;++n)if(pin_request.mask&(1u<<n))
            oracle[pin_request.address+n]=pin_request.data[n];
        for(unsigned n=0;n<16;++n) {
            uint32_t address=pin_request.address+n;
            require(uint8_t(memory.load(address/2)>>(8*(address%2)))==expected(address),
                "CDC SDRAM bytes differ from independent byte oracle");
        }
        accounted=true;
    }
    void step() {
        dut.sdram_dq_in=memory.drive;dut.eval();
        bool next_s=dut.s_clk;
        if(pause_source) --pause_source;
        else {next_s=((source_time/source_half)&1)!=0;++source_time;}
        const bool next_m=(((now+phase)/memory_half)&1)!=0;
        const bool s_rise=next_s && !dut.s_clk,m_rise=next_m && !dut.m_clk;
        coincident+=s_rise && m_rise;source_edges+=s_rise;memory_edges+=m_rise;
        require(!(dut.m_reset && dut.m_ready),"SDRAM response escaped destination reset");
        require(!(dut.s_reset && dut.s_ready),"CDC response escaped source reset");
        if(m_rise) {
            Pins pins(dut);
            if(pins.command()==3) {
                size_t found=requests.size();
                for(size_t i=0;i<requests.size();++i) {
                    const auto& q=requests[i];
                    if(q.retired || q.activated || !q.request.legal)continue;
                    if(pins.bank==(q.request.address/(2u<<TEST_COLUMNS))%4 &&
                        pins.address==q.request.address/(8u<<TEST_COLUMNS)) {
                        require(found==requests.size(),"ambiguous test address for physical request");found=i;
                    }
                }
                require(found<requests.size(),"SDRAM activate has no issued request");
                require(!physical_valid || (memory.closed() && !memory.read_running && !memory.write_running),
                    "new request overtook an unfinished burst");
                physical=found;physical_valid=true;pin_request=requests[found].request;
                requests[found].activated=true;accounted=false;
            }
            const uint64_t refresh_before=memory.refreshes;
            memory.step(pins);
            if(dut.m_reset) reset_refreshes+=memory.refreshes-refresh_before;
            if(physical_valid && pin_request.saw_write && !memory.write_running && !accounted)account_write();
            if(dut.m_valid && dut.m_ready) {
                require(active && !backend_completed,"stale destination response after reset");
                backend_completed=true;
            }
            mix(pins.command()|(uint64_t(pins.address)<<3)|(uint64_t(pins.bank)<<16)|
                (uint64_t(pins.dqm)<<18)|(uint64_t(pins.oe)<<20)|(uint64_t(dut.m_reset)<<21));
            if(pins.oe)mix(pins.data);
        }
        if(s_rise && dut.s_ready) {
            require(active && !returned && backend_completed,"stale or duplicate CDC completion");
            const auto& q=requests[current].request;
            require(bool(dut.s_fault)!=q.legal,"CDC SDRAM fault differs from request oracle");
            if(q.legal)require(requests[current].activated && physical==current && memory.closed() &&
                !memory.read_running && !memory.write_running,"source completed before its physical operation");
            for(unsigned n=0;n<16;++n) {
                uint8_t want=q.legal && !q.write ? expected(q.address+n) : 0;
                uint8_t actual=uint8_t(dut.s_rdata[n/4]>>(8*(n%4)));
                require(actual==want,"CDC SDRAM read differs from independent byte oracle");mix(actual);
            }
            returned=true;++completed;
        }
        dut.s_clk=next_s;dut.m_clk=next_m;dut.eval();
        // SDRAM changes DQ after its edge; the controller samples the previous
        // value at that edge. This is also true for simultaneous source edges.
        dut.sdram_dq_in=memory.drive;dut.eval();context.time(++now);
    }
    void idle(uint64_t ticks) {for(uint64_t n=0;n<ticks;++n)step();}
    template<class Predicate> void wait(Predicate predicate,uint64_t limit=0) {
        if(!limit)limit=2*(source_half+memory_half)*(3*TEST_REFRESH+2000);
        for(uint64_t n=0;!predicate();++n) {require(n<limit,"CDC SDRAM test timed out");step();}
    }
    uint32_t address() {
        ++serial;
        return uint32_t((serial%(TEST_BYTES/(8u<<TEST_COLUMNS)))*(8u<<TEST_COLUMNS)+
            (serial%4)*(2u<<TEST_COLUMNS)+((serial*7)%((1u<<TEST_COLUMNS)/8))*16);
    }
    void start(bool write,uint32_t address,uint16_t mask) {
        require(!active,"overlapping source requests in test");
        Word data=random_word();
        Request q{true,write,address%16==0 && mask!=0 && uint64_t(address)+16<=TEST_BYTES,
            false,address,mask,data};
        current=requests.size();requests.push_back({q,false,false});
        active=true;returned=false;backend_completed=false;
        dut.s_valid=1;dut.s_write=write;dut.s_address=address;dut.s_mask=mask;
        for(unsigned n=0;n<4;++n) {
            uint32_t packed=0;for(unsigned b=0;b<4;++b)packed|=uint32_t(data[4*n+b])<<(8*b);
            dut.s_wdata[n]=packed;
        }
        for(uint64_t value:{uint64_t(write),uint64_t(address),uint64_t(mask)}) {
            stimulus^=value;stimulus*=1099511628211ULL;
        }
        for(uint8_t value:data) {stimulus^=value;stimulus*=1099511628211ULL;}
    }
    void finish() {
        wait([&] {return returned;});
        idle(8*source_half); // A held request must not be executed a second time.
        dut.s_valid=0;idle(8*(source_half+memory_half));active=false;
        for(auto& q:requests)q.retired=true;
    }
    void transfer(bool write,uint32_t address,uint16_t mask) {start(write,address,mask);finish();}
    void interrupt(bool write,unsigned stage,unsigned style) {
        const uint32_t target=address();
        const uint64_t activations=memory.activations,commands=memory.reads+memory.writes;
        const uint64_t beats=write ? memory.write_beats : memory.read_beats;
        start(write,target,uint16_t(random_value()|1));
        wait([&] {
            switch(stage) {
                case 0:return bool(dut.m_valid) && memory.activations==activations;
                case 1:return memory.activations>activations;
                case 2:return memory.reads+memory.writes>commands;
                case 11:return memory.activations>activations && memory.closed();
                case 12:return bool(dut.m_ready);
                case 13:return backend_completed;
                case 14:return returned;
                default:return (write ? memory.write_beats : memory.read_beats)-beats==stage-2;
            }
        });
        ++coverage[unsigned(write)][stage][style];
        // At this first destination-valid transition the SDR controller has
        // not yet sampled the request. Reset must prevent its later activation.
        // Other phases have already accepted a physical operation, which drains.
        if(stage==0)requests[current].retired=true;
        cancelled+=!returned;active=false;dut.s_valid=0;dut.reset=1;step();
        require(dut.s_reset && dut.m_reset && !dut.s_ready && !dut.m_valid,
            "common reset did not cancel both interfaces asynchronously");
        if(style==1) {
            const uint64_t previous=memory.refreshes;
            idle(2*memory_half*(2*TEST_REFRESH+100));
            require(memory.refreshes>previous,"refresh did not continue during long warm reset");
        }
        dut.reset=0;
        if(style==2)pause_source=2*memory_half*(2*TEST_REFRESH+100);
        ++resets;
        // Offer a new request immediately, before reset release or old burst
        // draining. Its different address distinguishes any stale read response.
        transfer(false,address(),0xffff);
        require(dut.initialized && memory.initial_refreshes==2,"warm reset restarted SDRAM initialization");
        transfer(false,target,0xffff); // Accepted masked writes must have finished.
    }
    void run() {
        transfer(false,0,0xffff);
        transfer(true,TEST_BYTES-16,0xa55a);transfer(false,TEST_BYTES-16,0xffff);
        for(unsigned stage=0;stage<15;++stage)for(bool write:{false,true})for(unsigned style=0;style<3;++style)
            interrupt(write,stage,style);
        for(unsigned n=0;n<64;++n) {
            const uint32_t target=address();
            transfer(true,target,uint16_t(random_value()|1));transfer(false,target,0xffff);
        }
        for(unsigned byte=1;byte<16;++byte)transfer(true,byte,0xffff);
        transfer(false,0,0);transfer(true,0,0);transfer(false,TEST_BYTES,0xffff);
        transfer(true,0xfffffff0u,0xffff);
        require(reset_refreshes>0,"no refresh observed during destination reset");
        for(const auto& direction:coverage)for(const auto& stage:direction)for(unsigned count:stage)
            require(count==1,"reset phase coverage is incomplete");
        require(source_edges==(source_time+source_half-1)/(2*source_half) &&
            memory_edges==(now+phase+memory_half-1)/(2*memory_half),
            "clock edge counts differ from independent elapsed-time calculation");
        const uint64_t period=std::lcm(2*source_half,2*memory_half);
        uint64_t first=period;
        for(uint64_t tick=source_half;tick<period;tick+=2*source_half)
            if((tick+phase)%(2*memory_half)==memory_half) {first=tick;break;}
        // Source pauses last an integral number of memory periods, preserving
        // this phase relation when the source resumes.
        const uint64_t expected_coincident=first==period || source_time<=first ? 0 :
            1+(source_time-1-first)/period;
        require(coincident==expected_coincident,"simultaneous clock edges were missed or duplicated");
        dut.final();
    }
    void json() const {
        std::cout<<"{\"source_half_period\":"<<source_half<<",\"memory_half_period\":"<<memory_half
            <<",\"memory_phase\":"<<phase<<",\"completed\":"<<completed<<",\"warm_resets\":"<<resets
            <<",\"cancelled_requests\":"<<cancelled<<",\"source_rising_edges\":"<<source_edges
            <<",\"memory_rising_edges\":"<<memory_edges<<",\"simultaneous_rising_edges\":"<<coincident
            <<",\"refreshes_during_reset\":"<<reset_refreshes<<",\"read_bursts\":"<<memory.reads
            <<",\"write_bursts\":"<<memory.writes<<",\"largest_refresh_gap\":"<<memory.refresh_max_gap
            <<",\"elapsed_ticks\":"<<now<<",\"stimulus_hash\":"<<stimulus
            <<",\"observation_hash\":"<<observation<<",\"coverage\":[";
        for(unsigned w=0;w<2;++w) {
            if(w)std::cout<<',';
            std::cout<<'[';
            for(unsigned stage=0;stage<15;++stage) {
                if(stage)std::cout<<',';
                std::cout<<'[';
                for(unsigned style=0;style<3;++style) {if(style)std::cout<<',';std::cout<<coverage[w][stage][style];}
                std::cout<<']';
            }
            std::cout<<']';
        }
        std::cout<<"]}";
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        const unsigned configurations[][3]={{2,3,0},{3,2,1},{5,7,3},{4,4,2},{32,1,0},{1,32,17},{1,1,0}};
        std::cout<<"{\"status\":\"passed\",\"configurations\":[";
        for(unsigned i=0;i<7;++i) {
            const auto& c=configurations[i];
            auto t=std::make_unique<CrossingTest>(c[0],c[1],c[2],argc>1 ? argv[1] : "");
            t->run();if(i)std::cout<<',';t->json();
        }
        std::cout<<"]}\n";return 0;
    } catch(const std::exception& error) {std::cerr<<error.what()<<'\n';return 1;}
}
