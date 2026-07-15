import os
import unittest
import json
from pathlib import Path


class ApiSmokeTests(unittest.TestCase):
    def setUp(self):
        # Ensure no API token is required for tests
        os.environ.pop('AEGIS_API_TOKEN', None)
        # Import the app after env setup
        try:
            from api import app as app_module
            self.app = app_module.app.test_client()
        except ModuleNotFoundError:
            # Flask not installed in this interpreter; skip API tests
            raise unittest.SkipTest("Flask not available in test environment")

    def test_health(self):
        res = self.app.get('/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('status', data)

    def test_create_and_list_runs(self):
        payload = {'task': 'unittest run', 'status': 'completed', 'summary': 'test run summary'}
        post = self.app.post('/runs', json=payload)
        self.assertIn(post.status_code, (200, 201))
        created = post.get_json()
        self.assertEqual(created.get('task'), 'unittest run')

        # list via proxy (no token)
        res = self.app.get('/proxy/runs')
        self.assertEqual(res.status_code, 200)
        runs = res.get_json()
        self.assertIsInstance(runs, list)
        # at least one run exists
        self.assertTrue(any(r.get('task') == 'unittest run' for r in runs))


if __name__ == '__main__':
    unittest.main()
