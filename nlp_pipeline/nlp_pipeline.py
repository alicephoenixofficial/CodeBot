from nlp_pipeline.tokenizer import Tokenizer
from nlp_pipeline.pos_tagger import POSTagger
from nlp_pipeline.intent_classifier import IntentClassifier
from nlp_pipeline.entity_recognizer import EntityRecognizer
from nlp_pipeline.response_generator import ResponseGenerator

class NLPPipeline:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.pos_tagger = POSTagger()
        self.intent_classifier = IntentClassifier()
        self.entity_recognizer = EntityRecognizer()
        self.response_generator = ResponseGenerator()

    def process_input(self, user_input):
        print(f"User Input: {user_input}")
        tokens = self.tokenizer.tokenize(user_input)
        print(f"Tokens: {tokens}")
        pos_tags = self.pos_tagger.tag(tokens)
        print(f"POS Tags: {pos_tags}")
        intent = self.intent_classifier.classify(tokens)
        print(f"Detected Intent: {intent}")
        entities = self.entity_recognizer.recognize(tokens)
        print(f"Recognized Entities: {entities}")
        response = self.response_generator.generate(intent, entities)
        print(f"Response: {response}")
        return response