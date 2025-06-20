from agent import ask_model

def get_coding_help(question):
    return ask_model(f"Hilf bei folgendem Codeproblem:\n{question}")
