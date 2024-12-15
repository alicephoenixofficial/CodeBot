import unittest
from unittest.mock import patch, mock_open, MagicMock
from context_manager import ContextManager
import os
from cryptography.fernet import Fernet  # For encryption (requires installation via `pip install cryptography`)

class TestContextManager(unittest.TestCase):

    def setUp(self):
        # Set up the test with a unique user ID
        self.user_id = "user123"
        self.encryption_key = Fernet.generate_key()
        self.context_manager = ContextManager(user_id=self.user_id, encryption_key=self.encryption_key)

    @patch("builtins.open", new_callable=mock_open)  # Mock file opening
    @patch("cryptography.fernet.Fernet.encrypt", return_value=b"encrypted_data")
    def test_save_context(self, mock_encrypt, mock_file):
        # Test saving the context
        self.context_manager.update(intent="greeting", entity="hello", topic="greeting", input_text="Hi", response="Hello, user!")
        self.context_manager.save_context()
        
        # Verify encryption and file operations
        mock_encrypt.assert_called_once()
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "wb")
        mock_file().write.assert_called_once_with(b"encrypted_data")

    @patch("builtins.open", new_callable=mock_open, read_data=b"encrypted_data")
    @patch("cryptography.fernet.Fernet.decrypt", return_value=b'{"user_id": "user123", "last_intent": "greeting", "last_entity": "hello", "topic": "greeting", "history": []}')
    def test_load_context(self, mock_decrypt, mock_file):
        
        # Test loading the context with decryption
        self.context_manager.load_context()
        
        # Verify decryption and file operations
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "rb")
        mock_decrypt.assert_called_once_with(b"encrypted_data")
        
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
    @patch("cryptography.fernet.Fernet.encrypt", return_value=b"encrypted_data")
    def test_manual_save(self, mock_encrypt, mock_file):
        
        # Test manual saving of context with encryption
        self.context_manager.update(intent="greeting", entity="hello", topic="greeting", input_text="Hi", response="Hello, user!")
        self.context_manager.manual_save()
        
        # Verify encryption and file operations
        mock_encrypt.assert_called_once()
        mock_file.assert_called_once_with(f"session_context_{self.user_id}.json", "wb")
        mock_file().write.assert_called_once_with(b"encrypted_data")

    @patch("builtins.open", new_callable=mock_open, read_data=b"encrypted_data")
    @patch("cryptography.fernet.Fernet.decrypt", side_effect=Exception("Decryption failed"))
    def test_load_corrupt_context_file(self, mock_decrypt, mock_file):
        
        # Test handling of corrupt encrypted context files
        with self.assertLogs(level="ERROR") as log:
            self.context_manager.load_context()

        # Verify decryption failure was logged
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

    @patch("threading.Timer", autospec=True)
    def test_reset_timer(self, mock_timer):
        
        # Mock timer instance
        mock_timer_instance = mock_timer.return_value
        self.context_manager.timer = mock_timer_instance  # Set the timer explicitly
        self.context_manager.timer.start()

        self.context_manager.reset_timer()
        mock_timer_instance.cancel.assert_called_once()  # Timer should be canceled first
        mock_timer_instance.start.assert_called_once()  # Timer should be started

if __name__ == "__main__":
    unittest.main()
