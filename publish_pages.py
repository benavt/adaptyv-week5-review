"""One verified Pages deployment with bounded polling; never retry a POST.

Uses the same Pages API/OIDC payload as the pinned actions/deploy-pages source.
Its ten-minute polling cap cannot be extended through the timeout input.
"""
import json
import os
from collections import Counter
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

TERMINAL = {'deployment_failed', 'deployment_perms_error',
            'deployment_content_failed', 'deployment_cancelled', 'deployment_lost'}


def prevent_data_regression(current, proposed):
    """A UI-only release must not replace a newer completed-data snapshot."""
    if Counter(current['modelFiles'].values()) - Counter(proposed['modelFiles'].values()):
        raise ValueError('Publication would remove or replace live native models; reconcile newer data first')
    for key in ['candidates', 'APNovo', 'PCANN']:
        old = current.get('currentReview', {}).get(key, current.get('counts', {}).get(key, 0))
        new = proposed.get('currentReview', {}).get(key, proposed.get('counts', {}).get(key, 0))
        if new < old:
            raise ValueError('Publication would regress live ' + key + '; reconcile newer data first')


def deploy(api, oidc, artifact_id, version, receipt, *, clock=time.monotonic,
           sleep=time.sleep, timeout=1800):
    receipt = Path(receipt)
    assert re.fullmatch(r'[a-f0-9]{40}', version)
    assert str(artifact_id).isdigit() and int(artifact_id) > 0
    state = {'buildVersion': version, 'artifactId': int(artifact_id),
             'status': 'submission_intent', 'automaticPostRetries': 0}
    # An uncertain submission must be reconciled rather than repeated.
    with receipt.open('x') as f:
        json.dump(state, f, indent=2)
    response = api('POST', '/pages/deployments', {
        'artifact_id': int(artifact_id), 'pages_build_version': version,
        'oidc_token': oidc,
    })
    deployment_id = str(response.get('id') or version)
    assert re.fullmatch(r'[A-Za-z0-9_-]+', deployment_id)
    state.update(deploymentId=deployment_id, status='submitted')
    receipt.write_text(json.dumps(state, indent=2) + '\n')
    print('Pages deployment ID:', deployment_id, flush=True)
    start = clock()
    while clock() - start < timeout:
        status = api('GET', '/pages/deployments/' + deployment_id, None).get('status', '')
        state.update(status=status, elapsedSeconds=round(clock() - start))
        receipt.write_text(json.dumps(state, indent=2) + '\n')
        print('Pages status:', status or 'unknown', flush=True)
        if status == 'succeed':
            return state
        if status in TERMINAL:
            raise RuntimeError('Pages deployment ended: ' + status)
        sleep(30)
    # Retain the ID for reconciliation; do not cancel or create another request.
    raise TimeoutError('Pages polling ended; reconcile saved deployment ID before retrying')


def main():
    repo = os.environ['GITHUB_REPOSITORY']
    assert repo == 'benavt/adaptyv-week5-review'
    assert os.environ['GITHUB_REF'] == 'refs/heads/main'
    token = os.environ['GITHUB_TOKEN']
    artifact_id = os.environ['PAGES_ARTIFACT_ID']
    run = os.environ['GITHUB_RUN_ID']
    version = os.environ['GITHUB_SHA']
    assert run.isdigit()
    prefix = 'https://api.github.com/repos/' + repo

    def api(method, path, body):
        request = urllib.request.Request(prefix + path, method=method,
            headers={'Authorization': 'Bearer ' + token,
                     'Accept': 'application/vnd.github+json',
                     'Content-Type': 'application/json',
                     'X-GitHub-Api-Version': '2022-11-28'},
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            # Do not print a response body that could echo sensitive inputs.
            raise RuntimeError(f'Pages API {method} {path}: HTTP {error.code}') from None

    artifact = api('GET', '/actions/artifacts/' + artifact_id, None)
    assert artifact['name'] == 'github-pages' and not artifact['expired']
    assert artifact['workflow_run']['id'] == int(run)
    assert artifact['workflow_run']['head_sha'] == version
    assert 0 < artifact['size_in_bytes'] < 1024**3
    request = urllib.request.Request(
        'https://benavt.github.io/adaptyv-week5-review/publication-manifest.json?preflight=' + run,
        headers={'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, timeout=60) as response:
        raw = response.read(10 * 1024**2 + 1)
    assert len(raw) <= 10 * 1024**2
    current = json.loads(raw)
    proposed = json.loads(Path('published-site/publication-manifest.json').read_text())
    prevent_data_regression(current, proposed)
    request = urllib.request.Request(os.environ['ACTIONS_ID_TOKEN_REQUEST_URL'],
        headers={'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
    with urllib.request.urlopen(request, timeout=60) as response:
        oidc = json.load(response)['value']
    assert isinstance(oidc, str) and oidc
    state = deploy(api, oidc, artifact_id, version, 'pages-deployment-receipt.json')
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write('page_url=https://benavt.github.io/adaptyv-week5-review/\n')
    print(json.dumps(state))


if __name__ == '__main__':
    main()
