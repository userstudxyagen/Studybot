from sympy import symbols, Eq, solve, sympify, simplify, solveset, S
import re

def solve_math_problem(problem: str) -> str:
    try:
        # Whitespace entfernen
        problem = problem.replace(" ", "")

        # Implizite Multiplikation: z.B. 2x -> 2*x, (x+1)(x-1) -> (x+1)*(x-1)
        problem = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', problem)
        problem = re.sub(r'(\))(\()', r'\1*\2', problem)

        # Variablen erkennen (a-z, A-Z)
        variables = sorted(set(re.findall(r'[a-zA-Z]', problem)))
        if not variables:
            variables = ['x']  # default Variable

        sympy_vars = symbols(variables)

        # Prüfen auf Gleichungen oder Ungleichungen
        if "=" in problem:
            left_side, right_side = problem.split("=")
            left_expr = sympify(left_side, locals=dict(zip(variables, sympy_vars)))
            right_expr = sympify(right_side, locals=dict(zip(variables, sympy_vars)))
            eq = Eq(left_expr, right_expr)
            result = solve(eq, sympy_vars)
        elif any(op in problem for op in ["<=", ">=", "<", ">"]):
            # Ungleichungen mit solveset lösen
            for op in ["<=", ">=", "<", ">"]:
                if op in problem:
                    left_side, right_side = problem.split(op)
                    left_expr = sympify(left_side, locals=dict(zip(variables, sympy_vars)))
                    right_expr = sympify(right_side, locals=dict(zip(variables, sympy_vars)))
                    # Gleichung in Ungleichung umwandeln
                    if op == "<=":
                        from sympy import Le
                        inequality = Le(left_expr, right_expr)
                    elif op == ">=":
                        from sympy import Ge
                        inequality = Ge(left_expr, right_expr)
                    elif op == "<":
                        from sympy import Lt
                        inequality = Lt(left_expr, right_expr)
                    elif op == ">":
                        from sympy import Gt
                        inequality = Gt(left_expr, right_expr)
                    result = solveset(inequality, sympy_vars[0], domain=S.Reals)
                    break
        else:
            # Nur Ausdruck -> z.B. vereinfachen
            expr = sympify(problem, locals=dict(zip(variables, sympy_vars)))
            simplified = simplify(expr)
            return f"Vereinfachter Ausdruck: {simplified}"

        # Ergebnis formatieren
        if isinstance(result, list) or isinstance(result, tuple):
            if not result:
                return "Keine Lösung gefunden."
            return "Lösungen: " + ", ".join(str(r) for r in result)
        else:
            return str(result)

    except Exception as e:
        return f"Fehler beim Lösen: {e}"
