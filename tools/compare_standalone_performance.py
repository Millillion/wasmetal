#!/usr/bin/env python3
"""Compare measured standalone cycles with the preserved byte-memory CI run."""
import json
from pathlib import Path

from prepare_standalone import ROOT, digest


def main():
    inputs={str(Path(__file__).resolve().relative_to(ROOT)):digest(Path(__file__).resolve())}
    results={}
    for name in ('standalone','standalone-board'):
        baseline=ROOT/'docs/verification/standalone-ci'/f'{name}.json'
        current=ROOT/'reports'/f'{name}.json'
        for path in (baseline,current): inputs[str(path.relative_to(ROOT))]=digest(path)
        old,new=(json.loads(p.read_text()) for p in (baseline,current))
        if old['status']!='passed' or new['status']!='passed' or old['profile']!=new['profile']:
            raise ValueError('performance comparison needs passed runs with identical capacities')
        previous={case['name']:case for case in old['cases']}
        cases=[]
        for case in new['cases']:
            label=case['name']
            if label.startswith('reset-') or label not in previous: continue
            before=previous[label]
            if before['source_sha256']!=case['source_sha256'] or before['image_files']!=case['image_files']:
                raise ValueError('performance comparison changed the workload: '+label)
            a,b=before['frames'][0],case['frames'][0]
            for key in ('status','trap','values'):
                if a[key]!=b[key]: raise ValueError('performance comparison changed results: '+label)
            if b['status'] not in (0,1): continue
            entry={'name':label,'status':b['status'],'trap':b['trap'],
                   'old_execution_cycles':a['cycles'],'new_execution_cycles':b['cycles'],
                   'old_completion_clocks':a['simulation_clocks'],'new_completion_clocks':b['simulation_clocks']}
            if b['cycles']:
                entry['execution_speedup']=a['cycles']/b['cycles']
            if name=='standalone-board':
                entry['old_simulated_completion_ms']=a['simulation_clocks']/25000
                entry['new_simulated_completion_ms']=b['simulation_clocks']/25000
            cases.append(entry)
        if not cases: raise ValueError('no comparable measured workloads')
        results[name]=cases
    report={'status':'passed','baseline_commit':'4e8e696ff7d568e43d04e77c4a6088409ad8dfa0',
        'baseline_run':'https://github.com/Millillion/wasmetal/actions/runs/41572176563',
        'scope':'first boot of identical images; execution counter excludes clearing, boot replay and UART',
        'clock_units':{'standalone':'core cycles, accelerated test UART','standalone-board':'25 MHz oscillator cycles, board-rate UART'},
        'inputs':inputs,'comparisons':results,'physical_hardware_tested':False}
    (ROOT/'reports/standalone-performance.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Compared',sum(map(len,results.values())),'measured runs with identical images and results')


if __name__=='__main__':main()
