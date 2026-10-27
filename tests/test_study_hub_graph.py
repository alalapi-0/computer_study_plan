"""Synthetic detached native records; no LabManager, business data or Hub dependency."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

ENTRY = Path(__file__).resolve().parents[1] / 'scripts/study_hub_graph.py'
WHEN = '2026-01-01T01:00:00+00:00'
LATER = '2026-01-01T02:00:00+00:00'
AID = 'a' * 32
HASH = 'b' * 64


def load_graph():
    spec = importlib.util.spec_from_file_location('candidate_study_graph_test', ENTRY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native_fixture():
    # Keys match catalog(), history() and _environment(), including fields the
    # detached adapter must discard rather than expose in graph attributes.
    versions = {'bubblewrap': 'bubblewrap 0.11.1', 'python': '3.14.4', 'bash': 'GNU bash 5.3',
                'git': 'git version 2.53', 'stat': 'stat 0.10', 'architecture': 'x86_64', 'userland': 'Synthetic Linux'}
    scenario = {'id': 'repair-config', 'version': 1, 'content_hash': HASH, 'title': 'Repair the config',
                'summary': 'A deterministic userland repair', 'tags': ['shell'],
                'symptom': 'The configured value is wrong.', 'goal': 'Set it to good.',
                'constraints': ['Do not create forbidden.'],
                'environment': {'adapter': 'bwrap-userland', 'nodes': ['lab'], 'shell': 'bash', 'required_tools': ['bash', 'python3']},
                'provenance': {'kind': 'test'}, 'hints': [{'command': 'SYNTHETIC_PRIVATE_COMMAND'}],
                'solution': {'steps': [{'command': 'SYNTHETIC_PRIVATE_SOLUTION'}]},
                'playable': True, 'publication_status': 'validation_mode'}
    attempt = {'id': AID, 'scenario_id': 'repair-config', 'scenario_version': 1, 'scenario_hash': HASH,
               'status': 'active', 'started_at': WHEN, 'ended_at': None, 'end_reason': None,
               'hints_viewed': True, 'solution_viewed': False, 'view_events': [{'kind': 'hints', 'at': WHEN}],
               'checks': [{'at': WHEN, 'status': 'failed', 'passed': False, 'evidence': {'config': 'SYNTHETIC_PRIVATE_CHECK'},
                           'details': 'SYNTHETIC_PRIVATE_DETAILS', 'operation_id': 'check-before'},
                          {'at': WHEN, 'status': 'passed', 'passed': True, 'evidence': ['target checked'],
                           'details': 'SYNTHETIC_PRIVATE_DETAILS', 'operation_id': 'check-after'}],
               'inputs': [{'data': 'SYNTHETIC_PRIVATE_INPUT'}], 'tool_versions': copy.deepcopy(versions),
               'output': 'SYNTHETIC_PRIVATE_TERMINAL', 'output_base': 0, 'output_truncated': False,
               'workspace_name': AID}
    env = {'adapter': 'bwrap-userland', 'label': 'Rootless synthetic userland', 'nodes': ['lab'], 'shell': 'bash',
           'required_tools': ['bash', 'python3'], 'versions': copy.deepcopy(versions), 'network': 'isolated',
           'workspace': '/workspace', 'limits': {'lifetime_seconds': 1800, 'output_bytes': 524288}}
    return {'scenarios': [scenario]}, {'revision': 8, 'attempts': [attempt]}, {AID: env}


class StudyGraphTests(unittest.TestCase):
    def setUp(self):
        self.module = load_graph()
        self.assertEqual(Path(self.module.__file__), ENTRY)
        self.catalog, self.history, self.environments = native_fixture()

    def document(self):
        return self.module.native_document(catalog=self.catalog, history=self.history, environments=self.environments,
                                          source01_version='c' * 64, native_code_sha256='d' * 64)

    def context(self, document, minimum=0):
        return self.module.make_context(document, exporter_sha256='e' * 64, permission_version='f' * 64, minimum_revision=minimum)

    def project(self, document=None, context=None, when=WHEN):
        doc = self.document() if document is None else document
        return self.module.build_study_graph(doc, context=self.context(doc) if context is None else context, observed_at=when)

    def valid(self):
        result = self.project()
        self.assertTrue(result['available'], result['error'])
        return result

    def test_native_four_classes_links_assistance_failed_and_passed(self):
        result = self.valid()
        graph = result['graph']
        kinds = {obj['data']['domain_kind'] for obj in graph['objects']}
        self.assertEqual(kinds, {'ScenarioVersion', 'Attempt', 'Environment', 'Check'})
        by_kind = {obj['data']['domain_kind']: obj for obj in graph['objects']}
        self.assertEqual(by_kind['Attempt']['native_id'], AID)
        self.assertTrue(by_kind['Attempt']['data']['hints_viewed']['value'])
        self.assertFalse(by_kind['Attempt']['data']['solution_viewed']['value'])
        self.assertIsNone(by_kind['Attempt']['data']['independent_mastery']['value'])
        self.assertIsNone(by_kind['Environment']['data']['alive']['value'])
        checks = [o for o in graph['objects'] if o['data']['domain_kind'] == 'Check']
        self.assertEqual([o['data']['status']['value'] for o in checks], ['failed', 'passed'])
        self.assertEqual([o['data']['passed']['value'] for o in checks], [False, True])
        self.assertEqual([o['native_id'] for o in checks], ['check.' + AID + '.0', 'check.' + AID + '.1'])
        objects = {(o['id'], o['revision']) for o in graph['objects']}
        for edge in graph['relations']:
            self.assertIn((edge['from']['id'], edge['from']['revision']), objects)
            self.assertIn((edge['to']['id'], edge['to']['revision']), objects)
        self.assertEqual({e['type'] for e in graph['relations']}, {'consumes', 'references', 'part_of'})

    def test_exact_hub_graph_shape_artifact_explanations_rows_and_hash(self):
        graph = self.valid()['graph']
        self.assertEqual(set(graph), {'schema_version', 'project_id', 'source_version', 'projection_version', 'projected_at',
                                     'objects', 'relations', 'layouts', 'rows', 'unknown_types', 'read_only', 'compatibility'})
        self.assertEqual(graph['schema_version'], '1.0')
        self.assertEqual(graph['compatibility'], {'major': 1, 'minimum_reader': '1.0'})
        self.assertEqual(graph['projection_version'], self.module.digest({k: graph[k] for k in ('project_id', 'source_version', 'objects', 'relations')}))
        expected_rows = [{'object_id': o['id'], 'revision': o['revision'], 'type': o['type'], 'label': o['label'],
                          'identity': o['identity'], 'source_version': o['source']['version'],
                          'projection_version': graph['projection_version']} for o in graph['objects']]
        self.assertEqual(graph['rows'], expected_rows)
        self.assertEqual(set(graph['unknown_types']), self.module.TYPES - {o['type'] for o in graph['objects']})
        for obj in graph['objects']:
            self.assertEqual(set(obj), {'id', 'project_id', 'type', 'native_id', 'revision', 'label', 'identity', 'source', 'data', 'explanations'})
            self.assertEqual(set(obj['explanations']), self.module.EXPLANATIONS)
            self.assertEqual(set(obj['source']), {'ref', 'version', 'sha256', 'fact_time', 'collected_at', 'origin', 'applicability', 'unknown_reason'})
            self.assertEqual(obj['id'], 'computer-study-plan/' + obj['type'] + '/' + obj['native_id'])
            if obj['type'] == 'Artifact':
                self.assertEqual(set(obj['data']['artifact']), {'input_version', 'code_version', 'sha256', 'purpose', 'host', 'file_ref'})
                self.assertIsNone(obj['data']['artifact']['host']['value'])
        for edge in graph['relations']:
            self.assertEqual(set(edge), {'id', 'project_id', 'native_id', 'revision', 'type', 'from', 'to', 'evidence', 'source', 'identity', 'run_id'})

    def test_builder_is_pure_and_drops_all_raw_private_fields(self):
        document = self.document()
        original = copy.deepcopy(document)
        with mock.patch('builtins.open', side_effect=AssertionError('no IO')):
            result = self.project(document)
        self.assertTrue(result['available'])
        self.assertEqual(document, original)
        serialized = json.dumps(result)
        for forbidden in ('SYNTHETIC_PRIVATE', '/workspace', 'workspace_name', 'operation_id', 'commands', 'PID', 'token'):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn('inputs', document['attempts'][0])
        self.assertEqual(set(document['attempts'][0]['checks'][0]), {'at', 'status', 'passed'})

    def test_stopped_expired_and_restart_lost_never_resurrect(self):
        for status, reason in (('stopped', 'user_stop'), ('expired', 'lifetime_limit'), ('lost', 'manager_restart')):
            with self.subTest(status=status):
                attempt = self.history['attempts'][0]
                attempt.update(status=status, ended_at=LATER, end_reason=reason)
                result = self.valid()
                run = next(o for o in result['graph']['objects'] if o['type'] == 'Run')
                env = next(o for o in result['graph']['objects'] if o['type'] == 'Service')
                self.assertEqual(run['native_id'], AID)
                self.assertEqual(run['data']['status']['value'], status)
                self.assertFalse(env['data']['alive']['value'])
                self.assertIsNone(run['data']['learning_completion']['value'])

    def test_missing_fields_and_references_are_unresolved_not_success(self):
        del self.history['attempts'][0]['hints_viewed']
        del self.history['attempts'][0]['checks']
        self.catalog['scenarios'] = []
        self.environments = {}
        result = self.valid()
        self.assertEqual([o['type'] for o in result['graph']['objects']], ['Run'])
        self.assertEqual(result['graph']['relations'], [])
        self.assertEqual({i['code'] for i in result['issues']}, {'scenario_reference_unresolved', 'environment_unobserved', 'checks_unobserved'})
        run = result['graph']['objects'][0]
        self.assertIsNone(run['data']['hints_viewed']['value'])
        self.assertFalse(run['data']['checks_known'])

    def test_unknown_scenario_version_and_orphan_environment_no_invented_nodes(self):
        del self.catalog['scenarios'][0]['content_hash']
        self.environments['f' * 32] = copy.deepcopy(self.environments[AID])
        result = self.valid()
        self.assertIn('scenario_version_unresolved', {i['code'] for i in result['issues']})
        self.assertIn('environment_attempt_unresolved', {i['code'] for i in result['issues']})
        self.assertFalse(any(o['type'] == 'Artifact' for o in result['graph']['objects']))
        self.assertEqual(len([o for o in result['graph']['objects'] if o['type'] == 'Service']), 1)

    def test_bad_ids_paths_duplicates_and_private_stdin_fields_fail(self):
        for container, key, value in ((self.catalog['scenarios'][0], 'id', '../escape'),
                                      (self.history['attempts'][0], 'id', '/private/id'),
                                      (self.catalog['scenarios'][0], 'title', '/home/private'),
                                      (self.history['attempts'][0], 'scenario_hash', 'invalid')):
            old = container[key]
            container[key] = value
            self.assertFalse(self.project()['available'])
            container[key] = old
        self.history['attempts'].append(copy.deepcopy(self.history['attempts'][0]))
        self.assertFalse(self.project()['available'])
        self.history['attempts'].pop()
        self.catalog['scenarios'].append(copy.deepcopy(self.catalog['scenarios'][0]))
        self.assertFalse(self.project()['available'])
        self.catalog['scenarios'].pop()
        doc = self.document()
        doc['attempts'][0]['inputs'] = []
        doc['content_sha256'] = self.module.digest({k: v for k, v in doc.items() if k != 'content_sha256'})
        self.assertFalse(self.project(doc)['available'])

    def test_same_snapshot_time_replay_stable_changed_history_and_package_versions(self):
        first = self.valid()
        replay = self.project(when=LATER)
        self.assertEqual(first['source_version'], replay['source_version'])
        self.assertEqual(first['graph']['projection_version'], replay['graph']['projection_version'])
        self.history['revision'] += 1
        attempt = self.history['attempts'][0]
        attempt['solution_viewed'] = True
        attempt['view_events'].append({'kind': 'solution', 'at': LATER})
        second = self.valid()
        self.assertNotEqual(first['source_version'], second['source_version'])
        ids1 = [o['id'] for o in first['graph']['objects']]
        self.assertEqual(ids1, [o['id'] for o in second['graph']['objects']])
        self.catalog['scenarios'][0].update(version=2, content_hash='1' * 64)
        changed = self.valid()
        self.assertNotEqual(first['source_version'], changed['source_version'])
        self.assertIn('scenario_reference_unresolved', {i['code'] for i in changed['issues']})
        self.assertNotEqual(next(o['id'] for o in first['graph']['objects'] if o['type'] == 'Artifact'),
                            next(o['id'] for o in changed['graph']['objects'] if o['type'] == 'Artifact'))

    def test_content_context_code_contract_permission_and_revision_bindings(self):
        doc = self.document()
        ctx = self.context(doc)
        for key, value in (('helper_sha256', '0' * 64), ('source01_version', '0' * 64),
                           ('native_code_sha256', '0' * 64), ('document_sha256', '0' * 64),
                           ('graph_schema', '2.0'), ('project_id', 'other'), ('minimum_revision', 9)):
            altered = {**ctx, key: value}
            self.assertFalse(self.project(doc, altered)['available'])
        old = self.project(doc, ctx)
        changed_permission = self.project(doc, {**ctx, 'permission_version': '0' * 64})
        self.assertTrue(changed_permission['available'])
        self.assertNotEqual(old['source_version'], changed_permission['source_version'])
        doc['revision'] -= 1
        self.assertFalse(self.project(doc, ctx)['available'])
        doc['content_sha256'] = self.module.digest({k: v for k, v in doc.items() if k != 'content_sha256'})
        self.assertFalse(self.project(doc, self.context(doc, minimum=8))['available'])

    def test_limits_invalid_shapes_contradictions_and_no_old_course_inference(self):
        self.history['attempts'][0]['checks'] *= 33
        with self.assertRaises(self.module.GraphSourceError):
            self.document()
        self.history['attempts'][0]['checks'] = [{'at': WHEN, 'status': 'failed', 'passed': True}]
        self.assertFalse(self.project()['available'])
        self.history['attempts'][0]['checks'] = []
        self.history['attempts'][0]['ended_at'] = LATER
        self.assertFalse(self.project()['available'])
        self.history = {'revision': 0, 'attempts': [], 'done': 80, 'total': 80}
        self.catalog = {'scenarios': []}
        self.environments = {}
        result = self.valid()
        self.assertEqual(result['graph']['objects'], [])
        self.assertNotIn('Mastery', json.dumps(result))
        doc = self.document()
        doc['extra'] = 'x' * (self.module.MAX_DOCUMENT_BYTES + 1)
        self.assertFalse(self.project(doc)['available'])


if __name__ == '__main__':
    unittest.main()
