import json
import logging
import signal
import sys
import time
from threading import Timer
import os

class ContextManager:
    def __init__(self, user_id, inactivity_timeout=600, timeout=300):
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

        # Set up signal handlers for graceful exit
        signal.signal(signal.SIGINT, self.signal_handler)  # Catch Ctrl+C
        signal.signal(signal.SIGTERM, self.signal_handler)  # Catch termination requests

    def signal_handler(self, sig, frame):
        """Handles termination signals and gracefully archives context."""
        print("\nProgram terminated. Saving context...")
        self.save_context()
        sys.exit(0)

    def update(self, intent=None, entity=None, topic=None, input_text=None, response=None):
        """Updates the context based on new input and response."""
        self.last_interaction_time = time.time()  # Update the timestamp of the last interaction
        if intent:
            self.context["last_intent"] = intent
        if entity:
            self.context["last_entity"] = entity
        if topic:
            self.context["topic"] = topic
        if input_text and response:
            self.context["history"].append({"input": input_text, "response": response})
        
        # Reset the inactivity timer
        self.reset_timer()

    def reset_timer(self):
        """Resets the inactivity timer."""
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.timeout, self.on_timeout)
        self.timer.start()

    def on_timeout(self):
        """Saves context after inactivity timeout without terminating the session."""
        print("Inactivity timeout reached. Saving context...")
        self.save_context()

    def save_context(self):
        """Saves the current context to a JSON file."""
        if not self.is_terminated:
            # Convert context to JSON and save
            with open(self.context_file_path, "w") as file:
                json.dump(self.context, file, indent=4)
            print(f"Context for user {self.user_id} saved.")

    def manual_save(self):
        """Allows the user to manually save the context."""
        print("Manually saving context...")
        self.save_context()

    def manual_terminate(self):
        """Allows the user to manually terminate the session and save the context."""
        print("Manually terminating session. Saving context...")
        self.save_context()
        self.is_terminated = True
        print("Session terminated.")
        sys.exit(0)  # Terminate the session manually

    def load_context(self):
        """Load the context from the JSON file if it exists."""
        if os.path.exists(self.context_file_path):
            try:
                with open(self.context_file_path, "r") as file:
                    self.context = json.load(file)
                    print(f"Context for user {self.user_id} loaded.")
            except (json.JSONDecodeError, IOError) as e:
                # Handle corrupt or unreadable files gracefully
                logging.error(f"Error loading context for user {self.user_id}: {e}")
                self.context = {
                    "user_id": self.user_id,
                    "last_intent": None,
                    "last_entity": None,
                    "topic": None,
                    "history": []
                }
        else:
            print(f"No saved context found for user {self.user_id}. Starting fresh.")

    def clear_context(self):
        """Clear the current context."""
        self.context = {key: None for key in self.context.keys()}
        self.context["history"] = []
        self.last_interaction_time = time.time()
        print(f"Context for user {self.user_id} cleared.")

    def get_summary(self):
        """Retrieve a summary of the current context."""
        return {
            "current_topic": self.context.get("topic"),
            "last_intent": self.context.get("last_intent"),
            "last_entity": self.context.get("last_entity"),
        }

    def start(self):
        """Starts the bot and waits for user interaction."""
        print("Bot running. Type 'exit' to terminate or 'save' to save context manually.")
        while not self.is_terminated:
            user_input = input("> ").strip().lower()
            if user_input == 'exit':
                self.manual_terminate()
            elif user_input == 'save':
                self.manual_save()
            else:
                print("Bot responding to input...")
                self.update(input_text=user_input, response="Bot response based on input.")
                time.sleep(1)  # Simulating bot's work

if __name__ == "__main__":
    print("Context Manager is running...")
    # You can call any functions or actions you'd like to test here

# Example usage:
#context_manager = ContextManager(user_id="user123")
#context_manager.load_context()  # Simulate loading the saved context
#context_manager.start()
