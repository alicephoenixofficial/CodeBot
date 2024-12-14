class IntentClassifier:
    def classify(self, tokens):
        """Classify the intent based on keywords."""
        if "hello" in tokens or "hi" in tokens:
            return "greeting"
        elif "developer" in tokens:
            return "self_intro"
        else:
            return "unknown"