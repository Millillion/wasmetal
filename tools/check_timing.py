#!/usr/bin/env python3
"""Check clock constraints and the held-bus timing contract in a nextpnr report."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def clock_kind(name):
    name=name.removeprefix('posedge ').removeprefix('negedge ')
    name=name.removeprefix('$glbnet$')
    if name=='core_clock': return 'core'
    if name=='bridge_clock': return 'bridge'
    if name.startswith('clk_25mhz'): return 'oscillator'
    if name=='<async>': return None
    raise ValueError(f'unrecognized clock: {name}')


def audit(path):
    report=json.loads(path.read_text())
    clocks={}
    for name,values in report['fmax'].items():
        kind=clock_kind(name)
        if kind is None: raise ValueError('unexpected asynchronous fmax entry')
        required={'oscillator':25.0,'bridge':12.5,'core':1.0}[kind]
        achieved=float(values['achieved']);constraint=float(values['constraint'])
        if not math.isfinite(achieved) or not math.isfinite(constraint) or constraint<required or achieved<constraint:
            raise ValueError(f'clock failed timing: {name}: {values}')
        if kind in clocks: raise ValueError(f'duplicate {kind} clock')
        clocks[kind]={'net':name,'required_mhz':constraint,'achieved_mhz':achieved}
    if set(clocks)!={'oscillator','bridge','core'}: raise ValueError('missing constrained clock')
    crossings={}
    core_paths={}
    for entry in report['critical_paths']:
        source=clock_kind(entry['from']);destination=clock_kind(entry['to'])
        if source==destination=='core':
            edges=[entry[key].split(' ',1)[0] for key in ('from','to')]
            if any(edge not in ('posedge','negedge') for edge in edges):
                raise ValueError('core timing path lacks clock-edge information')
            budget=(1000.0 if edges[0]==edges[1] else 500.0)/clocks['core']['required_mhz']
            delay=sum(float(segment['delay']) for segment in entry['path'])
            if not math.isfinite(delay) or delay<0 or delay>budget:
                raise ValueError(f'core path exceeds its {budget} ns clock-edge budget')
            core_paths['->'.join(edges)]={'delay_ns':delay,'budget_ns':budget}
        if source is None or destination is None or source==destination: continue
        delay=sum(float(segment['delay']) for segment in entry['path'])
        if not math.isfinite(delay) or delay<0 or delay>1000.0:
            raise ValueError(f'held-bus crossing exceeds conservative 1 us budget: {entry["from"]} -> {entry["to"]}: {delay} ns')
        key=source+'->'+destination
        crossings[key]=max(crossings.get(key,0),delay)
    if set(crossings)!={'bridge->core','core->bridge'}:
        raise ValueError('report does not contain both held-bus clock crossings')
    if not core_paths: raise ValueError('report does not contain a core critical path')
    return {'report_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'clocks':clocks,'crossing_budget_ns':1000.0,'maximum_crossing_delay_ns':crossings,
            'reported_core_paths':core_paths,
            'utilization':report['utilization'],
            'physical_hardware_tested':False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('report',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=audit(args.report)
    text=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')


if __name__=='__main__': main()
