#!/usr/bin/env python3
"""Prepare and run a repeatable serial acceptance campaign for a programmed board."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import time

from check_loadable import extra_cases,parse_frames
from check_standalone import cases,check_expected
from loadable_ci import RECOVERY
from prepare_standalone import ROOT,prepare,digest,load_profile
from program_upload import encode,profile_tag
from standalone_support import verify_image
from upload_program import transfer


INPUTS=('tools/board_acceptance.py','tools/check_loadable.py','tools/check_standalone.py',
        'tools/loadable_ci.py','tools/prepare_standalone.py','tools/standalone_support.py',
        'tools/program_upload.py','tools/upload_program.py','tools/read_standalone.py')


def catalog():
    return [case for case in cases() if not any(key in case for key in ('reset_at','reset_phase','corrupt'))]+list(extra_cases())


def local_path(directory,name):
    path=(directory/name).resolve()
    if not path.is_relative_to(directory.resolve()):raise ValueError('acceptance artifact escapes its directory')
    return path


def current_inputs():
    return {name:digest(ROOT/name) for name in INPUTS}


def check_reference(reference):
    model=reference['model'];profile=load_profile()
    if reference['status']!='passed' or model['backend']!='loadable-rtl' or model['profile']!=profile:
        raise ValueError('passed native programmable reference for this profile required')
    expected={case['name'] for case in catalog()}|set(RECOVERY)
    records={case['name']:case for case in reference['cases']}
    if len(records)!=len(reference['cases']) or set(records)!=expected:
        raise ValueError('native reference is incomplete or duplicated')
    if not {'tools/check_loadable.py','tools/check_standalone.py','tests/standalone/loadable.cpp'}<=reference['inputs'].keys():
        raise ValueError('native checker provenance is incomplete')
    required={'rtl/wasmetal_core.sv','soc/wasmetal_standalone.sv','soc/loader/wasmetal_loadable.sv',
              'tools/build_loadable_sim.py','soc/profile.json'}
    if not required<=model['inputs'].keys():raise ValueError('native circuit provenance is incomplete')
    for inputs in (reference['inputs'],model['inputs']):
        for name,value in inputs.items():
            path=Path(name)
            if path.is_absolute() or '..' in path.parts:raise ValueError('unsafe native reference input')
            # A completed CI receipt can be used without its compiled executable.
            # Its source inputs must still match this checkout.
            if not name.startswith('build/') and digest(ROOT/path)!=value:
                raise ValueError('stale native reference input: '+name)
    for case in catalog():
        record=records[case['name']];frame=record['result']
        check_expected(frame,case['expected'],case.get('status',0),case.get('trap',0))
        if type(frame['cycles']) is not int or not 0<frame['cycles']<=profile['watchdog_cycles']:
            raise ValueError('invalid reference execution cycle count')
        replies,frames=parse_frames(record['uart']['uart'])
        if [r['status'] for r in replies]!=['ready','committed'] or frames!=[frame]:
            raise ValueError('reference does not contain a complete upload and execution')
        if replies[0]['nonce']!=replies[1]['nonce']:raise ValueError('reference upload nonce changed')
    return records


def prepare_plan(directory,reference_path):
    directory=directory.resolve();reference_path=reference_path.resolve()
    directory.mkdir(parents=True,exist_ok=True);plan_path=directory/'plan.json'
    plan_path.unlink(missing_ok=True)
    reference=json.loads(reference_path.read_text());records=check_reference(reference)
    inputs=current_inputs();reference_sha=digest(reference_path);entries=[]
    for case in catalog():
        work=directory/'images'/case['name'];work.mkdir(parents=True,exist_ok=True)
        source=case.get('source',work/'source.wat')
        if 'wat' in case:source.write_text(case['wat'])
        image=work/'image';prepare(source,image,arguments=case.get('args',[]))
        record=records[case['name']];replies,_=parse_frames(record['uart']['uart'])
        upload=encode(image,replies[0]['nonce'])
        if hashlib.sha256(upload.bytes()).hexdigest()!=record['packet_sha256']:
            raise ValueError('prepared program differs from executed native image: '+case['name'])
        entries.append({'name':case['name'],'image':str(image.relative_to(directory)),
            'manifest_sha256':digest(image/'manifest.json'),'expected':record['result']})
    if digest(reference_path)!=reference_sha or current_inputs()!=inputs:
        raise ValueError('acceptance preparation inputs changed')
    if reference_path!=(directory/'native-reference.json').resolve():
        shutil.copyfile(reference_path,directory/'native-reference.json')
    plan={'format':'wasmetal-board-acceptance-v1','profile':load_profile(),
        'profile_tag':profile_tag(load_profile()).hex(),'inputs':inputs,
        'reference_sha256':reference_sha,'cases':entries,'physical_hardware_tested':False}
    plan_path.write_text(json.dumps(plan,indent=2)+'\n');verify_plan(plan_path)
    return plan_path


def verify_plan(path):
    path=path.resolve();directory=path.parent;plan=json.loads(path.read_text())
    if plan['format']!='wasmetal-board-acceptance-v1' or plan['profile']!=load_profile() or plan['profile_tag']!=profile_tag(load_profile()).hex():
        raise ValueError('wrong acceptance plan format or hardware profile')
    if plan['inputs']!=current_inputs():raise ValueError('acceptance tools changed; prepare a fresh plan')
    reference=directory/'native-reference.json'
    if digest(reference)!=plan['reference_sha256']:raise ValueError('native acceptance reference changed')
    records=check_reference(json.loads(reference.read_text()))
    if [item['name'] for item in plan['cases']]!=[case['name'] for case in catalog()]:
        raise ValueError('acceptance program coverage is incomplete, reordered or duplicated')
    for item in plan['cases']:
        image=local_path(directory,item['image']);verify_image(image)
        if digest(image/'manifest.json')!=item['manifest_sha256']:raise ValueError('acceptance image manifest changed')
        record=records[item['name']]
        if item['expected']!=record['result']:raise ValueError('acceptance expectation differs from native execution')
        replies,_=parse_frames(record['uart']['uart']);upload=encode(image,replies[0]['nonce'])
        if hashlib.sha256(upload.bytes()).hexdigest()!=record['packet_sha256']:
            raise ValueError('acceptance image differs from native execution')
    return plan


def verify_bitstream(path,profile):
    path=path.resolve();manifest=json.loads(path.read_text());bitstream=path.parent/'wasmetal.bit'
    if manifest['top']!='wasmetal_loadable_ulx3s' or manifest['profile']!=profile or manifest['profile_tag']!=profile_tag(profile).hex():
        raise ValueError('wrong programmable board bitstream')
    if not manifest.get('bitstream_round_trip_passed') or digest(bitstream)!=manifest['artifacts']['wasmetal.bit']:
        raise ValueError('unverified or changed board bitstream')
    required={'tools/upstream.lock.json','soc/profile.json','soc/loader/ulx3s.lpf',
              'soc/loader/wasmetal_loadable.sv','soc/loader/wasmetal_loadable_ulx3s.sv'}
    if not required<=manifest['inputs'].keys():raise ValueError('bitstream source provenance is incomplete')
    for name,value in manifest['inputs'].items():
        file=Path(name)
        if file.is_absolute() or '..' in file.parts:raise ValueError('unsafe bitstream input path')
        if not name.startswith('build/') and digest(ROOT/file)!=value:raise ValueError('stale bitstream source: '+name)
    return {'manifest_sha256':digest(path),'bitstream_sha256':digest(bitstream),
            'board':manifest['board'],'read_back_from_device':False}


def run_plan(path,device,report_path,*,repetitions=2,timeout=120,bitstream_manifest=None,hardware=False,label=''):
    if type(repetitions) is not int or repetitions<1:raise ValueError('repetitions must be a positive integer')
    if not math.isfinite(timeout) or timeout<=0:raise ValueError('timeout must be finite and positive')
    if hardware and (not label or bitstream_manifest is None or os.path.realpath(device).startswith('/dev/pts/')):
        raise ValueError('hardware runs require a board label, verified bitstream manifest and physical serial device')
    path=path.resolve();plan=verify_plan(path);plan_sha=digest(path)
    intended=verify_bitstream(bitstream_manifest,plan['profile']) if bitstream_manifest is not None else None
    report_path=report_path.resolve();report_path.parent.mkdir(parents=True,exist_ok=True)
    # Never overwrite an input artifact while saving progress.
    if report_path.is_relative_to(path.parent):raise ValueError('keep the run report outside the prepared plan directory')
    if bitstream_manifest is not None and report_path.is_relative_to(bitstream_manifest.resolve().parent):
        raise ValueError('keep the run report outside the bitstream artifact directory')
    started=time.monotonic();report={'status':'running','scope':f'{len(plan["cases"])} prepared programs over serial; not the official corpus',
        'device':os.path.realpath(device),'board_label':label,'hardware_asserted_by_operator':hardware,
        'physical_hardware_tested':hardware,'intended_bitstream':intended,'plan_sha256':plan_sha,
        'reference_sha256':plan['reference_sha256'],'repetitions':repetitions,'cases':[],
        'inputs':current_inputs(),'elapsed_seconds':0,'active_case':None}
    def save(status):
        report['status']=status;report['elapsed_seconds']=time.monotonic()-started
        temporary=report_path.with_suffix(report_path.suffix+'.tmp')
        temporary.write_text(json.dumps(report,indent=2)+'\n');temporary.replace(report_path)
    save('running')
    try:
        for repetition in range(repetitions):
            for item in plan['cases']:
                report['active_case']={'repetition':repetition+1,'name':item['name']};save('running')
                upload=encode(local_path(path.parent,item['image']));then=time.monotonic()
                result=transfer(upload,device,timeout)
                observed={'repetition':repetition+1,'name':item['name'],'transfer':result,
                    'elapsed_seconds':time.monotonic()-then,'matches_reference':False}
                report['cases'].append(observed)
                expected=item['expected'];frame=result['result']
                check_expected(frame,expected['values'],expected['status'],expected['trap'])
                if frame['cycles']!=expected['cycles']:raise ValueError('execution cycle count differs from native reference: '+item['name'])
                observed['matches_reference']=True;save('running')
                print(f'PASS serial {repetition+1}/{repetitions}: {item["name"]}',flush=True)
        if digest(path)!=plan_sha or verify_plan(path)!=plan:raise ValueError('acceptance plan changed during execution')
        if bitstream_manifest is not None and verify_bitstream(bitstream_manifest,plan['profile'])!=intended:
            raise ValueError('intended board bitstream changed during execution')
        report['active_case']=None;save('passed');return report
    except BaseException as error:
        report['error']=f'{type(error).__name__}: {error}';save('failed');raise


def main():
    parser=argparse.ArgumentParser(description=__doc__);commands=parser.add_subparsers(dest='action',required=True)
    prepare_args=commands.add_parser('prepare')
    prepare_args.add_argument('--output',type=Path,default=ROOT/'build/board-acceptance')
    prepare_args.add_argument('--reference',type=Path,default=ROOT/'reports/loadable-rtl.json')
    prepare_args.add_argument('--report',type=Path,default=ROOT/'reports/board-acceptance-preparation.json')
    run=commands.add_parser('run');run.add_argument('--plan',type=Path,default=ROOT/'build/board-acceptance/plan.json')
    run.add_argument('--device',required=True);run.add_argument('--report',type=Path,required=True)
    run.add_argument('--repetitions',type=int,default=2);run.add_argument('--timeout',type=float,default=120)
    run.add_argument('--bitstream-manifest',type=Path);run.add_argument('--hardware',action='store_true')
    run.add_argument('--board-label',default='')
    args=parser.parse_args()
    if args.action=='prepare':
        if args.report.resolve().is_relative_to(args.output.resolve()):parser.error('keep the preparation report outside the plan directory')
        args.report.unlink(missing_ok=True)
        path=prepare_plan(args.output,args.reference);plan=verify_plan(path)
        receipt={'status':'passed','scope':'prepared upload packets match the completed native execution reference',
            'case_count':len(plan['cases']),'cases':[item['name'] for item in plan['cases']],
            'plan_sha256':digest(path),'reference_sha256':plan['reference_sha256'],
            'inputs':plan['inputs'],'physical_hardware_tested':False}
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(receipt,indent=2)+'\n');print(path);return
    run_plan(args.plan,args.device,args.report,repetitions=args.repetitions,timeout=args.timeout,
        bitstream_manifest=args.bitstream_manifest,hardware=args.hardware,label=args.board_label)


if __name__=='__main__':main()
