#include "Vwasmetal_memory_bist.h"
#include "verilated.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#ifndef TEST_BYTES
#define TEST_BYTES 80
#endif
#ifndef TEST_TIMEOUT
#define TEST_TIMEOUT 32
#endif
using Word=std::array<uint32_t,4>;
constexpr unsigned words=TEST_BYTES/16;
struct Operation {unsigned address;bool write;Word data;};
struct Defect {enum Kind {None,Stuck0,Stuck1,Rise,Fall,And,Or,Alias,ReadXor,DropByte,Bus,BusRead,BusAndData,
    InvertRise,InvertFall,Force0Rise,Force1Rise,Force0Fall,Force1Fall} kind=None;
    unsigned word=0,bit=0,second=1;};
struct Error {unsigned code=0,address=0;Word expected{},observed{};};
struct Totals {uint64_t cycles=0,campaigns=0,requests=0,reads=0,writes=0,resets=0,
    detected=0,timeouts=0,held_start_cycles=0,trace=1469598103934665603ULL;} totals;
std::string context;
void require(bool value,const std::string& message) {
    if(!value)throw std::runtime_error("BIST "+context+": "+message);
}
void hash(uint64_t value) {totals.trace=(totals.trace^value)*1099511628211ULL;}
template<class T> Word unpack(const T& value) {
    Word result{};for(unsigned i=0;i<4;++i)result[i]=value[i];return result;
}
template<class T> void pack(T& output,const Word& value) {
    for(unsigned i=0;i<4;++i)output[i]=value[i];
}
bool bit(const Word& word,unsigned index) {return (word[index/32]>>(index%32))&1U;}
void bit(Word& word,unsigned index,bool value) {
    const uint32_t mask=1U<<(index%32);
    word[index/32]=(word[index/32]&~mask)|(value?mask:0);
}
Word inverse(Word value) {for(auto& part:value)part=~part;return value;}

// Declarative March elements, independent of the RTL state and address logic.
std::vector<Operation> sequence() {
    std::vector<Operation> result;
    struct Step {bool write,complement;};
    const std::vector<std::vector<Step>> elements={{{true,false}},{{false,false},{true,true}},
        {{false,true},{true,false}},{{false,false},{true,true}},{{false,true},{true,false}},{{false,false}}};
    for(unsigned background=0;background<8;++background) {
        Word value{};
        if(background<7)for(unsigned i=0;i<128;++i)bit(value,i,(i>>background)&1U);
        for(unsigned element=0;element<elements.size();++element)
            for(unsigned offset=0;offset<words;++offset) {
                const unsigned address=(element==3 || element==4)?words-1-offset:offset;
                for(const auto& step:elements[element])
                    result.push_back({address*16,step.write,step.complement?inverse(value):value});
            }
    }
    require(result.size()==80ULL*words,"oracle sequence length");return result;
}

class Test {
    Vwasmetal_memory_bist dut;
    const std::vector<Operation>& operations;
    std::vector<Word> memory;
    enum BusState {Idle,Waiting,Release} bus=Idle;
    Operation pending{};
    Word request_payload{};
    Word response{};
    bool response_fault=false;
    unsigned remaining=0,age=0,delay=0;
    bool jitter=false,blocked=false;
    Defect defect;
    Error expected_error;
    uint64_t acknowledged=0;
    unsigned physical(unsigned address)const {
        unsigned index=address/16;
        if(defect.kind==Defect::Alias)index&=~(1U<<defect.bit);
        require(index<words,"physical model bounds");return index;
    }
    Word store_value(unsigned index,Word value) {
        const Word old=memory[index];
        if(index==defect.word) {
            if(defect.kind==Defect::Stuck0)bit(value,defect.bit,false);
            if(defect.kind==Defect::Stuck1)bit(value,defect.bit,true);
            if(defect.kind==Defect::Rise && !bit(old,defect.bit))bit(value,defect.bit,false);
            if(defect.kind==Defect::Fall && bit(old,defect.bit))bit(value,defect.bit,true);
            if(defect.kind==Defect::And || defect.kind==Defect::Or) {
                const bool merged=defect.kind==Defect::And ?
                    bit(value,defect.bit)&&bit(value,defect.second):bit(value,defect.bit)||bit(value,defect.second);
                bit(value,defect.bit,merged);bit(value,defect.second,merged);
            }
            if(defect.kind==Defect::DropByte) {
                const unsigned lane=defect.bit;
                const uint32_t mask=0xffU<<((lane%4)*8);
                value[lane/4]=(value[lane/4]&~mask)|(old[lane/4]&mask);
            }
            if(defect.kind>=Defect::InvertRise) {
                const bool falling=defect.kind==Defect::InvertFall ||
                    defect.kind==Defect::Force0Fall || defect.kind==Defect::Force1Fall;
                const bool trigger=falling ? bit(old,defect.bit)&&!bit(value,defect.bit):
                    !bit(old,defect.bit)&&bit(value,defect.bit);
                if(trigger) {
                    Word& victim=memory.at(defect.second);
                    const bool invert=defect.kind==Defect::InvertRise || defect.kind==Defect::InvertFall;
                    bit(victim,defect.bit,invert?!bit(victim,defect.bit):
                        defect.kind==Defect::Force1Rise || defect.kind==Defect::Force1Fall);
                }
            }
        }
        return value;
    }
    void first_error(unsigned code,const Word& observed) {
        if(expected_error.code)return;
        expected_error={code,pending.address,pending.data,observed};
        if(code==3)++totals.timeouts;
    }
    void status() {
        require(dut.completed_operations==acknowledged,"completion counter differs from actual responses");
        require(bool(dut.failed)==bool(expected_error.code),"failure detection differs from independent oracle");
        require(dut.error_code==expected_error.code,"wrong error class");
        require(dut.error_address==expected_error.address && unpack(dut.expected_data)==expected_error.expected &&
                unpack(dut.observed_data)==expected_error.observed,"first-error evidence changed or is incorrect");
        if(dut.done)require(!dut.busy && !dut.valid && bus==Idle,"done before memory request was released");
    }
public:
    size_t accepted=0;
    explicit Test(const std::vector<Operation>& list):operations(list),memory(words) {dut.start=0;dut.reset=0;dut.clk=0;}
    void tick() {
        dut.clk=0;dut.eval();
        const bool response_ready=!dut.reset && bus==Waiting && !blocked && remaining==0;
        dut.ready=response_ready;dut.fault=response_ready?response_fault:1;
        Word poison{};for(unsigned i=0;i<4;++i)poison[i]=uint32_t(totals.cycles+0x1937U+17*i);
        pack(dut.rdata,response_ready?response:poison);dut.eval();
        if(dut.reset) {
            require(!dut.valid,"reset left a destructive request active");
            bus=Idle;age=0;accepted=0;acknowledged=0;expected_error={};
        } else {
            if(bus==Waiting) {
                require(dut.valid && dut.address==pending.address && bool(dut.write)==pending.write &&
                        dut.mask==0xffff && unpack(dut.wdata)==request_payload,
                        "pending request withdrawn or changed");
                if(response_ready) {
                    ++acknowledged;hash(acknowledged);
                    if(response_fault)first_error(2,response);
                    else if(!pending.write && response!=pending.data)first_error(1,response);
                    bus=Release;
                } else if(!blocked && remaining)--remaining;
            } else if(bus==Idle && dut.valid) {
                require(accepted<operations.size(),"extra memory request");
                pending=operations[accepted++];
                request_payload=unpack(dut.wdata);
                require(dut.address==pending.address && bool(dut.write)==pending.write && dut.mask==0xffff,
                        "request sequence, direction or mask differs from March oracle");
                if(pending.write)require(unpack(dut.wdata)==pending.data,"write background differs from oracle");
                ++totals.requests;hash(pending.address);hash(pending.write);
                const unsigned index=physical(pending.address);
                if(pending.write) {memory[index]=store_value(index,pending.data);++totals.writes;response=poison;}
                else {response=memory[index];++totals.reads;
                    if(defect.kind==Defect::ReadXor && index==defect.word)bit(response,defect.bit,!bit(response,defect.bit));}
                for(uint32_t part:response)hash(part);
                response_fault=(defect.kind==Defect::Bus && accepted==3) ||
                    ((defect.kind==Defect::BusRead || defect.kind==Defect::BusAndData) &&
                     !pending.write && accepted==words+1);
                if(response_fault && defect.kind==Defect::BusAndData)bit(response,0,!bit(response,0));
                remaining=jitter?unsigned((totals.cycles+accepted)%6):delay;bus=Waiting;
            } else if(bus==Release && !dut.valid)bus=Idle;
            if(dut.valid && !dut.ready) {
                if(++age==TEST_TIMEOUT)first_error(3,{});
            } else age=0;
        }
        dut.clk=1;dut.eval();++totals.cycles;dut.clk=0;dut.eval();
        status();
    }
    void reset() {
        const auto before=memory;dut.start=0;dut.reset=1;tick();tick();dut.reset=0;tick();++totals.resets;
        require(before==memory,"reset fabricated new SRAM contents");
        require(!dut.done && !dut.busy && !dut.failed,"reset status");
    }
    void configure(Defect injected={},unsigned latency=0,bool varying=false,bool no_response=false) {
        defect=injected;delay=latency;jitter=varying;blocked=no_response;
        for(unsigned a=0;a<words;++a)for(unsigned b=0;b<4;++b)
            memory[a][b]=0x9381a76dU^(0x9e3779b9U*a)^(0x111d0137U*b);
        reset();
    }
    void start() {dut.start=1;tick();require(dut.busy && !dut.done,"start did not begin a new test");}
    void finish(bool should_fail,bool pulses=false) {
        uint64_t limit=operations.size()*(uint64_t(delay)+12)+TEST_TIMEOUT+20;
        while(!dut.done && limit--) {
            if(pulses)dut.start=totals.cycles&1U;
            tick();
        }
        require(dut.done,"campaign did not finish within its response bound");
        require(bool(expected_error.code)==should_fail,"injected defect was not sensitized");
        if(!should_fail) {
            require(accepted==operations.size() && acknowledged==operations.size(),"incomplete successful March trace");
            require(std::all_of(memory.begin(),memory.end(),[](const Word& value){return value==Word{};}),
                    "successful test did not leave zero background");
        } else {
            ++totals.detected;
            const auto before=totals.requests;
            for(unsigned i=0;i<3;++i)tick();
            require(dut.done && totals.requests==before,"failed test issued further memory traffic");
        }
        ++totals.campaigns;hash(dut.error_code);hash(dut.error_address);
    }
    void run(Defect injected={},unsigned latency=0,bool varying=false,bool pulses=false) {
        configure(injected,latency,varying);start();finish(injected.kind!=Defect::None,pulses);
    }
    void held_start() {
        run();const auto before=totals.requests;
        for(unsigned i=0;i<17;++i){tick();++totals.held_start_cycles;}
        require(dut.done && totals.requests==before,"held start repeated destructive test");
        dut.start=0;tick();accepted=0;acknowledged=0;expected_error={};start();finish(false);
    }
    void timeout(bool forever,bool read=false) {
        configure({},read?0:TEST_TIMEOUT+3,false,read?false:forever);start();
        if(read) {
            while(acknowledged<words)tick();
            tick();require(dut.valid && !dut.write,"read-timeout setup did not reach a read");
            delay=TEST_TIMEOUT+3;blocked=forever;
        }
        for(unsigned i=0;i<TEST_TIMEOUT+2;++i)tick();
        require(dut.failed && dut.error_code==3 && dut.busy && dut.valid && !dut.done,
                "timeout released an outstanding memory operation");
        if(forever) {for(unsigned i=0;i<7;++i)tick();blocked=false;reset();run();}
        else finish(true);
    }
    void interrupt(unsigned target,unsigned offset) {
        configure({},3);start();
        unsigned bound=unsigned(operations.size()*10+10);
        while(accepted<=target && bound--)tick();
        require(bound!=0,"could not reach reset target");
        for(unsigned i=0;i<offset;++i)tick();
        reset();start();finish(false);
    }
};

int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    try {
        const auto operations=sequence();Test test(operations);
        context="healthy variable latency";test.run({},0,true,true);
        context="healthy fixed latency";test.run({},7);
        context="held start and restart";test.held_start();
        context="late timeout completion";test.timeout(false);
        context="permanent timeout and reset recovery";test.timeout(true);
        context="late read timeout completion";test.timeout(false,true);
        context="permanent read timeout and reset recovery";test.timeout(true,true);
        if(words<=8) {
            for(auto kind:{Defect::Stuck0,Defect::Stuck1,Defect::Rise,Defect::Fall,Defect::ReadXor})
                for(unsigned address=0;address<words;++address)for(unsigned b=0;b<128;++b) {
                    context="single bit "+std::to_string(kind)+" word "+std::to_string(address)+" bit "+std::to_string(b);
                    test.run({kind,address,b,0},1,true);
                }
            // Each pair of data bits differs in at least one separating background.
            for(auto kind:{Defect::And,Defect::Or})for(unsigned a=0;a<128;++a)for(unsigned b=a+1;b<128;++b) {
                context="bridged bits "+std::to_string(a)+","+std::to_string(b);
                test.run({kind,words-1,a,b});
            }
            for(unsigned b=0;(1U<<b)<words;++b) {
                context="address alias "+std::to_string(b);test.run({Defect::Alias,0,b,0});
            }
            for(auto kind:{Defect::InvertRise,Defect::InvertFall,Defect::Force0Rise,Defect::Force1Rise,
                           Defect::Force0Fall,Defect::Force1Fall})
                for(unsigned aggressor=0;aggressor<words;++aggressor)for(unsigned victim=0;victim<words;++victim)
                    if(aggressor!=victim)for(unsigned b=0;b<128;++b) {
                        context="coupled words "+std::to_string(kind)+" "+std::to_string(aggressor)+
                            ","+std::to_string(victim)+" bit "+std::to_string(b);
                        test.run({kind,aggressor,b,victim});
                    }
            for(unsigned lane=0;lane<16;++lane) {
                context="lost write lane "+std::to_string(lane);test.run({Defect::DropByte,words-1,lane,0});
            }
            context="memory fault response";test.run({Defect::Bus,0,0,0});
            context="read memory fault response";test.run({Defect::BusRead,0,0,0});
            context="read fault has priority over wrong data";test.run({Defect::BusAndData,0,0,0});
            for(unsigned target=0;target<operations.size();++target)for(unsigned offset=0;offset<7;++offset) {
                context="reset command "+std::to_string(target)+" offset "+std::to_string(offset);
                test.interrupt(target,offset);
            }
        }
        std::cout<<"{\"campaigns\":"<<totals.campaigns<<",\"cycles\":"<<totals.cycles
            <<",\"requests\":"<<totals.requests<<",\"reads\":"<<totals.reads<<",\"writes\":"<<totals.writes
            <<",\"resets\":"<<totals.resets<<",\"detected_faults\":"<<totals.detected
            <<",\"timeouts\":"<<totals.timeouts<<",\"held_start_cycles\":"<<totals.held_start_cycles
            <<",\"trace_hash\":"<<totals.trace<<"}\n";
    } catch(const std::exception& error) {std::cerr<<error.what()<<"\n";return 1;}
}
