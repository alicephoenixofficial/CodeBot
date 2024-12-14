from nlp_pipeline.nlp_pipeline import NLPPipeline

if __name__ == "__main__":
    pipeline = NLPPipeline()
    print("NLP Pipeline initialized. Type 'exit' to quit.")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        response = pipeline.process_input(user_input)
        print(response)
