from context_manager import ContextManager
from nlp_pipeline import Tokenizer, IntentClassifier

class CodeBot:
    def __init__(self, user_id):
        self.context_manager = ContextManager(user_id)
        self.tokenizer = Tokenizer()
        self.intent_recognizer = IntentClassifier()

    def handle_input(self, user_input):
        tokens = self.tokenizer.tokenize(user_input)
        intent = self.intent_recognizer.recognize_intent(tokens)
        
        if intent == "greet":
            response = "Hello! How can I assist you today?"
        elif intent == "bye":
            response = "Goodbye! Have a great day!"
        elif intent == "ask_for_help":
            response = "How can I help you?"
        else:
            response = "I'm not sure how to respond to that."
        
        self.context_manager.update(intent=intent, input_text=user_input, response=response)
        return response
    
def start(self):
        print("Bot running. Type 'exit' to terminate or 'save' to save context manually.")
        while True:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                self.context_manager.save_context()  # Save context before exit
                break
            elif user_input.lower() == 'save':
                self.context_manager.save_context()  # Manually save context
                print("Context saved.")
            else:
                response = self.handle_input(user_input)
                print(response)

if __name__ == "__main__":
    user_id = "user123"
    bot = CodeBot(user_id)
    bot.context_manager.load_context()  # Simulate loading the saved context
    bot.context_manager.start(bot)
