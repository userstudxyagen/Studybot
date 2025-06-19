from sympy import symbols, Eq, solve, simplify, sympify
import re

def solve_math_problem(problem: str) -> str:
    try:
        # Whitespace entfernen und implizite Multiplikation behandeln (z.B. 2x → 2*x)
        clean = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', problem.replace(" ", ""))
        
        # Variablen erkennen (Standard: x)
        variables = sorted(set(re.findall(r'[a-zA-Z]', clean))) or ['x']
        sym_dict = {v: symbols(v) for v in variables}

        # Gleichung oder Ausdruck unterscheiden
        if "=" in clean:
            left, right = clean.split("=")
            eq = Eq(sympify(left, locals=sym_dict), sympify(right, locals=sym_dict))
            result = solve(eq, list(sym_dict.values())[0])
            return f"Lösung: {result}"
        else:
            expr = sympify(clean, locals=sym_dict)
            return f"Vereinfacht: {simplify(expr)}"
    
    except Exception as e:
        return f"❌ Fehler: {e}"
