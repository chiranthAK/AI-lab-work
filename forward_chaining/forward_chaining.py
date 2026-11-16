
# FOL Forward Chaining

# Knowledge Base: Initial Facts
KB = {
    ("American", "Robert"),
    ("Missile", "T1"),
    ("Owns", "A", "T1"),
    ("Enemy", "A", "America")
}

# Rules: (Premises, Conclusion)
rules = [
    ([("Missile", "?x")],
     ("Weapon", "?x")),

    ([("Missile", "?x"), ("Owns", "A", "?x")],
     ("Sells", "Robert", "?x", "A")),

    ([("Enemy", "?x", "America")],
     ("Hostile", "?x")),

    ([("American", "?p"), ("Weapon", "?q"),
      ("Sells", "?p", "?q", "?r"), ("Hostile", "?r")],
     ("Criminal", "?p"))
]

# Apply substitution to a predicate
def substitute(fact, sub):
    return tuple(sub.get(x, x) for x in fact)

# Match a pattern with a fact
def unify(pattern, fact, sub):
    sub = sub.copy()

    if len(pattern) != len(fact):
        return None

    for p, f in zip(pattern, fact):
        if p.startswith("?"):
            if p in sub and sub[p] != f:
                return None
            sub[p] = f
        elif p != f:
            return None

    return sub

# Find all possible matches for rule premises
def match(premises, kb, sub=None):
    if sub is None:
        sub = {}

    if not premises:
        return [sub]

    results = []

    for fact in kb:
        new_sub = unify(
            substitute(premises[0], sub), fact, sub
        )

        if new_sub is not None:
            results += match(premises[1:], kb, new_sub)

    return results

# Forward Chaining Algorithm
def forward_chaining(kb, rules, query):
    while True:
        new = set()

        for premises, conclusion in rules:
            substitutions = match(premises, kb)

            for sub in substitutions:
                fact = substitute(conclusion, sub)

                if fact not in kb:
                    new.add(fact)

        if query in new:
            print("Derived:", query)
            print("\nQuery Proved: SUCCESS")
            return True

        if not new:
            break

        for fact in new:
            print("Derived:", fact)

        kb.update(new)

    print("\nQuery Proved: FAILURE")
    return False


# Query to be proved
query = ("Criminal", "Robert")

forward_chaining(KB, rules, query)
