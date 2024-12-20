class ResponseGenerator:
    def generate(self, intent, entities):
        """Generate a response based on intent and entities."""
        if intent == "greet":
           return "Hello! How can I assist you today?"
        elif intent == "bye":
           return "Goodbye! Have a great day!"
        elif intent == "ask_for_help":
            return "How can I help you?"
        elif intent == "self_intro":
            return "Nice to meet you! I'm a bot designed to assist with coding tasks."
        else:
            return "I'm not sure I understand. Could you clarify?"