#!/usr/bin/env python3
"""Check the mapped board's UART/reset synchronizers and free-running clock."""
import argparse
import copy
import json
from pathlib import Path
from prepare_standalone import ROOT,digest


def audit(module):
    drivers={};consumers={}
    for name,cell in module['cells'].items():
        for port,bits in cell['connections'].items():
            for bit in bits:
                if not isinstance(bit,int):continue
                if cell['port_directions'][port]=='output':
                    if bit in drivers:raise ValueError('multiple signal drivers')
                    drivers[bit]=(name,cell,port)
                else:consumers.setdefault(bit,[]).append((name,port))
    for name,port in module['ports'].items():
        if port['direction']=='output':
            for bit in port['bits']:consumers.setdefault(bit,[]).append(('top port',name))
    def bits(name,width):
        value=module['netnames'][name]['bits']
        if len(value)!=width:raise ValueError('wrong synchronization width: '+name)
        return value
    clock=bits('core_clock',1);oscillator=module['ports']['clk_25mhz']['bits']
    divider=bits('divider',5)
    def flop(bit,clk):
        if bit not in drivers:raise ValueError('synchronizer or divider net has no register driver')
        name,cell,port=drivers[bit];p=cell['parameters'];pins=cell['connections']
        if cell['type']!='TRELLIS_FF' or port!='Q' or pins['CLK']!=clk:
            raise ValueError('wrong register or clock')
        if p.get('CEMUX','').strip()!='1' or p.get('CLKMUX','').strip()!='CLK':
            raise ValueError('synchronizer or divider clock is gated/inverted')
        return name,cell
    _,buffer,_=drivers[clock[0]]
    if buffer['type']!='DCCA' or buffer['connections']['CE']!=['1'] or buffer['connections']['CLKI']!=[divider[4]]:
        raise ValueError('core clock is not the free-running buffered divider')
    for bit in divider:flop(bit,oscillator)
    def value(bit,known,active=None):
        if bit in ('0','1'):return int(bit)
        if bit in known:return known[bit]
        active=set() if active is None else active
        if bit in active:raise ValueError('loop in reset cone')
        active=active|{bit};_,cell,_=drivers[bit];pins=cell['connections']
        if cell['type']!='LUT4':raise ValueError('unreviewed reset-cone primitive')
        index=sum(value(pins[pin][0],known,active)<<n for n,pin in enumerate('ABCD'))
        return int(cell['parameters']['INIT'],2)>>index&1
    chains={}
    for net,source,async_reset,reset_source in [
        ('reset_sync','1',True,module['ports']['btn_n']['bits'][0]),
        ('system.serial.rx_sync',module['ports']['ftdi_txd']['bits'][0],False,bits('reset_sync',2)[1])]:
        first,second=bits(net,2);a,fa=flop(first,clock);b,fb=flop(second,clock)
        attrs=module['netnames'][net]['attributes']
        if not any(str(attrs.get(key,'')).lower()=='true' for key in ('ASYNC_REG','async_reg')):
            raise ValueError('synchronizer attribute was lost')
        if fa['connections']['DI']!=[source] or fb['connections']['DI']!=[first]:
            raise ValueError('two-stage synchronization was bypassed')
        if consumers.get(first)!=[(b,'DI')]:raise ValueError('first synchronizer stage has other consumers')
        if not async_reset and consumers.get(source)!=[(a,'DI')]:
            raise ValueError('raw UART input reaches other logic')
        for cell in (fa,fb):
            expected='ASYNC' if async_reset else 'LSR_OVER_CE'
            if cell['parameters'].get('SRMODE','').strip()!=expected:
                raise ValueError('wrong synchronizer reset mode')
            if cell['parameters'].get('REGSET','').strip()!=('RESET' if async_reset else 'SET'):
                raise ValueError('wrong synchronizer reset value')
            if cell['parameters'].get('LSRMUX','').strip()!='LSR':raise ValueError('wrong reset polarity')
            for level in (0,1):
                if value(cell['connections']['LSR'][0],{reset_source:level})!=1-level:
                    raise ValueError('reset depends on the wrong source/polarity')
        chains[net]={'stages':[a,b],'clock':clock,'asynchronous_assertion':async_reset}
    return chains


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist',type=Path,default=ROOT/'build/loadable-ulx3s/design.json')
    args=parser.parse_args();path=args.netlist.resolve();manifest_path=path.with_suffix('.manifest.json')
    manifest=json.loads(manifest_path.read_text())
    if digest(path)!=manifest['netlist_sha256']:raise ValueError('board circuit hash mismatch')
    for name,value in manifest['inputs'].items():
        if digest(ROOT/name)!=value:raise ValueError('stale board circuit input: '+name)
    module=json.loads(path.read_text())['modules']['wasmetal_loadable_ulx3s'];chains=audit(module)
    inputs={str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__).resolve(),path,manifest_path]}
    rejected=[]
    for kind in ('uart-bypass','first-stage-leak','wrong-clock','synchronous-reset','reset-polarity','missing-attribute','gated-clock','undriven-stage'):
        broken=dict(module);broken['cells']=dict(module['cells'])
        net='reset_sync' if kind in ('synchronous-reset','reset-polarity','undriven-stage') else 'system.serial.rx_sync'
        first,second=chains[net]['stages']
        broken['cells'][second]=copy.deepcopy(module['cells'][second]);cell=broken['cells'][second]
        if kind=='uart-bypass':cell['connections']['DI']=module['ports']['ftdi_txd']['bits']
        elif kind=='first-stage-leak':
            broken['ports']=copy.deepcopy(module['ports'])
            broken['ports']['ftdi_rxd']['bits']=module['cells'][first]['connections']['Q']
        elif kind=='wrong-clock':cell['connections']['CLK']=module['ports']['clk_25mhz']['bits']
        elif kind=='synchronous-reset':cell['parameters']['SRMODE']='LSR_OVER_CE'
        elif kind=='reset-polarity':cell['connections']['LSR']=module['ports']['btn_n']['bits']
        elif kind=='gated-clock':cell['parameters']['CEMUX']='0'
        elif kind=='undriven-stage':
            broken['netnames']=dict(module['netnames']);broken['netnames'][net]=copy.deepcopy(module['netnames'][net])
            orphan=1+max(bit for wire in module['netnames'].values() for bit in wire['bits'] if isinstance(bit,int))
            broken['netnames'][net]['bits'][1]=orphan
        else:
            broken['netnames']=dict(module['netnames']);broken['netnames'][net]=copy.deepcopy(module['netnames'][net])
            for key in ('ASYNC_REG','async_reg'):broken['netnames'][net]['attributes'].pop(key,None)
        try:audit(broken)
        except ValueError:rejected.append(kind)
        else:raise ValueError('I/O audit accepted '+kind)
    if any(digest(ROOT/name)!=value for name,value in inputs.items()):raise ValueError('I/O audit input changed')
    for name,value in manifest['inputs'].items():
        if digest(ROOT/name)!=value:raise ValueError('board circuit input changed during I/O audit: '+name)
    report={'status':'passed','scope':'mapped functional structure, not analog metastability or physical timing signoff',
        'chains':chains,'divider_registers':5,'negative_controls_rejected':rejected,'inputs':inputs,
        'netlist_sha256':digest(path),'physical_hardware_tested':False}
    (ROOT/'reports/loadable-io.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS mapped UART/reset chains and clock structure')


if __name__=='__main__':main()
