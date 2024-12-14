class EntityRecognizer:
    def recognize(self, tokens):
        """Simple entity recognition based on keywords."""
        entities = []
        for token in tokens:
            if token.lower() == "developer":
                entities.append({"type": "profession", "value": "developer"})
        return entities
