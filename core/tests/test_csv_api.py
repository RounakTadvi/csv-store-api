import tempfile
import os
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import csv
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlite3

CSV_URL = reverse("core:datasets")


def dataset_details_url(table_name):
    """Return Csv details url"""
    return reverse("core:dataset-details", args=[table_name])


class TestPublicDatasetsApi(TestCase):
    """
    Test the publicly available datasets API
    """

    def setUp(self) -> None:
        """
        setUp() is invoked before all tests run
        """
        self.client = APIClient()

    @patch("pandas.read_csv")
    @patch("pandas.DataFrame.to_sql")
    def test_upload_csv_success(self, mock_read_csv, mock_to_sql) -> None:
        """Test uploading a csv file"""
        file_name = "test.csv"
        # Open file in write mode (Arrange)
        with open(file_name, "w") as file:
            writer = csv.writer(file)
            # Add some rows in csv file
            writer.writerow(["name", "area", "country_code2", "country_code3"])
            writer.writerow(
                ["Albania", 28748, "AL", "ALB"],
            )
            writer.writerow(
                ["Algeria", 2381741, "DZ", "DZA"],
            )
            writer.writerow(
                ["Andorra", 468, "AD", "AND"],
            )
        # open file in read mode
        data = open(file_name, "rb")
        # Create a simple uploaded file
        data = SimpleUploadedFile(
            content=data.read(), name=data.name, content_type="multipart/form-data"
        )

        # Perform put request (Act)
        res = self.client.put(CSV_URL, {"file": data}, format="multipart")
        # Mock read_csv() and to_sql() functions provided by pandas module
        mock_read_csv.return_value = True
        mock_to_sql.return_value = True

        # Assert
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, "Data set uploaded")
        # Delete the test csv file
        os.remove(file_name)

    def test_upload_csv_invalid_file(self) -> None:
        """Test uploading image"""
        # Arrange
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            # Save Image File
            img.save(ntf, format="JPEG")
            # Set pointer back to beginning
            ntf.seek(0)
            # Act
            res = self.client.put(CSV_URL, {"file": ntf}, format="multipart")
            # Assert
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_csv_bad_request(self) -> None:
        """Test uploading an invalid csv file"""
        # Act
        res = self.client.put(CSV_URL, {"file": "notcsv"}, format="multipart")
        # Assert
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
