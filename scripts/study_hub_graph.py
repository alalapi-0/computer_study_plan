"""Detached LabManager facts -> SOURCE envelope containing exact Hub graph 1.0.

No LabManager/Hub import, business-file read, command, service or state mutation.
Only module import fingerprints this public code file; build_study_graph is pure.

Host integration (the host owns any explicitly authorized native observation):
  doc = native_document(catalog=detached_catalog, history=detached_history,
        environments={attempt_uuid: detached_snapshot['environment']},
        source01_version=source01_digest, native_code_sha256=lab_runtime_digest)
  ctx = make_context(doc, exporter_sha256=exact_exporter_digest,
        permission_version=trusted_permission_digest, minimum_revision=watermark)
  result = build_study_graph(doc, context=ctx, observed_at=aware_ISO_timestamp)

catalog has native {'scenarios': [...]} entries, including id/version/content_hash.
history has native {'revision': int, 'attempts': [...]} records. Environment is
LabManager._environment's detached dictionary, keyed externally by its Attempt.
The adapter selects native fields, strips inputs/output/workspace/check details,
and never calls snapshot/history/constructor (those may mutate native state).
Missing optional fields become null/unknown, never inferred success. The strict
sanitized document can also be supplied directly: see native_document's return.
The CLI stdin bundle is exactly {document, context, observed_at}; raw snapshots
with private fields are NOT accepted by build_study_graph or that CLI.

Context is an explicit trusted caller binding, not permission: exact schema,
project, helper/exporter/native-code/source01 digests, permission version, current
document digest and minimum native revision. Reusing old context cannot prove
freshness; hosts must supply their current digest/watermark. No internal ledger.
Logical locators identify detached native records, never prove a file exists.
Scenario package hashes are native declarations, not recomputed package checks.
"""
from __future__ import annotations

import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

PROJECT_ID = 'computer-study-plan'
DOCUMENT_SCHEMA = 'study-native-document/1'
CONTEXT_SCHEMA = 'study-graph-context/1'
DOMAIN_CONTRACT = 'study-domain-source/1.2.0'
GRAPH_SCHEMA = '1.0'
MAX_DOCUMENT_BYTES = 512 * 1024
MAX_OBJECTS = 2048
MAX_RECORDS = 128
MAX_CHECKS = 64
TYPES = frozenset({'Project', 'Goal', 'Phase', 'Round', 'Task', 'Artifact', 'FileRef', 'Workflow', 'Run', 'Service', 'Tool', 'Decision', 'Review'})
RELATIONS = frozenset({'managed_by', 'part_of', 'depends_on', 'blocks', 'consumes', 'produces', 'derived_from', 'references', 'related_to'})
EXPLANATIONS = frozenset({'purpose', 'outputs', 'current_work', 'next_action', 'actor'})
CODE_SHA256 = globals().get('_SOURCE_CODE_SHA256') or hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
SHA = re.compile(r'[0-9a-f]{64}\Z')
NATIVE_ID = re.compile(r'[a-z0-9][a-z0-9-]{0,79}\Z')
UUID = re.compile(r'[0-9a-f]{32}\Z')
SCENARIO_FIELDS = ('id', 'version', 'content_hash', 'title', 'environment')
ATTEMPT_FIELDS = ('id', 'scenario_id', 'scenario_version', 'scenario_hash', 'status', 'started_at',
                  'ended_at', 'end_reason', 'hints_viewed', 'solution_viewed', 'view_events', 'checks', 'tool_versions')
ENV_FIELDS = ('adapter', 'nodes', 'shell', 'required_tools', 'versions', 'network')
CHECK_FIELDS = ('at', 'status', 'passed')
CONTEXT_FIELDS = frozenset({'schema_version', 'project_id', 'document_schema', 'graph_schema', 'domain_contract',
                          'helper_sha256', 'exporter_sha256', 'native_code_sha256', 'source01_version',
                          'permission_version', 'document_sha256', 'minimum_revision'})


class GraphSourceError(ValueError):
    """Public constant error code; raw input/paths are never included."""


def need(ok, reason):
    if not ok:
        raise GraphSourceError(reason)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _bounded(value):
    """Bound object depth/shape before recursive serialization, reject cycles."""
    stack, count, size, containers = [(value, 0)], 0, 0, set()
    while stack:
        item, depth = stack.pop()
        count += 1
        need(depth <= 16 and count <= 40000, 'document_structure_limit')
        if type(item) in (dict, list):
            need(id(item) not in containers, 'aliased_or_cyclic_document')
            containers.add(id(item))
            if type(item) is dict:
                need(all(type(k) is str for k in item), 'non_string_key')
                for key, child in item.items():
                    size += len(key.encode('utf-8'))
                    stack.append((child, depth + 1))
            else:
                stack.extend((child, depth + 1) for child in item)
        elif type(item) is str:
            size += len(item.encode('utf-8'))
        else:
            need(item is None or type(item) in (bool, int), 'invalid_scalar_type')
            if type(item) is int:
                need(abs(item) <= 2**63 - 1, 'integer_limit')
        need(size <= MAX_DOCUMENT_BYTES, 'document_byte_limit')
    need(len(canonical(value)) <= MAX_DOCUMENT_BYTES, 'document_byte_limit')


def _exact(value, fields, reason='invalid_fields'):
    need(type(value) is dict and set(value) == set(fields), reason)


def _sha(value):
    need(type(value) is str and SHA.fullmatch(value) is not None, 'invalid_digest')
    return value


def _text(value, limit=512):
    need(type(value) is str and 0 < len(value) <= limit and not any(ord(c) < 32 or ord(c) == 127 for c in value), 'invalid_text')
    # No absolute/relative filesystem strings or URLs in free-form attributes.
    need('/' not in value and '\\' not in value and '~' not in value, 'private_path_text')
    return value


def _time(value):
    need(type(value) is str and len(value) <= 40, 'invalid_timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise GraphSourceError('invalid_timestamp') from None
    need(parsed.tzinfo is not None and parsed.utcoffset() is not None, 'timestamp_requires_timezone')
    return parsed


def _optional(value, checker):
    if value is not None:
        checker(value)


def _versions(value):
    if value is None:
        return
    need(type(value) is dict and set(value) <= {'bubblewrap', 'userland', 'python', 'bash', 'git', 'stat', 'architecture'}, 'invalid_tool_versions')
    for item in value.values():
        _text(item)


def _environment(value, scenario=False):
    if value is None:
        return
    _exact(value, ('adapter', 'nodes', 'shell', 'required_tools') if scenario else ENV_FIELDS, 'invalid_environment_fields')
    for key in ('adapter', 'shell'):
        _optional(value[key], lambda x: need(type(x) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', x), 'invalid_environment_identifier'))
    for key in ('nodes', 'required_tools'):
        if value[key] is not None:
            need(type(value[key]) is list and len(value[key]) <= 32, 'invalid_environment_list')
            need(len(value[key]) == len(set(value[key])), 'duplicate_environment_item')
            for item in value[key]:
                need(type(item) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', item), 'invalid_environment_item')
    if not scenario:
        _versions(value['versions'])
        need(value['network'] in (None, 'isolated'), 'invalid_network_fact')


def _pick(record, fields):
    need(type(record) is dict, 'native_record_not_object')
    return {key: copy.deepcopy(record.get(key)) for key in fields}


def native_document(*, catalog, history, environments, source01_version, native_code_sha256):
    """Filter already detached native dictionaries; no IO or native method calls.

    This adapter is the ONLY boundary accepting full native records. Strict graph
    input below contains native field names with null for absent observations.
    Checks retain ordinal/status/passed/at, not details/evidence/operation text.
    """
    _bounded({'catalog': catalog, 'history': history, 'environments': environments})
    need(type(catalog) is dict and type(history) is dict and type(environments) is dict, 'invalid_native_bundle')
    scenarios = catalog.get('scenarios')
    attempts = history.get('attempts')
    need(type(scenarios) is list and type(attempts) is list and len(scenarios) <= MAX_RECORDS and len(attempts) <= MAX_RECORDS, 'native_record_limit')
    clean_scenarios = []
    for item in scenarios:
        clean = _pick(item, SCENARIO_FIELDS)
        if clean['environment'] is not None:
            clean['environment'] = _pick(clean['environment'], ('adapter', 'nodes', 'shell', 'required_tools'))
        clean_scenarios.append(clean)
    clean_attempts = []
    for item in attempts:
        clean = _pick(item, ATTEMPT_FIELDS)
        if clean['checks'] is not None:
            need(type(clean['checks']) is list and len(clean['checks']) <= MAX_CHECKS, 'check_limit')
            clean['checks'] = [_pick(check, CHECK_FIELDS) for check in clean['checks']]
        if clean['view_events'] is not None:
            need(type(clean['view_events']) is list and len(clean['view_events']) <= 2, 'view_event_limit')
            clean['view_events'] = [_pick(event, ('kind', 'at')) for event in clean['view_events']]
        clean_attempts.append(clean)
    clean_env = [{'attempt_id': key, 'environment': _pick(value, ENV_FIELDS)} for key, value in environments.items()]
    body = {'schema_version': DOCUMENT_SCHEMA, 'project_id': PROJECT_ID, 'native_schema_version': 1,
            'source01_version': source01_version, 'native_code_sha256': native_code_sha256,
            'revision': history.get('revision'), 'scenarios': clean_scenarios,
            'attempts': clean_attempts, 'environments': clean_env}
    return {**body, 'content_sha256': digest(body)}


def make_context(document, *, exporter_sha256, permission_version, minimum_revision):
    """Convenience for a trusted host; does not grant permission or freshness."""
    return {'schema_version': CONTEXT_SCHEMA, 'project_id': PROJECT_ID, 'document_schema': DOCUMENT_SCHEMA,
            'graph_schema': GRAPH_SCHEMA, 'domain_contract': DOMAIN_CONTRACT, 'helper_sha256': CODE_SHA256,
            'exporter_sha256': exporter_sha256, 'native_code_sha256': document['native_code_sha256'],
            'source01_version': document['source01_version'], 'permission_version': permission_version,
            'document_sha256': document['content_sha256'], 'minimum_revision': minimum_revision}


def _validate(document, context):
    _bounded(document)
    _bounded(context)
    _exact(context, CONTEXT_FIELDS, 'invalid_context_fields')
    need((context['schema_version'], context['project_id'], context['document_schema'], context['graph_schema'], context['domain_contract']) ==
         (CONTEXT_SCHEMA, PROJECT_ID, DOCUMENT_SCHEMA, GRAPH_SCHEMA, DOMAIN_CONTRACT), 'wrong_context_contract')
    for key in ('helper_sha256', 'exporter_sha256', 'native_code_sha256', 'source01_version', 'permission_version', 'document_sha256'):
        _sha(context[key])
    need(context['helper_sha256'] == CODE_SHA256, 'wrong_helper_code')
    need(type(context['minimum_revision']) is int and context['minimum_revision'] >= 0, 'invalid_revision_watermark')
    _exact(document, {'schema_version', 'project_id', 'native_schema_version', 'source01_version', 'native_code_sha256',
                      'revision', 'scenarios', 'attempts', 'environments', 'content_sha256'}, 'invalid_document_fields')
    need((document['schema_version'], document['project_id'], document['native_schema_version']) == (DOCUMENT_SCHEMA, PROJECT_ID, 1)
         and type(document['native_schema_version']) is int, 'wrong_native_contract')
    need(type(document['revision']) is int and document['revision'] >= context['minimum_revision'], 'revision_downgrade_or_unknown')
    for key in ('source01_version', 'native_code_sha256'):
        need(document[key] == context[key], 'wrong_source_context')
    need(document['content_sha256'] == context['document_sha256'] == digest({k: v for k, v in document.items() if k != 'content_sha256'}), 'inconsistent_document_version')
    for key in ('scenarios', 'attempts', 'environments'):
        need(type(document[key]) is list and len(document[key]) <= MAX_RECORDS, 'record_limit')
    scenarios, attempts, envs = {}, {}, {}
    for item in document['scenarios']:
        _exact(item, SCENARIO_FIELDS, 'invalid_scenario_fields')
        need(type(item['id']) is str and NATIVE_ID.fullmatch(item['id']), 'invalid_scenario_id')
        _optional(item['version'], lambda v: need(type(v) is int and v > 0, 'invalid_scenario_version'))
        _optional(item['content_hash'], _sha)
        _optional(item['title'], _text)
        _environment(item['environment'], scenario=True)
        key = (item['id'], item['version'], item['content_hash'])
        need(key not in scenarios, 'duplicate_scenario_version')
        scenarios[key] = item
    for item in document['attempts']:
        _exact(item, ATTEMPT_FIELDS, 'invalid_attempt_fields')
        need(type(item['id']) is str and UUID.fullmatch(item['id']), 'invalid_attempt_id')
        need(item['id'] not in attempts, 'duplicate_attempt')
        _optional(item['scenario_id'], lambda v: need(type(v) is str and NATIVE_ID.fullmatch(v), 'invalid_scenario_reference'))
        _optional(item['scenario_version'], lambda v: need(type(v) is int and v > 0, 'invalid_scenario_version'))
        _optional(item['scenario_hash'], _sha)
        need(item['status'] in (None, 'active', 'stopped', 'lost', 'expired'), 'invalid_attempt_status')
        for key in ('started_at', 'ended_at'):
            _optional(item[key], _time)
        _optional(item['end_reason'], lambda v: need(v in {'user_stop', 'reset', 'replaced', 'manager_restart', 'process_missing', 'shell_exit', 'infrastructure_error', 'manager_close', 'output_limit', 'lifetime_limit', 'workspace_limit'}, 'invalid_end_reason'))
        if item['status'] == 'active':
            need(item['ended_at'] is None and item['end_reason'] is None, 'contradictory_active_lifecycle')
        if item['started_at'] is not None and item['ended_at'] is not None:
            need(_time(item['ended_at']) >= _time(item['started_at']), 'invalid_lifecycle_order')
        for key in ('hints_viewed', 'solution_viewed'):
            need(item[key] is None or type(item[key]) is bool, 'invalid_assistance_fact')
        events = item['view_events']
        if events is not None:
            need(type(events) is list and len(events) <= 2, 'invalid_view_events')
            seen = set()
            for event in events:
                _exact(event, ('kind', 'at'), 'invalid_view_event_fields')
                need(event['kind'] in {'hints', 'solution'} and event['kind'] not in seen, 'invalid_view_kind')
                seen.add(event['kind'])
                _optional(event['at'], _time)
                key = 'hints_viewed' if event['kind'] == 'hints' else 'solution_viewed'
                need(item[key] is not False, 'contradictory_assistance_fact')
        checks = item['checks']
        if checks is not None:
            need(type(checks) is list and len(checks) <= MAX_CHECKS, 'check_limit')
            for check in checks:
                _exact(check, CHECK_FIELDS, 'invalid_check_fields')
                _optional(check['at'], _time)
                need(check['status'] in (None, 'passed', 'failed', 'infra_error'), 'invalid_check_status')
                need(check['passed'] is None or type(check['passed']) is bool, 'invalid_check_passed')
                need(not (check['status'] == 'passed' and check['passed'] is False or check['status'] in ('failed', 'infra_error') and check['passed'] is True), 'contradictory_check_result')
        _versions(item['tool_versions'])
        attempts[item['id']] = item
    for item in document['environments']:
        _exact(item, ('attempt_id', 'environment'), 'invalid_environment_reference')
        need(type(item['attempt_id']) is str and UUID.fullmatch(item['attempt_id']), 'invalid_environment_attempt_id')
        need(item['attempt_id'] not in envs, 'duplicate_environment')
        _environment(item['environment'])
        envs[item['attempt_id']] = item['environment']
    return scenarios, attempts, envs


def _unknown(reason):
    return {'value': None, 'unknown_reason': reason}


def _cell(value, reason='Native field is absent.'):
    return _unknown(reason) if value is None else {'value': copy.deepcopy(value), 'unknown_reason': None}


def _explanations(source, domain):
    result = {key: {'state': 'unknown', 'value': None, 'source': None,
                    'unknown_reason': 'No native explanation is published for this object.'} for key in sorted(EXPLANATIONS)}
    result['purpose'] = {'state': 'known', 'value': domain + ' detached source facts; no learning acceptance inferred.',
                         'source': copy.deepcopy(source), 'unknown_reason': None}
    return result


def build_study_graph(document, *, context, observed_at):
    """Return {available, graph, source_version, context, issues, scope, error}.

    Invalid input returns unavailable with no graph/version. Valid but incomplete
    native facts return issues and unknown cells; unresolved references create no
    fictitious object/edge. Graph rows and hash match frozen Hub graph_records.
    Observation time is only graph.projected_at, excluded from source identity.
    """
    failure = {'available': False, 'graph': None, 'source_version': None, 'context': None,
               'issues': [], 'scope': 'local_source_engineering_only', 'error': None}
    try:
        _time(observed_at)
        scenarios, attempts, envs = _validate(document, context)
        source_version = digest({'document': document['content_sha256'], 'context': context, 'contract': DOMAIN_CONTRACT})
        objects, relations, issues = [], [], []
        object_ids, edge_ids = set(), set()
        def issue(code, locator):
            issues.append({'code': code, 'locator': locator})
        def source(locator, revision, when=None):
            return {'ref': locator, 'version': revision, 'sha256': revision, 'fact_time': when,
                    'collected_at': None, 'origin': 'source_fact', 'applicability': 'current',
                    'unknown_reason': None if when is not None else 'Native record has no fact timestamp.'}
        def obj(kind, native, domain, data, record, locator, when=None):
            need(kind in TYPES and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,255}', native), 'invalid_graph_id')
            revision = digest({'record': record, 'native_code': context['native_code_sha256'], 'domain_contract': DOMAIN_CONTRACT})
            identity = PROJECT_ID + '/' + kind + '/' + native
            need(identity not in object_ids and len(objects) < MAX_OBJECTS, 'duplicate_or_excess_objects')
            object_ids.add(identity)
            src = source(locator, revision, when)
            item = {'id': identity, 'project_id': PROJECT_ID, 'type': kind, 'native_id': native,
                    'revision': revision, 'label': domain + ' ' + native, 'identity': 'fact', 'source': src,
                    'data': {'domain_kind': domain, **data}, 'explanations': _explanations(src, domain)}
            objects.append(item)
            return item
        def edge(kind, a, b, locator):
            need(kind in RELATIONS, 'invalid_relation')
            native = kind + '.' + digest([a['id'], b['id']])
            need(native not in edge_ids, 'duplicate_relation')
            edge_ids.add(native)
            revision = digest([kind, a['revision'], b['revision']])
            relations.append({'id': PROJECT_ID + '/Relation/' + native, 'project_id': PROJECT_ID,
                              'native_id': native, 'revision': revision, 'type': kind,
                              'from': {'id': a['id'], 'revision': a['revision']},
                              'to': {'id': b['id'], 'revision': b['revision']},
                              'evidence': [locator], 'source': source(locator, revision),
                              'identity': 'fact', 'run_id': None})
        scenario_objects = {}
        for key, item in sorted(scenarios.items(), key=lambda pair: canonical(pair[0])):
            sid, version, content_hash = key
            locator = 'content/scenarios/' + sid + '/scenario.json'
            if version is None or content_hash is None:
                issue('scenario_version_unresolved', locator)
                continue
            native = 'scenario.' + sid + '.v' + str(version) + '.' + content_hash
            artifact = {key: _unknown('Scenario reference does not publish ' + key + '.')
                        for key in ('input_version', 'code_version', 'sha256', 'purpose', 'host', 'file_ref')}
            artifact.update(input_version=_cell(str(version)), code_version=_cell(context['native_code_sha256']),
                            sha256=_cell(content_hash), purpose=_cell('Versioned teaching scenario package'), file_ref=_cell(locator))
            scenario_objects[key] = obj('Artifact', native, 'ScenarioVersion',
                {'artifact': artifact, 'scenario_id': sid, 'scenario_version': version,
                 'package_hash_semantics': 'native_package_digest_not_recomputed', 'environment_spec': _cell(item['environment']),
                 'availability': _unknown('Reference does not prove current file existence or quality.')}, item, locator)
        for aid, item in sorted(attempts.items()):
            locator = 'attempts.json#attempts[id=' + aid + ']'
            checks = item['checks']
            attempt = obj('Run', aid, 'Attempt', {
                'native_uuid': aid, 'status': _cell(item['status']), 'started_at': _cell(item['started_at']),
                'ended_at': _cell(item['ended_at']), 'end_reason': _cell(item['end_reason']),
                'hints_viewed': _cell(item['hints_viewed']), 'solution_viewed': _cell(item['solution_viewed']),
                'view_events': _cell(item['view_events']), 'checks_known': checks is not None,
                'independent_mastery': _unknown('Check outcomes and assistance do not establish independent mastery.'),
                'learning_completion': _unknown('No user learning acceptance is inferred.'),
                'project_completion_inferred': False}, item, locator, item['ended_at'] or item['started_at'])
            scenario_key = (item['scenario_id'], item['scenario_version'], item['scenario_hash'])
            target = scenario_objects.get(scenario_key)
            if target is None:
                issue('scenario_reference_unresolved', locator + '.scenario_hash')
            else:
                edge('consumes', attempt, target, locator + '.scenario_hash')
            if aid not in envs or envs[aid] is None:
                issue('environment_unobserved', locator)
            else:
                environment = envs[aid]
                alive = False if item['status'] in ('stopped', 'lost', 'expired') else None
                env = obj('Service', 'environment.' + aid, 'Environment', {
                    'native_identity': 'derived_from_attempt_uuid; no separately persisted environment ID',
                    'attempt_uuid': aid, 'alive': _cell(alive, 'Native environment descriptor has no process liveness observation.'),
                    'attempt_status': _cell(item['status']),
                    **{key: _cell(environment[key]) for key in ENV_FIELDS}},
                    {'environment': environment, 'attempt_status': item['status'], 'ended_at': item['ended_at'], 'end_reason': item['end_reason']},
                    locator + '.environment', item['ended_at'])
                edge('references', attempt, env, locator + '.environment')
            if checks is None:
                issue('checks_unobserved', locator + '.checks')
            else:
                for ordinal, check in enumerate(checks):
                    check_locator = locator + '.checks[' + str(ordinal) + ']'
                    review = obj('Review', 'check.' + aid + '.' + str(ordinal), 'Check', {
                        'native_identity': 'derived_native_array_locator; not a persisted business ID',
                        'attempt_uuid': aid, 'ordinal': ordinal, 'status': _cell(check['status']),
                        'passed': _cell(check['passed']), 'at': _cell(check['at']),
                        'details': _unknown('Raw checker details and evidence are intentionally not exported.'),
                        'acceptance_inferred': False}, check, check_locator, check['at'])
                    edge('part_of', review, attempt, check_locator)
        for aid in sorted(set(envs) - set(attempts)):
            issue('environment_attempt_unresolved', 'attempts.json#attempts[id=' + aid + '].environment')
        graph = {'schema_version': GRAPH_SCHEMA, 'project_id': PROJECT_ID, 'source_version': source_version,
                 'projected_at': observed_at, 'objects': objects, 'relations': relations, 'layouts': [],
                 'read_only': True, 'compatibility': {'major': 1, 'minimum_reader': '1.0'}}
        graph['projection_version'] = digest({key: graph[key] for key in ('project_id', 'source_version', 'objects', 'relations')})
        graph['rows'] = [{'object_id': o['id'], 'revision': o['revision'], 'type': o['type'], 'label': o['label'],
                          'identity': o['identity'], 'source_version': o['source']['version'], 'projection_version': graph['projection_version']} for o in objects]
        graph['unknown_types'] = {kind: 'No authorized native object of this type is present in this detached document.'
                                  for kind in sorted(TYPES - {o['type'] for o in objects})}
        return {'available': True, 'graph': graph, 'source_version': source_version,
                'context': copy.deepcopy(context), 'issues': issues, 'scope': failure['scope'], 'error': None}
    except (GraphSourceError, ValueError, TypeError, KeyError, AttributeError, RecursionError, UnicodeError):
        # Public reasons are controlled constants; never echo malformed input.
        import sys
        exc = sys.exc_info()[1]
        failure['error'] = str(exc) if isinstance(exc, GraphSourceError) else 'invalid_native_document'
        return failure
