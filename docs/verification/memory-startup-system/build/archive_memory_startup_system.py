"""Capture complete CPU startup and fresh, identical-RTL reference evidence."""
from pathlib import Path
import gzip,json,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from prepare_standalone import digest
from standalone_support import verify_simulator
names=[f'{prefix}-{n}' for n in (1,3) for prefix in ('memory-startup-system','asic-sram-system')]
names += [f'memory-startup-system-{n}-reconciliation' for n in (1,3)]
names += ['memory-startup-system-3-negative']
reports={name:json.loads((ROOT/'reports'/f'{name}.json').read_text()) for name in names}
files={ROOT/'reports'/f'{name}.json' for name in names};files.add(Path(__file__).resolve())
verified={}
def verify(value):
    if isinstance(value,list):
        for item in value:verify(item)
    elif isinstance(value,dict):
        for key,item in value.items():
            if key=='inputs' and isinstance(item,dict):
                for name,sha in item.items():
                    if not isinstance(sha,str) or len(sha)!=64:continue
                    path=ROOT/name
                    if digest(path)!=sha:raise ValueError('changed startup-system input: '+name)
                    if name in verified and verified[name]!=sha:raise ValueError('conflicting startup-system input: '+name)
                    verified[name]=sha
                    if not name.startswith('.cache/'):files.add(path)
            verify(item)
for name,report in reports.items():
    if report['status']!='passed':raise ValueError('unfinished gate: '+name)
    verify(report)
    if name.endswith('-reconciliation'):
        if report['negative_controls_rejected']!=16 or report['check']['case_count']!=35:raise ValueError('incomplete reconciliation')
        continue
    negative=name.endswith('-negative')
    expected=0 if negative else 35
    if report['case_count']!=expected or report['corrupt_read_negative_control_rejected']!=negative:raise ValueError('wrong execution coverage')
    binary_label=name.removesuffix('-negative')+('-corrupt' if negative else '')
    binary=ROOT/'build'/binary_label/'Vwasmetal_loadable'
    if verify_simulator(binary)!=report['model']:raise ValueError('changed CPU model')
    observations=ROOT/'reports'/(name+'-observations.json')
    if digest(observations)!=report['observation_report_sha256']:raise ValueError('changed CPU observations')
    files.update([observations,Path(str(binary)+'.build.json'),binary.parent/'build.log',ROOT/'build'/name/'execution.log'])
    harness=binary.parent/'loadable.cpp'
    if harness.exists():files.add(harness)
for dirname in ('memory-startup-system-initial-rejected','memory-startup-system-deadline-rejected'):
    files.update(path for path in (ROOT/'build'/dirname).rglob('*') if path.is_file())
for name in ('memory-startup-runner-fixtures.log','startup-reconciliation-1.log','startup-reconciliation-3.log',
             'memory-startup-system-1-driver.log','memory-startup-system-3-driver.log',
             'memory-startup-system-negative-driver.log','startup-reference-1.log','startup-reference-3.log',
             'memory-startup-system-workflow-lint.log','run_startup_reference.py'):
    files.add(ROOT/'build'/name)
files.update([ROOT/'tests/startup_runner_test.py',ROOT/'.github/workflows/rtl.yml',ROOT/'third_party/hardfloat/COPYING.txt'])
if 'Ran 3 tests' not in (ROOT/'build/memory-startup-runner-fixtures.log').read_text() or 'OK' not in (ROOT/'build/memory-startup-runner-fixtures.log').read_text():raise ValueError('missing runner fixture result')
summary={'status':'passed','scope':'complete programmable CPU startup with behavioral SRAM; RTL simulation',
 'capacity_bytes':131072,'cases_per_latency':35,'read_latencies':[1,3],
 'startup_clocks_per_committed_image':{'1':2949121,'3':3604481},
 'unchanged_shared_inputs_per_pair':60,'same_uart_bytes_and_cpu_execution_cycles':True,
 'exact_wall_clock_predictions':True,'cpu_watchdog_cycles':10000000,
 'corrupt_read_boot_rejected':True,'reconciliation_faults_rejected':32,'runner_cleanup_fixtures_passed':3,
 'reference':'Fresh no-startup runs use the same current CPU RTL as each startup run.',
 'failed_trials':'Retained initial width-lint failure and old overall-deadline failure; neither counted as a pass.',
 'default_fpga_integration':False,'physical_hardware_tested':False,'foundry_macro_tested':False,
 'reports':{name:digest(ROOT/'reports'/f'{name}.json') for name in names},'verified_inputs':verified}
summary_path=ROOT/'reports/memory-startup-system-summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n');files.add(summary_path)
destination=ROOT/'docs/verification/memory-startup-system';destination.mkdir(parents=True,exist_ok=True);index=[]
for path in sorted(files):
    raw=path.read_bytes();compressed=len(raw)>262144;target=destination/path.relative_to(ROOT)
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=raw:raise ValueError('startup-system archive differs')
    index.append({'original_path':str(path.relative_to(ROOT)),'archive_path':str(target.relative_to(ROOT)),
                  'original_sha256':digest(path),'archive_sha256':digest(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
for name in names+['memory-startup-system-summary']:
    public=name.replace('asic-sram-system','memory-startup-system-reference')
    (ROOT/'docs/verification'/f'{public}.json').write_bytes((ROOT/'reports'/f'{name}.json').read_bytes())
for report in reports.values():verify(report)
print('PASS full-CPU startup archive:',len(index),'artifacts;',len(verified),'bound hashes;',sum((ROOT/r['archive_path']).stat().st_size for r in index),'bytes')
