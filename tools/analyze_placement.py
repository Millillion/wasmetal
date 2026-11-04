#!/usr/bin/env python3
"""Summarize placed resources and net spread without claiming routed timing."""
import argparse
from collections import Counter,defaultdict
import json
import os
from pathlib import Path
import re

from prepare_standalone import ROOT,digest


def category(name):
    if '.core.' in name:
        if '.fpu.' in name or '.\\fpu.' in name:return 'floating point'
        if 'simd' in name:return 'SIMD'
        if '.value_file.' in name:return 'value storage'
        if 'labels_memory' in name or 'frames_memory' in name:return 'labels and call frames'
        return 'other CPU logic'
    if '.ram_backend.' in name:return 'backing RAM'
    if '.loader.' in name:return 'image loader'
    if '.execution.' in name:return 'boot and program stores'
    return 'UART, clocks and board'


def analyze(module):
    coordinates={};groups={};types=Counter();group_counts=defaultdict(Counter);endpoints=defaultdict(list)
    for name,cell in module['cells'].items():
        bel=cell.get('attributes',{}).get('NEXTPNR_BEL','')
        match=re.match(r'X(\d+)/Y(\d+)/',bel)
        if not match:raise ValueError('unplaced or unrecognized cell location: '+name)
        coordinates[name]=tuple(map(int,match.groups()));groups[name]=category(name)
        types[cell['type']]+=1;group_counts[groups[name]][cell['type']]+=1
        for port,bits in cell['connections'].items():
            direction=cell['port_directions'][port]
            if direction not in ('input','output','inout'):raise ValueError('unrecognized port direction')
            for bit in bits:
                if isinstance(bit,int):endpoints[bit].append((name,port,direction))
    names=defaultdict(list);globals_=set()
    for name,net in module['netnames'].items():
        global_net=int(net.get('attributes',{}).get('ECP5_IS_GLOBAL','0').strip(),2)!=0
        for i,bit in enumerate(net['bits']):
            if not isinstance(bit,int):continue
            label=name if len(net['bits'])==1 else f'{name}[{i+net.get("offset",0)}]'
            names[bit].append((int(net.get('hide_name',0)),len(label),label))
            if global_net:globals_.add(bit)
    nets=[]
    for bit,pins in endpoints.items():
        drivers=[(n,p) for n,p,d in pins if d=='output']
        sinks=[(n,p) for n,p,d in pins if d in ('input','inout')]
        if not sinks:continue
        xs=[coordinates[n][0] for n,_,_ in pins];ys=[coordinates[n][1] for n,_,_ in pins]
        span=max(xs)-min(xs)+max(ys)-min(ys)
        excluded=''
        if bit in globals_ or any(module['cells'][n]['type']=='DCCA' for n,_ in drivers):excluded='global clock/distribution'
        for n,p in drivers:
            cell=module['cells'][n];params=cell.get('parameters',{})
            if cell['type']=='TRELLIS_COMB' and p=='F' and params.get('MODE','LOGIC').strip()=='LOGIC':
                value=params.get('INITVAL','').strip()
                if value and set(value)<={'0','1'} and int(value,2) in (0,65535):excluded='constant LUT'
        aliases=sorted(names[bit]);label=aliases[0][2] if aliases else f'bit {bit}'
        nets.append({'name':label,'bit':bit,'drivers':[{'cell':n,'port':p,'location':coordinates[n]} for n,p in drivers],
            'sink_pins':len(sinks),'sink_cells':len({n for n,_ in sinks}),
            'half_perimeter_tiles':span,'bbox':[min(xs),min(ys),max(xs),max(ys)],
            'fanout_times_span':len(sinks)*span,'excluded_from_logic_ranking':excluded,
            'sink_categories':dict(Counter(groups[n] for n,_ in sinks)),
            'sink_examples':[{'cell':n,'port':p,'location':coordinates[n]} for n,p in sinks[:12]]})
    logic=[n for n in nets if not n['excluded_from_logic_ranking']]
    summary={'placed_cells':sum(types.values()),'resource_counts':dict(types),
        'name_based_categories':{k:dict(v) for k,v in sorted(group_counts.items())},
        'nets_with_sinks':len(nets),'logic_nets_ranked':len(logic),
        'top_fanout':sorted(logic,key=lambda n:(-n['sink_pins'],n['name']))[:40],
        'top_fanout_times_span':sorted(logic,key=lambda n:(-n['fanout_times_span'],n['name']))[:40],
        'excluded_global_or_constant_nets':sorted([n for n in nets if n['excluded_from_logic_ranking']],key=lambda n:-n['sink_pins'])[:20]}
    return summary,coordinates


def figure(path,module,coordinates,report):
    # Keep font caches in this build, not the user's home directory.
    os.environ.setdefault('MPLCONFIGDIR',str(path.parent/'matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import BoundaryNorm
    width=max(x for x,y in coordinates.values())+1;height=max(y for x,y in coordinates.values())+1
    grid=np.zeros((height,width),dtype=int)
    for name,cell in module['cells'].items():
        if cell['type']=='TRELLIS_COMB':x,y=coordinates[name];grid[y,x]+=1
    fig,axes=plt.subplots(1,2,figsize=(14,6),layout='constrained')
    palette=plt.get_cmap('Blues',9)
    plotted=axes[0].imshow(grid,origin='lower',cmap=palette,norm=BoundaryNorm(np.arange(-.5,9.5),palette.N))
    fig.colorbar(plotted,ax=axes[0],label='Placed logic cells at each tile',shrink=.8,ticks=range(9))
    for kind,marker,color,label in [('DP16KD','s','#b05a00','Block RAM'),('MULT18X18D','^','#b52a50','DSP')]:
        points=[coordinates[n] for n,c in module['cells'].items() if c['type']==kind]
        if points:axes[0].scatter(*zip(*points),s=12,marker=marker,c=color,label=label)
    axes[0].set_title('Resource placement');axes[0].legend(loc='upper right',fontsize=8)
    axes[1].imshow(grid,origin='lower',cmap='Greys',vmin=0,vmax=16)
    colors=plt.get_cmap('tab10')
    for i,net in enumerate(report['top_fanout_times_span'][:6]):
        x0,y0,x1,y1=net['bbox'];color=colors(i)
        axes[1].add_patch(plt.Rectangle((x0,y0),x1-x0,y1-y0,fill=False,color=color,linewidth=1.5,
            label=f'{i+1}: {net["sink_pins"]} sink pins; span {net["half_perimeter_tiles"]}'))
        for driver in net['drivers']:axes[1].scatter(*driver['location'],marker='x',s=45,color=color)
    axes[1].set_title('Six highest fanout × span scores');axes[1].legend(loc='upper right',fontsize=8)
    for ax in axes:
        ax.set_xlabel('Device tile X');ax.set_ylabel('Device tile Y');ax.set_xlim(-1,width);ax.set_ylim(-1,height)
    fig.suptitle('WasMetal programmable ULX3S placement\nSpread estimates only: routing and timing are not established',fontsize=13)
    path.parent.mkdir(parents=True,exist_ok=True);fig.savefig(path,dpi=150);plt.close(fig)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--placement',type=Path,required=True);parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True);parser.add_argument('--figure',type=Path)
    args=parser.parse_args();placement=args.placement.resolve();manifest_path=args.manifest.resolve()
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.unlink(missing_ok=True)
    manifest=json.loads(manifest_path.read_text());design=manifest_path.parent/'design.json'
    if digest(design)!=manifest['netlist_sha256']:raise ValueError('mapping manifest does not match the design')
    paths=[placement,manifest_path,design,Path(__file__).resolve(),ROOT/'tools/prepare_standalone.py']
    inputs={str(p.relative_to(ROOT)):digest(p) for p in paths};inputs.update(manifest['inputs'])
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('stale placement analysis input: '+name)
    document=json.loads(placement.read_text())
    if len(document['modules'])!=1:raise ValueError('expected one packed top')
    module=next(iter(document['modules'].values()));summary,coordinates=analyze(module)
    summary.update(status='analyzed',scope='Placed-cell counts and geometric net-spread estimates; not actual routed wire lengths, congestion attribution, timing or FPGA success.',
        inputs=inputs,physical_hardware_tested=False,
        metric='fanout_times_span = input/inout pin count * Manhattan bounding-box half-perimeter in device tiles; global and constant nets excluded',
        classification='Resource categories are based on instance names; packing can obscure original hierarchy.')
    if args.figure:
        figure(args.figure,module,coordinates,summary)
        summary['figure_sha256']=digest(args.figure)
    for name,value in inputs.items():
        if digest(ROOT/name)!=value:raise ValueError('placement analysis input changed: '+name)
    args.report.write_text(json.dumps(summary,indent=2)+'\n')
    print('Analyzed',summary['placed_cells'],'placed cells and',summary['logic_nets_ranked'],'logic nets')
    for net in summary['top_fanout_times_span'][:10]:
        print(net['sink_pins'],net['half_perimeter_tiles'],net['name'])


if __name__=='__main__':main()
