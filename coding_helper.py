from agent import ask_deepseek

def get_coding_help(question):
    return ask_deepseek(f"Hilf bei folgendem Codeproblem:\n{question}")