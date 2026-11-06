import json
from pathlib import Path
import tempfile
import unittest
from publish_pages import deploy, prevent_data_regression


class PagesSubmission(unittest.TestCase):
    def test_new_data_superset_and_same_data_UI_update_are_allowed(self):
        current = {'modelFiles': {'old': 'a'}, 'currentReview': {'candidates': 1, 'PCANN': 1}}
        prevent_data_regression(current, current)
        prevent_data_regression(current, {'modelFiles': {'renamed': 'a', 'new': 'b'}, 'currentReview': {'candidates': 2, 'PCANN': 2}})

    def test_stale_UI_release_cannot_drop_models_or_completed_estimates(self):
        current = {'modelFiles': {'old': 'a', 'new': 'b'}, 'currentReview': {'candidates': 2, 'PCANN': 2}}
        with self.assertRaisesRegex(ValueError, 'native models'):
            prevent_data_regression(current, {'modelFiles': {'old': 'a'}, 'currentReview': {'candidates': 2, 'PCANN': 2}})
        with self.assertRaisesRegex(ValueError, 'PCANN'):
            prevent_data_regression(current, {'modelFiles': current['modelFiles'], 'currentReview': {'candidates': 2, 'PCANN': 1}})

    def test_one_submission_then_poll_to_success(self):
        calls = []
        statuses = iter(['syncing_files', 'succeed'])
        def api(method, path, body):
            calls.append((method, path, body))
            return {'id': 'abc'} if method == 'POST' else {'status': next(statuses)}
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            result = deploy(api, 'secret', 123, 'a'*40, receipt, sleep=lambda _: None)
            self.assertEqual(result['status'], 'succeed')
            self.assertEqual(sum(c[0] == 'POST' for c in calls), 1)
            self.assertNotIn('secret', receipt.read_text())
            self.assertEqual(calls[0][2]['artifact_id'], 123)
            with self.assertRaises(FileExistsError):
                deploy(api, 'secret', 123, 'a'*40, receipt)

    def test_uncertain_submission_is_not_retried(self):
        calls = []
        def api(*args):
            calls.append(args)
            raise ConnectionError('response lost')
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            with self.assertRaises(ConnectionError):
                deploy(api, 'secret', 123, 'a'*40, receipt)
            self.assertEqual(len(calls), 1)
            self.assertEqual(json.loads(receipt.read_text())['status'], 'submission_intent')

    def test_timeout_preserves_deployment_without_cancel_or_resubmit(self):
        calls = []
        ticks = iter([0, 0, 0, 1801])
        def api(method, path, body):
            calls.append(method)
            return {'id': 'abc'} if method == 'POST' else {'status': 'syncing_files'}
        with tempfile.TemporaryDirectory() as directory:
            receipt = Path(directory) / 'receipt.json'
            with self.assertRaises(TimeoutError):
                deploy(api, 'secret', 123, 'a'*40, receipt,
                       clock=lambda: next(ticks), sleep=lambda _: None)
            self.assertEqual(calls, ['POST', 'GET'])
            self.assertEqual(json.loads(receipt.read_text())['deploymentId'], 'abc')

    def test_terminal_failure_stops(self):
        with tempfile.TemporaryDirectory() as directory:
            def api(method, path, body):
                return {'id': 'abc'} if method == 'POST' else {'status': 'deployment_content_failed'}
            with self.assertRaisesRegex(RuntimeError, 'deployment_content_failed'):
                deploy(api, 'secret', 123, 'a'*40, Path(directory)/'receipt.json')


if __name__ == '__main__':
    unittest.main()
