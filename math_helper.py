from sympy import symbols, Eq, solve, simplify, sympify
import re

def solve_math_problem(problem: str) -> str:
    try:
        # Whitespace entfernen und implizite Multiplikation erkennen
        problem = problem.replace(" ", "")
        problem = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', problem)         # 2x → 2*x
        problem = re.sub(r'(\))(\()', r'\1*\2', problem)               # )( → )*(

        # Variablen automatisch erkennen
        variables = sorted(set(re.findall(r'[a-zA-Z]', problem)))
        if not variables:
            variables = ['x']
        sympy_vars = symbols(variables)

        # Gleichung oder Ausdruck?
        if "=" in problem:
            left, right = problem.split("=")
            left_expr = sympify(left, locals=dict(zip(variables, sympy_vars)))
            right_expr = sympify(right, locals=dict(zip(variables, sympy_vars)))
            eq = Eq(left_expr, right_expr)
            result = solve(eq, sympy_vars)
            if not result:
                return "Keine Lösung gefunden."
            return f"Lösung(en): {result}"
        else:
            expr = sympify(problem, locals=dict(zip(variables, sympy_vars)))
            simplified = simplify(expr)
            return f"Vereinfachter Ausdruck: {simplified}"

    except Exception as e:
        return f"❌ Fehler beim Lösen: {e}"
