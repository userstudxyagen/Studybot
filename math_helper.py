from sympy import symbols, Eq, solve, sympify
import re

def solve_math_problem(problem: str) -> str:
    x = symbols('x')
    # Ersetze z.B. 2x mit 2*x, damit sympy das versteht
    problem = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', problem.replace(" ", ""))

    try:
        if "=" in problem:
            left_side, right_side = problem.split("=")
            left_expr = sympify(left_side)
            right_expr = sympify(right_side)
            equation = Eq(left_expr, right_expr)
            result = solve(equation, x)
        else:
            expr = sympify(problem)
            result = solve(expr, x)
        return str(result)
    except Exception as e:
        return f"Fehler beim Lösen: {e}"
