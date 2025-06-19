from sympy import sympify, solve

def solve_math_problem(problem: str) -> str:
    try:
        expr = sympify(problem)
        result = solve(expr)
        return str(result)
    except Exception as e:
        return f"Fehler beim Lösen: {e}"
