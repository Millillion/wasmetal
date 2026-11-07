#!/usr/bin/env python3
"""Archive passing CI gate jobs and their artifacts with GitHub-verified digests."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = 'Millillion/wasmetal'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def api(path, *, raw=False):
    result = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', path],
                            check=True, capture_output=True)
    return result.stdout if raw else json.loads(result.stdout)


def paged(path, key):
    items, page = [], 1
    while True:
        batch = api(f'{path}?per_page=100&page={page}')[key]
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', type=int, required=True)
    parser.add_argument('--gate', action='append', required=True, help='job name that must have succeeded')
    parser.add_argument('--artifact', action='append', required=True, help='artifact name to download and verify')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--summary', type=Path, required=True)
    args = parser.parse_args()
    base = args.output_dir.resolve()
    if base.exists() and any(base.iterdir()):
        raise SystemExit(f'refusing to overwrite existing archive: {base}')
    args.summary.unlink(missing_ok=True)
    base.mkdir(parents=True, exist_ok=True)
    observed = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    run = api(f'repos/{REPOSITORY}/actions/runs/{args.run_id}')
    jobs = paged(f'repos/{REPOSITORY}/actions/runs/{args.run_id}/jobs', 'jobs')
    jobs_path = base/f'ci-{args.run_id}-jobs.json'
    jobs_path.write_text(json.dumps({'jobs': jobs}, indent=2)+'\n')

    gates = []
    for name in args.gate:
        matches = [j for j in jobs if j['name'] == name]
        if len(matches) != 1 or matches[0]['conclusion'] != 'success':
            raise SystemExit(f'gate did not pass exactly once: {name}')
        job = matches[0]
        (base/f'ci-job-{job["id"]}.log').write_bytes(api(f'repos/{REPOSITORY}/actions/jobs/{job["id"]}/logs', raw=True))
        gates.append({k: job[k] for k in ['name', 'id', 'html_url', 'conclusion', 'completed_at']})

    artifacts = {a['name']: a for a in paged(f'repos/{REPOSITORY}/actions/runs/{args.run_id}/artifacts', 'artifacts')}
    directory = base/f'ci-{args.run_id}-artifacts'
    directory.mkdir()
    for name in args.artifact:
        artifact = artifacts.get(name)
        if artifact is None or artifact['expired']:
            raise SystemExit(f'artifact unavailable: {name}')
        archive = directory/f'{name}.zip'
        archive.write_bytes(api(f'repos/{REPOSITORY}/actions/artifacts/{artifact["id"]}/zip', raw=True))
        if f'sha256:{digest(archive)}' != artifact['digest']:
            raise SystemExit(f'downloaded artifact does not match GitHub digest: {name}')
        with zipfile.ZipFile(archive) as stream:
            stream.extractall(directory/name)
        (directory/f'{name}-source.json').write_text(json.dumps(
            {'id': artifact['id'], 'name': name, 'bytes': archive.stat().st_size, 'sha256': digest(archive)}, indent=2)+'\n')

    files = sorted(p for p in base.rglob('*') if p.is_file())
    (base/'index.json').write_text(json.dumps({
        'artifacts': {str(p.relative_to(base)): {'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files},
        'downloaded_zip_digests_verified_against_github': True}, indent=2)+'\n')
    others = [{k: j[k] for k in ['name', 'status', 'conclusion', 'html_url']}
              for j in jobs if j['conclusion'] != 'success']
    summary = {'status': 'selected-gates-passed', 'repository': REPOSITORY, 'run_id': args.run_id,
               'head_sha': run['head_sha'], 'observed_at_utc': observed, 'gates': gates,
               'whole_workflow_passed': run['conclusion'] == 'success',
               'other_job_states_at_observation': others, 'physical_hardware_tested': False,
               'artifacts': len(args.artifact), 'archive': str(base.relative_to(ROOT)/'index.json')}
    args.summary.write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({'gates': len(gates), 'artifacts': len(args.artifact), 'summary': str(args.summary)}))


if __name__ == '__main__':
    main()
