#!/usr/bin/env python3
"""Run and reconcile all six complete-system Xilinx partitions."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from check_xc7_system import require, validate_models
from loadable_ci import GROUPS, RECOVERY
from prepare_standalone import ROOT, digest
from standalone_support import verify_simulator


def check_shard(report, index, reference, mapped):
    require(report['status'] == 'passed' and report['model'] == mapped,
            'partition is incomplete or uses a different executable')
    require(report['inputs'] == reference['inputs'], 'partition checker inputs differ')
    expected_names = GROUPS[index]+(RECOVERY if index == 0 else [])
    require([case['name'] for case in report['cases']] == expected_names, 'partition case inventory differs')
    expected = {case['name']:case for case in reference['cases']}
    for case in report['cases']:
        require(case == expected.get(case['name']), 'partition differs from native observations: '+case['name'])


def check_destinations(inputs, outputs):
    protected = {p.resolve() for p in inputs}; targets = [p.resolve() for p in outputs]
    require(len(targets)==len(set(targets)), 'campaign outputs overlap')
    require(protected.isdisjoint(targets), 'campaign output would overwrite a verification input')


def require_artifact_path(path, root=ROOT):
    resolved = path.resolve()
    require(any(base == resolved or base in resolved.parents for base in (root/'build',root/'reports')),
            'campaign artifacts must stay within build/ or reports/')


def stop_workers(processes):
    # Each worker owns a new process group containing its simulator. Signal
    # only groups created by this runner, including descendants of a failed
    # checker, so interrupted tests cannot leave expensive orphan simulations.
    for process in processes:
        try:os.killpg(process.pid,signal.SIGINT)
        except ProcessLookupError:pass
    deadline = time.monotonic()+5
    while any(p.poll() is None for p in processes) and time.monotonic()<deadline:
        time.sleep(0.05)
    for process in processes:
        try:os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        process.wait(timeout=5)


def run_workers(commands, indices, logs, workers, completed):
    pending = list(indices); active = {}; finished = []
    require(workers > 0, 'worker count must be positive')
    logs.mkdir(parents=True,exist_ok=True)
    try:
        while pending or active:
            while pending and len(active)<workers:
                index = pending.pop(0); stream = (logs/f'{index}.log').open('w')
                try:
                    process = subprocess.Popen(commands[index],cwd=ROOT,stdout=stream,
                                               stderr=subprocess.STDOUT,start_new_session=True)
                except BaseException:
                    stream.close();raise
                active[index] = (process,stream)
                print('START partition',index,flush=True)
            progressed = False
            for index,(process,stream) in list(active.items()):
                code = process.poll()
                if code is None:continue
                require(code == 0, f'partition {index} exited {code}; see {logs / (str(index)+".log")}')
                completed(index)
                # A successful checker must also leave no descendants behind.
                stop_workers([process]);stream.close();del active[index]
                finished.append(index);progressed = True
                print('PASS partition',index,flush=True)
            if not progressed:time.sleep(0.1)
    finally:
        stop_workers([p for p,_ in active.values()])
        for _,stream in active.values():stream.close()
    return finished


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers',type=int,default=4)
    parser.add_argument('--resume',action='store_true',help='reuse verified complete partitions and run missing ones')
    parser.add_argument('--reference',type=Path,default=ROOT/'reports/loadable-rtl.json')
    parser.add_argument('--native-simulator',type=Path,default=ROOT/'build/loadable-sim/Vwasmetal_loadable')
    parser.add_argument('--mapped-simulator',type=Path,default=ROOT/'build/xc7-accelerated-gate-fast/obj/Vwasmetal_loadable')
    parser.add_argument('--reports',type=Path,default=ROOT/'reports/xc7-system-shards')
    parser.add_argument('--logs',type=Path,default=ROOT/'build/xc7-system-run')
    parser.add_argument('--output',type=Path,default=ROOT/'reports/xc7-system-complete.json')
    args = parser.parse_args()
    if not 1<=args.workers<=len(GROUPS):parser.error('workers must be between one and six')
    for field in ('reference','native_simulator','mapped_simulator','reports','logs','output'):
        path = getattr(args,field).resolve()
        if ROOT not in path.parents:parser.error(field+' must be inside this checkout')
        setattr(args,field,path)
    try:
        for path in (args.reports,args.logs,args.output):require_artifact_path(path)
    except ValueError as error:parser.error(str(error))
    args.reports.mkdir(parents=True,exist_ok=True);args.logs.mkdir(parents=True,exist_ok=True)
    consumed = [args.reference,Path(__file__).resolve(),ROOT/'tools/check_xc7_system.py',ROOT/'tools/check_loadable.py',
                ROOT/'tools/loadable_ci.py',ROOT/'tools/standalone_support.py',ROOT/'tools/prepare_standalone.py',
                ROOT/'tools/program_upload.py',Path(str(args.native_simulator)+'.build.json'),
                Path(str(args.mapped_simulator)+'.build.json')]
    protected = [*consumed,args.native_simulator,args.mapped_simulator]
    paths = [args.reports/f'loadable-mapped-{i}.json' for i in range(len(GROUPS))]
    plan_path = args.logs/'plan.json'
    outputs = [args.output,plan_path,plan_path.with_suffix('.json.tmp'),args.logs/'comparison.log',*paths,
               *[args.logs/f'{i}.log' for i in range(len(GROUPS))]]
    try:
        check_destinations(protected,outputs)
    except ValueError as error:parser.error(str(error))
    # Prepared packets are shared by backend/case within a checkout, so even
    # campaigns with distinct report directories must not run concurrently.
    (ROOT/'build').mkdir(exist_ok=True)
    with (ROOT/'build/.xc7-system-campaign.lock').open('a') as global_lock, (args.reports/'.run.lock').open('a') as lock:
        fcntl.flock(global_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        inputs = {str(p.relative_to(ROOT)):digest(p) for p in consumed}
        reference = json.loads(args.reference.read_text())
        native = verify_simulator(args.native_simulator);mapped = verify_simulator(args.mapped_simulator)
        # Include every transitive source/generated-model input before deleting
        # or opening any campaign output. Inputs may themselves live in build/.
        protected += [ROOT/name for model in (native,mapped,reference) for name in model['inputs']]
        check_destinations(protected,outputs)
        args.output.unlink(missing_ok=True)
        validate_models(reference,native,mapped)
        names = {n for group in GROUPS for n in group}|set(RECOVERY)
        require(len(reference['cases'])==len(names) and {c['name'] for c in reference['cases']}==names,
                'complete native reference required before starting workers')
        for name,value in reference['inputs'].items():
            path = Path(name)
            require(not path.is_absolute() and '..' not in path.parts and digest(ROOT/path)==value,
                    'native checker input changed: '+name)
            require(name not in inputs or inputs[name]==value,'conflicting checker identity')
            inputs[name]=value
        existing = set(args.reports.glob('loadable-mapped-*.json'))
        require(existing <= set(paths),'unexpected partition files in output directory')
        require(args.resume or not existing,'partition files already exist; use --resume to verify completed evidence')
        reused=[]
        for index,path in enumerate(paths):
            if path.exists():
                check_shard(json.loads(path.read_text()),index,reference,mapped)
                inputs[str(path.relative_to(ROOT))]=digest(path);reused.append(index)
        commands=[]
        for index,group in enumerate(GROUPS):
            command=[sys.executable,str(ROOT/'tools/check_loadable.py'),'--binary',str(args.mapped_simulator),'--report',str(paths[index])]
            for name in group:command+=['--case',name]
            if index:command+=['--no-recovery']
            commands.append(command)
        started=time.monotonic();finished=list(reused)
        plan={'status':'running','scope':'all 35 bounded programmable Xilinx integration cases',
              'models':{'rtl':native,'mapped':mapped},'inputs':inputs,'commands':commands,
              'worker_limit':args.workers,'reused_partitions':reused,'completed_partitions':finished,
              'physical_hardware_tested':False}
        def save(status):
            plan.update(status=status,elapsed_seconds=time.monotonic()-started)
            temporary=plan_path.with_suffix('.json.tmp');temporary.write_text(json.dumps(plan,indent=2)+'\n');temporary.replace(plan_path)
        def completed(index):
            check_shard(json.loads(paths[index].read_text()),index,reference,mapped)
            finished.append(index);save('running')
        def interrupted(number,frame):raise InterruptedError('campaign interrupted by signal '+str(number))
        previous=signal.signal(signal.SIGTERM,interrupted)
        save('running')
        try:
            run_workers(commands,[i for i in range(len(GROUPS)) if i not in reused],args.logs,args.workers,completed)
            require(verify_simulator(args.native_simulator)==native and verify_simulator(args.mapped_simulator)==mapped,
                    'simulator identity changed during campaign')
            for name,value in inputs.items():require(digest(ROOT/name)==value,'campaign input changed: '+name)
            save('verifying')
            command=[sys.executable,str(ROOT/'tools/check_xc7_system.py'),'--reference',str(args.reference),
                     '--reports',str(args.reports),'--native-simulator',str(args.native_simulator),
                     '--mapped-simulator',str(args.mapped_simulator),'--output',str(args.output)]
            with (args.logs/'comparison.log').open('w') as stream:
                subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT,check=True,timeout=600)
            result=json.loads(args.output.read_text())
            require(result['status']=='passed' and result['case_count']==35 and result['negative_controls_rejected']==15,
                    'incomplete final reconciliation')
            for name,value in inputs.items():require(digest(ROOT/name)==value,'campaign input changed during reconciliation: '+name)
            require(verify_simulator(args.native_simulator)==native and verify_simulator(args.mapped_simulator)==mapped,
                    'simulator changed during reconciliation')
            plan.update(result_sha256=digest(args.output),comparison_command=command)
            save('passed');print('PASS complete Xilinx campaign; 35 cases and 15 comparison controls',flush=True)
        except BaseException as error:
            args.output.unlink(missing_ok=True);plan['error']=repr(error)
            save('interrupted' if isinstance(error,(KeyboardInterrupt,InterruptedError)) else 'failed')
            raise
        finally:signal.signal(signal.SIGTERM,previous)


if __name__=='__main__':main()
