from sympy import sympify, solve
from agent import ask_deepseek

def solve_math_problem(problem):
    try:
        result = solve(sympify(problem))
        return f"Lösung: {result}"
    except:
        return ask_deepseek(f"Löse dieses Matheproblem:\n{problem}")