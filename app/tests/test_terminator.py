from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import MagicMock, patch
import app.terminator


class TestTerminator(TestCase):
    @patch('app.terminator.requests')
    def test_get_current_instance_details(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'region': 'test-region',
            'instanceId': 'test-instance-id'
        }
        mock_request.get.return_value = mock_response
        region, instanceId = app.terminator.get_current_instance_details()
        self.assertEqual(region, 'test-region')
        self.assertEqual(instanceId, 'test-instance-id')

    def test_calculate_time_30_min(self):
        modified_time = datetime.now() - timedelta(minutes=30)
        delta_time = app.terminator.calculate_time(modified_time.timestamp())
        self.assertEqual(delta_time, 0.5)

    def test_calculate_time_1_hr(self):
        modified_time = datetime.now() - timedelta(hours=1)
        delta_time = app.terminator.calculate_time(modified_time.timestamp())
        self.assertEqual(delta_time, 1)