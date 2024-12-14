class POSTagger:
    def tag(self, tokens):
        """Simple POS tagging based on predefined rules."""
        tag_map = {
            "hello": "INTJ",
            "I": "PRON",
            "am": "VERB",
            "a": "DET",
            "developer": "NOUN",
        }
        return [(token, tag_map.get(token, "UNK")) for token in tokens]