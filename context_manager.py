import json
import logging
import signal
import sys
import time
from threading import Timer
import os
from cryptography.fernet import Fernet  # For encryption (requires installation via `pip install cryptography`)
from dotenv import load_dotenv, set_key  # Import functions for loading and saving to .env file

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", stream=sys.stdout)
sys.stdout.flush()  # Force flush to ensure logs are printed immediately
class ContextManager:
    def __init__(self, user_id, inactivity_timeout=600, timeout=300, encryption_key=None):
        self.user_id = user_id
        self.context = {
            "user_id": user_id,
            "last_intent": None,
            "last_entity": None,
            "topic": None,
            "history": []
        }
        self.last_interaction_time = time.time()
        self.inactivity_timeout = inactivity_timeout  # Timeout for inactivity (e.g., 600 seconds)
        self.timeout = timeout  # Timeout for periodic archival (e.g., 300 seconds)
        self.context_file_path = f"session_context_{user_id}.json"
        self.timer = None
        self.is_terminated = False
         # Load environment variables from .env file
        load_dotenv()

        # Check if the key already exists in the .env file
        if "ENCRYPTION_KEY" not in os.environ:
            # If not, generate a new encryption key
            encryption_key = Fernet.generate_key()
            # Store it in the .env file
            set_key('.env', 'ENCRYPTION_KEY', encryption_key.decode())
            logging.info("Encryption key generated and stored in .env file.")
        else:
            logging.info("Encryption key already exists in .env file.")
        
        # Use the encryption key from the environment
        self.cipher = Fernet(os.getenv("ENCRYPTION_KEY"))

        # Set up signal handlers for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)  # Catch Ctrl+C
        signal.signal(signal.SIGTERM, self.signal_handler)  # Catch termination requests

    def signal_handler(self, sig, frame):
        """Handles termination signals and gracefully archives context."""
        logging.info("Program terminated. Saving context...")
        self.save_context()
        sys.exit(0)

    def update(self, **kwargs):
        """Updates the context based on new input and response."""
        self.last_interaction_time = time.time()  # Update the timestamp of the last interaction
        if "intent" in kwargs:
            self.context["last_intent"] = kwargs["intent"]
        if "entity" in kwargs:
            self.context["last_entity"] = kwargs["entity"]
        if "topic" in kwargs:
            self.context["topic"] = kwargs["topic"]
        if "input_text" in kwargs and "response" in kwargs:
            self.context["history"].append({"input": kwargs["input_text"], "response": kwargs["response"]})
        
        # Reset the inactivity timer and log the context
        self.reset_timer()
        logging.info(f"Context updated for user {self.user_id}. Current context: {self.context}")

    def reset_timer(self):
        """Resets the inactivity timer."""
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.timeout, self.on_timeout)
        self.timer.start()

    def on_timeout(self):
        """Saves context after inactivity timeout without terminating the session."""
        logging.info("Inactivity timeout reached. Saving context...")
        self.save_context()

    def save_context(self):
        """Saves the current context to an encrypted JSON file."""
        try:
            if not self.is_terminated:
                # Encrypt context before saving
                context_data = json.dumps(self.context).encode()
                encrypted_data = self.cipher.encrypt(context_data)
                with open(self.context_file_path, "wb") as file:
                    file.write(encrypted_data)
                logging.info(f"Context for user {self.user_id} saved.")
        except Exception as e:
            logging.error(f"Failed to save context: {e}")

    def manual_save(self):
        """Allows the user to manually save the context."""
        logging.info("Manually saving context...")
        self.save_context()

    def manual_terminate(self):
        """Allows the user to manually terminate the session and save the context."""
        logging.info("Manually terminating session. Saving context...")
        self.save_context()
        self.is_terminated = True
        logging.info("Session terminated.")
        sys.exit(0)  # Terminate the session manually

    def load_context(self):
        """Load the context from the encrypted JSON file if it exists."""
        if os.path.exists(self.context_file_path):
            print("os path exists")
            try:
                with open(self.context_file_path, "rb") as file:
                    encrypted_data = file.read()
                    print("Encrypted data read.")
                
                    # Try decrypting and decoding
                    try:
                        context_data = self.cipher.decrypt(encrypted_data).decode()
                        print("Decryption successful.")
                    except Exception as decryption_error:
                        logging.error(f"Decryption failed: {decryption_error}")
                        return  # Exit the method early, as decryption failed
                    
                    # Try loading the context as JSON
                    try:
                        self.context = json.loads(context_data)
                        print("Context loaded.")
                        logging.info(f"Context for user {self.user_id} loaded.")
                    except json.JSONDecodeError as json_error:
                        logging.error(f"Error decoding JSON: {json_error}")
                        self.clear_context()
            except Exception as e:
                # Catch any unexpected errors and log them
                logging.error(f"Decryption failed for user {self.user_id}: {e}")
                self.clear_context()
        else:
            logging.info(f"No saved context found for user {self.user_id}. Starting fresh.")


    def clear_context(self):
        """Clear the current context."""
        self.context = {key: None for key in self.context.keys()}
        self.context["history"] = []
        self.last_interaction_time = time.time()
        logging.info(f"Context for user {self.user_id} cleared.")

    def get_summary(self):
        """Retrieve a summary of the current context."""
        return {
            "current_topic": self.context.get("topic"),
            "last_intent": self.context.get("last_intent"),
            "last_entity": self.context.get("last_entity"),
        }

    def start(self, bot):
        """Starts the bot and waits for user interaction."""
        logging.info("Bot running. Type 'exit' to terminate or 'save' to save context manually.")
        while not self.is_terminated:
            user_input = input("> ").strip().lower()
            if user_input == 'exit':
                self.manual_terminate()
            elif user_input == 'save':
                self.manual_save()
            else:
                logging.info("Bot responding to input...")
                self.update(input_text=user_input, response="Bot response based on input.")
                
                # Process input through CodeBot
                response = bot.handle_input(user_input) 
                print(response)
                time.sleep(1)  # Simulating bot's work

    def handle_input(self, user_input):
        # Placeholder: Will use NLP here in future steps
        return f"Bot response to '{user_input}'"

if __name__ == "__main__":
    logging.info("Context Manager is running...")
    # Example usage:
# context_manager = ContextManager(user_id="user123")
# context_manager.load_context()  # Simulate loading the saved context
# context_manager.start()
