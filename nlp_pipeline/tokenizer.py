class Tokenizer:
    def __init__(self):
        self.stopwords = ["the", "is", "a", "an", "the", "in", "on", "of", "to", "and", "for"]

    def tokenize(self, text):
        # Simple tokenizer that splits by spaces and removes stopwords
        tokens = text.lower().split()
        tokens = [token for token in tokens if token not in self.stopwords]
        return tokens