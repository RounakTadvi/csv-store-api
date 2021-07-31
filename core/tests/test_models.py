from unittest.case import expectedFailure
from django.test import TestCase
from unittest.mock import patch
from core import models


class TestCsvModel(TestCase):
    """
    This class contains unit tests written for models
    """

    @patch("uuid.uuid4")
    def test_csv_file_name(self, mock_uuid4) -> None:
        """Test that csv file is saved in the correct location"""

        uuid = "Test UUID"
        # Mock uuid
        mock_uuid4.return_value = uuid
        file_path = models.csv_file_path(None, "myfile.csv")

        expected_path = f"uploads/csv_files/{uuid}.csv"

        self.assertEqual(file_path, expected_path)
