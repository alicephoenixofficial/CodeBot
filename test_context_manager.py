import unittest
from unittest.mock import patch, mock_open, MagicMock
from context_manager import ContextManager
import os

class TestContextManager(unittest.TestCase):

    def setUp(self):
        # Set up the test with a unique user ID
        self.user_id = "user123"
        self.context_manager = ContextManager(user_id=self.user_id)

    @patch("builtins.open", new_callable=mock_open)  # Mock file opening
    @patch("json.dump")  # Mock JSON dump
    def test_save_context(self, mock_json_dump, mock_file):
        # Test saving the context
        self.context_manager.update(intent="greeting", entity="hello", topic="greeting", input_text="Hi", response="Hello, user!")
        self.context_manager.save_context()
        
        # Assert that the file was opened for writing
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "w")
        # Assert that json.dump was called with the context
        mock_json_dump.assert_called_once_with(self.context_manager.context, mock_file(), indent=4)

    @patch("builtins.open", new_callable=mock_open, read_data='{"user_id": "user123", "last_intent": "greeting", "last_entity": "hello", "topic": "greeting", "history": []}')
    @patch("json.load")  # Mock JSON load
    def test_load_context(self, mock_json_load, mock_file):
        # Mock JSON load to return a predefined context
        mock_json_load.return_value = {
            "user_id": self.user_id,
            "last_intent": "greeting",
            "last_entity": "hello",
            "topic": "greeting",
            "history": []
        }
        
        self.context_manager.load_context()
        # Assert that the file was opened for reading
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "r")
        # Assert that json.load was called to load the context
        mock_json_load.assert_called_once_with(mock_file())
        # Verify that the loaded context matches
        self.assertEqual(self.context_manager.context["last_intent"], "greeting")
        self.assertEqual(self.context_manager.context["last_entity"], "hello")
        self.assertEqual(self.context_manager.context["topic"], "greeting")

    @patch("sys.exit")  # Mock sys.exit
    def test_manual_terminate(self, mock_sys_exit):
        # Test manual termination
        self.context_manager.update(intent="greeting", entity="hello", topic="greeting", input_text="Hi", response="Hello, user!")
        self.context_manager.manual_terminate()
        
        # Verify that save_context was called before termination
        self.assertTrue(self.context_manager.is_terminated)
        mock_sys_exit.assert_called_once_with(0)  # Assert sys.exit(0) was called

    @patch("builtins.open", new_callable=mock_open)  # Mock file opening
    @patch("json.dump")  # Mock JSON dump
    def test_manual_save(self, mock_json_dump, mock_file):
        # Test manual saving
        self.context_manager.update(intent="greeting", entity="hello", topic="greeting", input_text="Hi", response="Hello, user!")
        self.context_manager.manual_save()
        
        # Assert that save_context was triggered
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "w")
        mock_json_dump.assert_called_once_with(self.context_manager.context, mock_file(), indent=4)

    @patch("builtins.open", new_callable=mock_open, read_data="corrupt {json:")
    @patch("os.path.exists", return_value=True)
    def test_load_corrupt_context_file(self, mock_exists, mock_open_file):
        """Test handling of corrupt JSON context files."""
        # Attempt to load the corrupt file
        with self.assertLogs(level="ERROR") as log:
            self.context_manager.load_context()

        # Check the logs for a meaningful error
        self.assertIn("Error loading context", log.output[0])

        # Verify the context is reset
        self.assertEqual(self.context_manager.context["history"], [])
        self.assertIsNone(self.context_manager.context["last_intent"])
        self.assertIsNone(self.context_manager.context["topic"])
        self.assertIsNone(self.context_manager.context["last_entity"])

    @patch("builtins.open", side_effect=IOError("Failed to open file"))
    @patch("os.path.exists", return_value=True)
    def test_load_io_error(self, mock_exists, mock_open_file):
        """Test handling of IO errors during file reading."""
        # Attempt to load a file with an IO error
        with self.assertLogs(level="ERROR") as log:
            self.context_manager.load_context()

        # Check the logs for a meaningful error
        self.assertIn("Error loading context", log.output[0])

        # Verify the context is reset
        self.assertEqual(self.context_manager.context["history"], [])
        self.assertIsNone(self.context_manager.context["last_intent"])
        self.assertIsNone(self.context_manager.context["topic"])
        self.assertIsNone(self.context_manager.context["last_entity"])

if __name__ == "__main__":
    unittest.main()
