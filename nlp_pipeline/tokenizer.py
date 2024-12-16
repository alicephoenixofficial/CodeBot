import re
import keyword

class Tokenizer:
    def __init__(self):
        # Basic stopwords for natural language
        self.stopwords = {"the", "is", "a", "an", "in", "on", "of", "to", "and", "for"}
        # Programming language keywords (using Python as an example)
        self.programming_keywords = set(keyword.kwlist)
    
    def tokenize(self, text):

        # Split text into words and symbols
        tokens = re.findall(r"[a-zA-Z0-9_]+|[^\s\w]", text)
        
        processed_tokens = []

        for token in tokens:
            # Preserve programming keywords
            if token in self.programming_keywords:
                processed_tokens.append(token)
            # Exclude natural language stopwords for non-code tokens
            elif token.lower() not in self.stopwords:
                processed_tokens.append(token)
        
        return processed_tokens

# if __name__ == "__main__":
    # tokenizer = Tokenizer()
    # sample_input = "The loop is written as: for i in range(10): print(i)"
    # tokens = tokenizer.tokenize(sample_input)
    # print(tokens)