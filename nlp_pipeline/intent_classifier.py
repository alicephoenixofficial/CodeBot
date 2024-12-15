class IntentClassifier:
    
    def __init__(self):
        self.intents = {
            "greet": ["hi", "hello", "hey", "howdy"],
            "bye": ["bye", "goodbye", "see you", "exit"],
            "ask_for_help": ["help", "assist", "support"]
        }

    def recognize_intent(self, tokens):
        for intent, keywords in self.intents.items():
            if any(keyword in tokens for keyword in keywords):
                return intent
        return "unknown"  # If no match, return 'unknown'
