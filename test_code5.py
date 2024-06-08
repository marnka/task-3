import unittest
from unittest.mock import patch
from io import StringIO
import os

class TestEventManager(unittest.TestCase):

    def setUp(self):
        self.event_manager = EventManager()
        self.listener = LoggingListener("test_log.txt", "Event occurred: %s")

    def test_subscribe_and_notify(self):
        self.event_manager.subscribe("test_event", self.listener)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.event_manager.notify("test_event", "Test data")
            expected_output = "Event occurred: Test data\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_unsubscribe(self):
        self.event_manager.subscribe("test_event", self.listener)
        self.event_manager.unsubscribe("test_event", self.listener)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.event_manager.notify("test_event", "Test data")
            self.assertEqual(mock_stdout.getvalue(), "")
            

class TestEditor(unittest.TestCase):

    def setUp(self):
        self.editor = Editor()

    def test_open_file(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.editor.open_file("test_file.txt")
            expected_output = "Email sent to admin@example.com: Someone has opened file: test_file.txt\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_save_file(self):
        email_alerts = EmailAlertsListener("admin@example.com", "Test message: %s")
        self.editor.events.subscribe("save", email_alerts)
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.editor.save_file()
            expected_output = "Email sent to admin@example.com: Test message: None\n"
            self.assertEqual(mock_stdout.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()
