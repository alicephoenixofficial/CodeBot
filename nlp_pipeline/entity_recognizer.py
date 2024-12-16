import keyword

class EntityRecognizer:
    def __init__(self):
        # Define entity types (keywords, identifiers, operators, etc.)
        self.entity_types = {
            "keyword": keyword.kwlist,
            "operator": ["+", "-", "*", "/", "=", ":", ">", "<", "(", ")", "{", "}", "[", "]", "!","|"],
            "function": set(),  # You can add logic to identify function names
            "class": set()     # Logic for class names
            # Add more as needed
        }
    
    def recognize_entities(self, tokens):

        recognized = []

        for token in tokens:
            if token in self.entity_types["keyword"]:
                recognized.append((token, "keyword"))
            elif token in self.entity_types["operator"]:
                recognized.append((token, "operator"))
            elif token.isidentifier():
                recognized.append((token, "identifier"))
            elif token.isnumeric():
                recognized.append((token, "number"))
            else:
                recognized.append((token, "unknown"))
        return recognized
