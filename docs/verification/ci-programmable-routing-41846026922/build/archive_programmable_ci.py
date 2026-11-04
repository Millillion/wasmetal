from pathlib import Path
import gzip,hashlib,json,re,zipfile
ROOT=Path(__file__).resolve().parent.parent
base=ROOT/'build/ci-programmable-routing-41846026922'
destination=ROOT/'docs/verification/ci-programmable-routing-41846026922'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta=json.loads((base/'job.json').read_text());job=meta['job']
if sha(base/'artifact.zip')!=meta['artifact_sha256']:raise ValueError('artifact digest differs from upload receipt')
with zipfile.ZipFile(base/'artifact.zip') as z:
    if len(z.namelist())!=4:raise ValueError('unexpected archive inventory')
    for name in z.namelist():
        if z.read(name)!=(base/name).read_bytes():raise ValueError('extracted log differs')
log=base/'build/loadable-ulx3s/routing.log'
iterations=[dict(zip(['iteration','wires','overused','overuse'],map(int,m))) for m in re.findall(r'iter=(\d+) wires=(\d+) overused=(\d+) overuse=(\d+)',log.read_text())]
if [r['iteration'] for r in iterations]!=list(range(1,23)):raise ValueError('incomplete iteration inventory')
report={'status':'incomplete','source':'GitHub Actions artifact with SHA-256 checked against the upload log',
'run_id':meta['run_id'],'head_sha':job['head_sha'],'job_id':job['id'],'job_url':job['html_url'],
'job_conclusion':job['conclusion'],'job_started_at':job['started_at'],'job_completed_at':job['completed_at'],
'workflow_job_budget_minutes':350,'artifact_id':meta['artifact_id'],'archive_sha256':meta['artifact_sha256'],
'artifact_url':'https://github.com/Millillion/wasmetal/actions/runs/41846026922/artifacts/13360844324',
'scope':'production programmable board router2 trial, distinct from the reset and descriptor fanout experiments',
'run_job_outcomes':meta['job_outcomes'],'top':'wasmetal_loadable_ulx3s',
'placed_resources':{'TRELLIS_COMB':61344,'TRELLIS_FF':6958,'DP16KD':192,'MULT18X18D':26},
'iterations':iterations,'best':min(iterations,key=lambda r:r['overused']),'last':iterations[-1],
'routing_completed':False,'timing_passed':False,'bitstream_round_trip_passed':False,'physical_hardware_tested':False,
'limit':'The 350-minute job timeout leaves routing incomplete. It does not prove the design cannot route.',
'raw_evidence_index':'docs/verification/ci-programmable-routing-41846026922/index.json'}
public=ROOT/'docs/verification/ci-programmable-routing-41846026922.json'
public.write_text(json.dumps(report,indent=2)+'\n')
files=[p for p in base.rglob('*') if p.is_file()]+[Path(__file__).resolve()]
index=[]
for source in sorted(files):
    relative=source.relative_to(ROOT);raw=source.read_bytes();compressed=len(raw)>262144
    target=destination/relative
    if compressed:target=Path(str(target)+'.gz')
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(gzip.compress(raw,mtime=0) if compressed else raw)
    if (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes())!=raw:raise ValueError('archive copy differs')
    index.append({'original_path':str(relative),'archive_path':str(target.relative_to(ROOT)),
    'original_sha256':sha(source),'archive_sha256':sha(target),'compressed':compressed})
(destination/'index.json').write_text(json.dumps(index,indent=2)+'\n')
print('PASS CI routing archive:',len(index),'artifacts;',len(iterations),'iterations;',report['best'],report['last'])
