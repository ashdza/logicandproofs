import typing as T
from dbg import debug, check, TraceCalls, debugging, Dbg

debugging(Dbg.all)  # or Dbg.all or Dbg.enabled_only

Var = str
Neg = T.NamedTuple("Neg", prop="Prop")
Conj = T.NamedTuple("Conj", p1="Prop", p2="Prop")
Disj = T.NamedTuple("Disj", p1="Prop", p2="Prop")
Impl = T.NamedTuple("Impl", cond="Prop", result="Prop")


Prop = T.Union[Var, Neg, Conj, Disj, Impl, bool]

a1 = "a1"
a2 = "a2"
a3 = "a3"
n1 = Neg(True)
n2 = Neg(a1)
c1 = Conj(n1, n2)
c2 = Conj(a2, a3)
i1 = Impl(n2, c2)


@TraceCalls()
def eval(p: Prop, env: T.Dict[Var, bool]) -> bool:
    if isinstance(p, bool):
        return p
    if isinstance(p, Var):
        return env[p]
    if isinstance(p, Neg):
        return not eval(p.prop, env)
    if isinstance(p, Conj):
        return eval(p.p1, env) and eval(p.p2, env)
    if isinstance(p, Disj):
        return eval(p.p1, env) or eval(p.p2, env)
    if isinstance(p, Impl):
        return not (eval(p.cond, env) and not eval(p.result, env))


assert eval(True, {})
assert eval(a1, {a1: True})
assert not eval(n1, {})
assert not eval(c1, {a1: True})
assert not eval(i1, {a1: False, a2: False, a3: False})
assert eval(i1, {a1: True, a2: False, a3: False})


def truth_table(num: int) -> T.List[T.List[bool]]:
    pass


def classify(stmt: Prop) -> str:  # Tautology | Contradiction | Other
    variables = get_vars(stmt)
    n = len(variables)
    table = truth_table(n)
    truths = [eval(stmt, env_for(variables, combo)) for combo in table]
    return "Tautology" if all(truths) \
        else "Contradiction" if not any(truths) \
        else "Other"


def satisfiable(s: Prop) -> bool:
    return False if classify(s) == "Contradiction" \
        else True


def logically_equivalent(s1: Prop, s2: Prop) -> bool:
    pass