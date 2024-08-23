import unittest
from unittest.mock import patch
import sqlite3
import os
import time
from utils.databaseUtils.database import get_db_connection, setup_db, insert_or_update_file, get_data_files, get_data_history, log_public_file

class TestDatabaseFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_drive_inventory.db'
        os.environ['DB_FILE'] = cls.test_db
        setup_db()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_db)

    def test_get_db_connection(self):
        conn = get_db_connection()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()

    def test_setup_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        cursor.close()
        conn.close()

    def test_insert_or_update_file(self):
        file_data = {
            'id': 'test_file_1',
            'name': 'Test File',
            'mimeType': 'text/plain',
            'owner': 'user1',
            'visibility': 'public',
            'modifiedTime': time.strftime('%Y-%m-%dT%H:%M:%S')
        }
        insert_or_update_file([file_data])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files WHERE id = ?", (file_data['id'],))
        result = cursor.fetchone()
        self.assertEqual(result[0], file_data['id'])
        self.assertEqual(result[1], file_data['name'])
        # ... check other fields
        cursor.close()
        conn.close()

    # ... Add more test cases for other functions
