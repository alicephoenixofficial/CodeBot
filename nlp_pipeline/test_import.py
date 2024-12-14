# test_import.py
from nlp_pipeline.intent_classifier import IntentClassifier
import sys
print(sys.path)

classifier = IntentClassifier()
print(classifier.classify(["hello"]))
