from context_manager import ContextManager
from nlp_pipeline.nlp_pipeline import NLPPipeline
import logging
import sys
class CodeBot:
    def __init__(self, user_id):
        self.context_manager = ContextManager(user_id)
        self.nlp_pipeline = NLPPipeline()

    def handle_input(self, user_input):
        response, intent = self.nlp_pipeline.process_input(user_input)
        self.context_manager.update(intent=intent, input_text=user_input, response=response)
        return response
    
    def start(self):
            print("Bot running. Type 'exit' to terminate or 'save' to save context manually.")
            while True:
                user_input = input("> ")
                if user_input.lower() == 'exit':
                    logging.info("Terminating session. Saving context...")
                    self.context_manager.save_context()  # Save context before exit
                    logging.info("Session terminated.")
                    sys.exit(0)  # Terminate the session manually
                elif user_input.lower() == 'save':
                    self.context_manager.save_context()  # Manually save context
                    logging.info("Context saved.")
                else:
                    response = self.handle_input(user_input)
                    logging.info(response)

if __name__ == "__main__":
    user_id = "user123"
    bot = CodeBot(user_id)
    bot.context_manager.load_context()  # Simulate loading the saved context
    bot.start()
