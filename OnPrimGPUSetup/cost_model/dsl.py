"""Tiny formula DSL: one expression string -> Python, Excel and JavaScript.

Every derived quantity in the cost model is written once, as a Python-syntax
expression over named variables, and transpiled to all three targets. That is
what guarantees the engine, the Excel workbook and the HTML calculator agree.

Allowed syntax: numbers, names, + - * / **, unary -, comparisons, and/or/not,
and the functions in FUNCS below.
"""
import ast
import math

FUNCS = {
    # name: (python, excel, js)
    "max": ("max", "MAX", "Math.max"),
    "min": ("min", "MIN", "Math.min"),
    "sqrt": ("math.sqrt", "SQRT", "Math.sqrt"),
    "ln": ("math.log", "LN", "Math.log"),
    "ceil": ("_ceil", "ROUNDUP({0},0)", "_ceil"),
    "floor": ("_floor", "ROUNDDOWN({0},0)", "_floor"),
    "iff": (None, "IF", None),  # handled specially (lazy)
}

_BINOPS = {ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.Pow: "**"}
_CMPOPS = {ast.Gt: ">", ast.Lt: "<", ast.GtE: ">=", ast.LtE: "<=", ast.Eq: "==", ast.NotEq: "!="}
_XL_CMP = {">": ">", "<": "<", ">=": ">=", "<=": "<=", "==": "=", "!=": "<>"}


def _ceil(x):
    # Excel ROUNDUP(x,0): away from zero
    return math.copysign(math.ceil(abs(x)), x)


def _floor(x):
    # Excel ROUNDDOWN(x,0): toward zero
    return float(math.trunc(x))


def names_in(expr):
    tree = ast.parse(expr, mode="eval")
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id not in FUNCS}


def _tx(node, target, ref):
    """Transpile an AST node. ref(name) maps a variable name to target text."""
    t = lambda n: _tx(n, target, ref)
    if isinstance(node, ast.Expression):
        return t(node.body)
    if isinstance(node, ast.Constant):
        v = node.value
        if isinstance(v, bool):
            v = int(v)
        return repr(float(v)) if target != "xl" else _xl_num(v)
    if isinstance(node, ast.Name):
        return ref(node.id)
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return f"(-{t(node.operand)})"
        if isinstance(node.op, ast.Not):
            return {"py": f"(not {t(node.operand)})", "js": f"(!{t(node.operand)})",
                    "xl": f"NOT({t(node.operand)})"}[target]
    if isinstance(node, ast.BinOp):
        op = _BINOPS[type(node.op)]
        if op == "**":
            return {"py": f"({t(node.left)}**{t(node.right)})",
                    "js": f"Math.pow({t(node.left)},{t(node.right)})",
                    "xl": f"POWER({t(node.left)},{t(node.right)})"}[target]
        return f"({t(node.left)}{op}{t(node.right)})"
    if isinstance(node, ast.Compare):
        assert len(node.ops) == 1, "chain comparisons not supported"
        op = _CMPOPS[type(node.ops[0])]
        if target == "xl":
            op = _XL_CMP[op]
        elif target == "js" and op in ("==", "!="):
            op = op + "="
        return f"({t(node.left)}{op}{t(node.comparators[0])})"
    if isinstance(node, ast.BoolOp):
        parts = [t(v) for v in node.values]
        if isinstance(node.op, ast.And):
            return {"py": "(" + " and ".join(parts) + ")", "js": "(" + " && ".join(parts) + ")",
                    "xl": "AND(" + ",".join(parts) + ")"}[target]
        return {"py": "(" + " or ".join(parts) + ")", "js": "(" + " || ".join(parts) + ")",
                "xl": "OR(" + ",".join(parts) + ")"}[target]
    if isinstance(node, ast.Call):
        fname = node.func.id
        args = [t(a) for a in node.args]
        if fname == "iff":
            c, a, b = args
            return {"py": f"({a} if {c} else {b})", "js": f"({c} ? {a} : {b})",
                    "xl": f"IF({c},{a},{b})"}[target]
        py, xl, js = FUNCS[fname]
        if target == "xl":
            return xl.format(*args) if "{0}" in xl else f"{xl}({','.join(args)})"
        fn = py if target == "py" else js
        return f"{fn}({','.join(args)})"
    raise ValueError(f"unsupported syntax: {ast.dump(node)}")


def _xl_num(v):
    v = float(v)
    return str(int(v)) if v.is_integer() and abs(v) < 1e15 else repr(v)


def to_py(expr, ref=lambda n: f"v[{n!r}]"):
    return _tx(ast.parse(expr, mode="eval"), "py", ref)


def to_js(expr, ref=lambda n: f"v.{n}"):
    return _tx(ast.parse(expr, mode="eval"), "js", ref)


def to_xl(expr, ref):
    return "=" + _tx(ast.parse(expr, mode="eval"), "xl", ref)


def toposort(formulas, known):
    """Order formulas so each one's inputs are computed first."""
    by_name = {f.name: f for f in formulas}
    done, order = set(known), []

    def visit(name, stack=()):
        if name in done:
            return
        if name not in by_name:
            raise KeyError(f"undefined variable {name!r} (needed by {stack[-1] if stack else '?'})")
        if name in stack:
            raise ValueError(f"cycle: {' -> '.join(stack + (name,))}")
        for dep in sorted(names_in(by_name[name].expr)):
            visit(dep, stack + (name,))
        done.add(name)
        order.append(by_name[name])

    for f in formulas:
        visit(f.name)
    return order


def compile_py(formulas, known):
    """Return evaluate(v: dict) -> dict that fills in every formula in order."""
    order = toposort(formulas, known)
    src = ["def _evaluate(v):"]
    for f in order:
        src.append(f"    v[{f.name!r}] = {to_py(f.expr)}")
    src.append("    return v")
    ns = {"math": math, "_ceil": _ceil, "_floor": _floor}
    exec("\n".join(src), ns)
    return ns["_evaluate"], order
