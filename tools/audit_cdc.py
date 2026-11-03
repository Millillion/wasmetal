#!/usr/bin/env python3
"""Check the actual synchronizer chains, allowed crossings and four-state reset."""
import copy
import json
from pathlib import Path
import subprocess

from build_board import yosys
from prepare_standalone import ROOT,digest

CHAINS={
    'source_release':('s_clk','reset','1'),
    'destination_release':('m_clk','reset','1'),
    'request_sync':('m_clk','m_reset','request_toggle'),
    'response_sync':('s_clk','s_reset','response_toggle'),
    'destination_up_sync':('s_clk','s_reset','destination_up'),
}


def audit(module,mapped=False):
    nets=module['netnames'];cells=module['cells']
    def bits(name):return [name] if name in ('0','1') else nets[name]['bits']
    drivers={};consumers={}
    for name,c in cells.items():
        for port,values in c['connections'].items():
            for n,bit in enumerate(values):
                if c['port_directions'][port]=='output':
                    if bit in drivers:raise ValueError('multiple drivers')
                    drivers[bit]=(name,port,n)
                else:consumers.setdefault(bit,[]).append((name,port,n))
    reports=[]
    for name,(clock,reset,source) in CHAINS.items():
        net=nets[name];q=net['bits'];attrs=net.get('attributes',{})
        if len(q)!=2 or attrs.get('async_reg')!='true' or attrs.get('ASYNC_REG')!='TRUE':
            raise ValueError('missing synchronizer attributes or stages: '+name)
        for n,bit in enumerate(q):
            driver,port,index=drivers[bit];c=cells[driver];p=c['parameters'];pins=c['connections']
            if port!='Q' or c['type']!=('TRELLIS_FF' if mapped else '$adff'):
                raise ValueError('synchronizer is not a register')
            if pins['CLK']!=bits(clock):raise ValueError('wrong synchronizer clock')
            actual=pins['DI'] if mapped else [pins['D'][index]]
            if actual!=([q[0]] if n else bits(source)):raise ValueError('broken synchronizer chain')
            if mapped:
                if p.get('CLKMUX','').strip()!='CLK' or p.get('CEMUX','').strip()!='1' or p.get('SRMODE')!='ASYNC':
                    raise ValueError('mapped synchronizer clock/enable/reset mode changed')
                if p.get('REGSET')!='RESET':raise ValueError('mapped synchronizer reset value changed')
            else:
                expected_resets=[(bits(reset),1)]
                if reset in ('s_reset','m_reset'):
                    release='source_release' if reset=='s_reset' else 'destination_release'
                    reset_driver=cells[drivers[bits(reset)[0]][0]]
                    if reset_driver['type'] not in ('$not','$logic_not') or reset_driver['connections']['A']!=[bits(release)[1]]:
                        raise ValueError('reset release is not the second synchronizer stage')
                    # PROC recognizes the inversion and can represent the same
                    # asynchronous reset with a low-active register primitive.
                    expected_resets.append(([bits(release)[1]],0))
                if (pins['ARST'],int(p['ARST_POLARITY'],2)) not in expected_resets or int(p['ARST_VALUE'],2)!=0 or int(p['CLK_POLARITY'],2)!=1:
                    raise ValueError('generic synchronizer reset/clock mode changed')
        first_users=consumers.get(q[0],[])
        if len(first_users)!=1 or first_users[0][0]!=drivers[q[1]][0] or first_users[0][1]!=('DI' if mapped else 'D'):
            raise ValueError('first synchronizer stage has extra fanout')
        if any(q[0] in p['bits'] for p in module['ports'].values() if p['direction']=='output'):
            raise ValueError('first synchronizer stage is exposed as an output')
        reports.append({'name':name,'clock':clock,'stages':2,'first_stage_consumers':1})
    crossings=[]
    if not mapped:
        domains={};registers=[]
        for name,c in cells.items():
            if 'CLK' not in c['connections']:continue
            if c['type']!='$adff':raise ValueError('unexpected sequential cell')
            clock=c['connections']['CLK']
            domain=next((n for n in ('s_clk','m_clk') if clock==bits(n)),None)
            if domain is None:raise ValueError('unknown register clock')
            for q in c['connections']['Q']:domains[q]=domain
            registers.append(c)
        for name,p in module['ports'].items():
            if p['direction']=='input' and name not in ('s_clk','m_clk','reset'):
                domain='s_clk' if name.startswith('s_') else 'm_clk'
                for bit in p['bits']:domains[bit]=domain
        allowed=[]
        for name,(_,_,source) in CHAINS.items():
            if source!='1':allowed.append((name,set(bits(source)),{bits(name)[0]}))
        allowed.extend([
            ('request payload',set(bits('request_payload')),set(bits('destination_request'))),
            ('response payload',set(bits('response_payload')),set(bits('s_rdata')+bits('s_fault'))),
        ])
        cache={};visiting=set()
        def roots(bit):
            if isinstance(bit,str) or bit==bits('reset')[0]:return set()
            if bit in domains:return {bit}
            if bit in cache:return cache[bit]
            if bit in visiting:raise ValueError('combinational loop')
            if bit not in drivers:raise ValueError('unexplained undriven crossing')
            visiting.add(bit);c=cells[drivers[bit][0]];found=set()
            for port,values in c['connections'].items():
                if c['port_directions'][port]=='input':
                    for value in values:found.update(roots(value))
            visiting.remove(bit);cache[bit]=found;return found
        seen=set()
        for c in registers:
            for target,data in zip(c['connections']['Q'],c['connections']['D']):
                for origin in roots(data):
                    if domains[origin]==domains[target]:continue
                    matches=[name for name,sources,targets in allowed if origin in sources and target in targets]
                    if len(matches)!=1:raise ValueError('unexpected register clock crossing')
                    seen.add(matches[0])
        if seen!={name for name,_,_ in allowed}:raise ValueError('expected clock crossing is missing')
        crossings=sorted(seen)
    return {'chains':reports,'allowed_register_crossings':crossings}


def main():
    directory=ROOT/'build/memory-cdc';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/'soc/external/wasmetal_memory_cdc.sv';bench=ROOT/'tests/memory/cdc_four_state.sv'
    mapped_path=directory/'cdc.json'
    inputs=[source,bench,Path(__file__).resolve(),ROOT/'tools/build_board.py',mapped_path]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in inputs}
    generic_path=directory/'structure.json'
    yosys(f'read_verilog -sv {source}\nhierarchy -top wasmetal_memory_cdc\nproc\nopt_clean\ncheck -assert\nwrite_json {generic_path}\n',
          'structure',directory)
    generic=json.loads(generic_path.read_text())['modules']['wasmetal_memory_cdc']
    mapped=json.loads(mapped_path.read_text())['modules']['wasmetal_memory_cdc']
    checked={'generic':audit(generic),'mapped':audit(mapped,True)}
    controls=[]
    for name in ('missing-attribute','first-stage-output','bypassed-stage','raw-data-crossing'):
        bad=copy.deepcopy(generic);q=bad['netnames']['request_sync']['bits']
        if name=='missing-attribute':del bad['netnames']['request_sync']['attributes']['ASYNC_REG']
        elif name=='first-stage-output':bad['ports']['unsafe_output']={'direction':'output','bits':[q[0]]}
        else:
            target=q[1] if name=='bypassed-stage' else bad['netnames']['destination_request']['bits'][0]
            for c in bad['cells'].values():
                if c['type']=='$adff' and target in c['connections']['Q']:
                    index=c['connections']['Q'].index(target)
                    c['connections']['D'][index]=bad['netnames']['request_toggle' if name=='bypassed-stage' else 's_address']['bits'][0]
        try:audit(bad)
        except ValueError:controls.append(name)
        else:raise ValueError('structural negative control escaped: '+name)
    def simulate(rtl,name):
        binary=directory/(name+'.vvp')
        subprocess.run([str(ROOT/'.cache/tools/usr/bin/iverilog'),'-B',str(ROOT/'.cache/tools/usr/lib/x86_64-linux-gnu/ivl'),
            '-g2012','-s','cdc_four_state','-o',str(binary),str(rtl),str(bench)],check=True)
        result=subprocess.run([str(ROOT/'.cache/tools/usr/bin/vvp'),str(binary)],capture_output=True,text=True,timeout=30)
        (directory/(name+'.log')).write_text(result.stdout+result.stderr);return result
    result=simulate(source,'four-state')
    if result.returncode or 'PASS CDC four-state' not in result.stdout:raise RuntimeError(result.stdout+result.stderr)
    corrupt=directory/'missing-reset.sv';old='source_state<=SOURCE_IDLE;request_toggle<=0;request_payload<=0;'
    assert source.read_text().count(old)==1
    corrupt.write_text(source.read_text().replace(old,'source_state<=SOURCE_IDLE;request_payload<=0;'))
    negative=simulate(corrupt,'four-state-negative')
    if negative.returncode==0 or 'four-state response timeout' not in negative.stdout:
        raise RuntimeError('four-state missing-reset control escaped')
    controls.append('uninitialized-request-toggle')
    if any(digest(ROOT/name)!=value for name,value in hashes.items()):raise RuntimeError('CDC audit inputs changed')
    report={'status':'passed','scope':'designated synchronizers, generic register crossings and four-state startup/reset',
        'structure':checked,'negative_controls_rejected':controls,'inputs':hashes,'generic_netlist_sha256':digest(generic_path),
        'physical_placement_checked':False,'bundled_data_delays_constrained':False,'metastability_signoff':False}
    (ROOT/'reports/cdc-structure.json').write_text(json.dumps(report,indent=2)+'\n')
    print(result.stdout,end='');print('PASS generic/mapped synchronizer structure and all register clock crossings')


if __name__=='__main__':main()
