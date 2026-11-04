#!/usr/bin/env python3
"""Compare downloaded SDRAM CI reports with the independently recorded local runs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:raise RuntimeError('CI evidence verification requires Python assertions')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,required=True,help='downloaded artifacts and GitHub jobs.json snapshot')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();base=args.directory.resolve()
    output=args.output.resolve();output.unlink(missing_ok=True)
    jobs_path=base/'jobs.json';metadata=json.loads(jobs_path.read_text())
    assert len(metadata['jobs'])==4 and all(j['conclusion']=='success' for j in metadata['jobs'])
    for job in metadata['jobs']:
        if job['name'].startswith('Complete CPU through SDRAM'):
            assert any(s['name']=='Execute compiled C and compare independent CRC results' and
                s['conclusion']=='success' for s in job['steps'])
    names=['sdram-mapped','sdram-proof','sdram-four-state',
        'sdram-system-25mhz-5000','sdram-system-100mhz-5000000',
        'sdram-system-25mhz-5000-read-corruption','sdram-system-100mhz-5000000-startup-bypass',
        'sdram-c-25mhz','sdram-c-100mhz-5000000']
    comparisons={};sources={};copies=[]
    for name in names:
        matches=list(base.rglob(name+'.json'));assert len(matches)==1,name
        path=matches[0];local_path=ROOT/'docs/verification'/(name+'.json')
        ci=json.loads(path.read_text());local=json.loads(local_path.read_text())
        assert ci['status']==local['status']=='passed',name
        def inputs(value):
            if isinstance(value,dict):
                for key,item in value.items():
                    if key=='inputs':
                        for source,sha in item.items():
                            if Path(source).is_absolute() or '..' in Path(source).parts:
                                raise ValueError('non-repository CI source path')
                            if not source.startswith('build/'):
                                assert digest(ROOT/source)==sha,source
                                sources[source]=sha
                    else:inputs(item)
            elif isinstance(value,list):
                for item in value:inputs(item)
        inputs(ci)
        compared=['passed status','source inputs']
        if name=='sdram-mapped':
            assert len(ci['profiles'])==len(local['profiles'])==6
            for a,b in zip(ci['profiles'],local['profiles']):
                assert a['name']==b['name'] and a['parameters']==b['parameters']
                for model in ('rtl','mapped'):
                    for key in ('results','negative_controls_rejected'):
                        assert a['tests'][model][key]==b['tests'][model][key],(name,a['name'],model,key)
            compared+=['all six profiles','all observations and cycles in both models','negative controls']
        elif name=='sdram-proof':
            for key,expected in [('configurations',6),('negative_controls',7)]:
                assert len(ci[key])==len(local[key])==expected
                for a,b in zip(ci[key],local[key]):
                    for field in ('profile','parameters','induction_depth','status'):
                        assert a[field]==b[field],(name,field)
            compared+=['all six proof configurations and depths','seven counterexamples']
        elif name=='sdram-four-state':
            assert ci['cases']==local['cases']==366
            assert {k:v['outcome'] for k,v in ci['checks'].items()}=={k:v['outcome'] for k,v in local['checks'].items()}
            compared+=['366 four-state cases','three rejected mutations']
        elif name.endswith(('read-corruption','startup-bypass')):
            expected='read-corruption' if name.endswith('read-corruption') else 'startup-bypass'
            assert ci['negative_control_rejected']==local['negative_control_rejected']==expected
            compared+=['integration negative control']
        elif name.startswith('sdram-system'):
            assert ci['case_count']==local['case_count']==35
            for key in ('device_parameters','device_coverage','device_runs'):
                assert ci[key]==local[key],(name,key)
            assert ci['observations']['cases']==local['observations']['cases'],name
            compared+=['all 35 observations including UART and cycles','complete device coverage']
        else:
            assert ci['wasm_sha256']==local['wasm_sha256']
            assert len(ci['cases'])==len(local['cases'])==5
            for a,b in zip(ci['cases'],local['cases']):
                # Image manifests also bind the preparation executable. Preserve
                # their distinct identities; compare the actual serialized upload.
                assert {k:v for k,v in a.items() if k!='image_manifest_sha256'}=={
                    k:v for k,v in b.items() if k!='image_manifest_sha256'},name
            assert ci['device_coverage']==local['device_coverage'],name
            compared+=['identical Wasm and upload packets','all five UART/results/cycles','complete device coverage']
        comparisons[name]={'ci_report_sha256':digest(path),'local_report_sha256':digest(local_path),'compared':compared}
        copies.append(path)
    output.parent.mkdir(parents=True,exist_ok=True)
    archive=output.parent/'ci-sdram';archive.mkdir(exist_ok=True)
    for path in copies:shutil.copyfile(path,archive/path.name)
    receipt={'status':'passed','github':metadata,'comparisons':comparisons,
        'verified_source_inputs':sources,'checker_sha256':digest(Path(__file__)),
        'github_snapshot_sha256':digest(jobs_path),
        'scope':'downloaded CI reports checked against local observations; no physical board test',
        'c_image_manifests':'Build-specific image-manifest identities are preserved separately; serialized upload hashes match.',
        'physical_hardware_tested':False}
    output.write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS all nine SDRAM CI reports, source inputs and local observation comparisons')


if __name__=='__main__':main()
