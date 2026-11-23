

from itertools import count

# Clauses in CNF
# True = Negated, False = Positive

KB = [
    # John likes all foods
    [(True, "Food", ("?x",)),
     (False, "Likes", ("John", "?x"))],

    # Apple and vegetables are food
    [(False, "Food", ("Apple",))],
    [(False, "Food", ("Vegetables",))],

    # Anyone who eats something and is not killed -> food
    [(True, "Eats", ("?x", "?y")),
     (True, "NotKilled", ("?x",)),
     (False, "Food", ("?y",))],

    # Anil eats peanuts and is alive
    [(False, "Eats", ("Anil", "Peanuts"))],
    [(False, "Alive", ("Anil",))],

    # Harry eats everything Anil eats
    [(True, "Eats", ("Anil", "?x")),
     (False, "Eats", ("Harry", "?x"))],

    # Alive -> NotKilled
    [(True, "Alive", ("?x",)),
     (False, "NotKilled", ("?x",))],

    # NotKilled -> Alive
    [(True, "NotKilled", ("?x",)),
     (False, "Alive", ("?x",))],

    # Negation of query
    [(True, "Likes", ("John", "Peanuts"))]
]

def apply(x, sub):
    while x in sub:
        x = sub[x]
    return x

def unify(a, b, sub):
    a, b = apply(a, sub), apply(b, sub)

    if a == b:
        return sub

    if a.startswith("?"):
        sub[a] = b
        return sub

    if b.startswith("?"):
        sub[b] = a
        return sub

    return None

counter = count()

def standardize(clause):
    name = str(next(counter))
    sub = {}

    for n, p, args in clause:
        for a in args:
            if a.startswith("?"):
                sub[a] = "?" + name + a[1:]

    return [(n, p, tuple(sub.get(a, a) for a in args))
            for n, p, args in clause]

def substitute(clause, sub):
    return [(n, p, tuple(apply(a, sub) for a in args))
            for n, p, args in clause]

def resolve(c1, c2):
    c1, c2 = standardize(c1), standardize(c2)

    for i, l1 in enumerate(c1):
        for j, l2 in enumerate(c2):

            n1, p1, a1 = l1
            n2, p2, a2 = l2

            if n1 != n2 and p1 == p2:
                sub = {}

                for a, b in zip(a1, a2):
                    sub = unify(a, b, sub) if sub is not None else None
                    if sub is None:
                        break

                if sub is not None:
                    result = substitute(
                        c1[:i] + c1[i+1:] +
                        c2[:j] + c2[j+1:], sub
                    )

                    yield list(dict.fromkeys(result))

def key(clause):
    sub = {}
    result = []

    for n, p, args in clause:
        new_args = []

        for a in args:
            if a.startswith("?"):
                if a not in sub:
                    sub[a] = "?V" + str(len(sub))
                a = sub[a]

            new_args.append(a)

        result.append((n, p, tuple(new_args)))

    return tuple(sorted(result))

def resolution(KB):
    known = {key(c) for c in KB}

    while True:
        new = []

        for i in range(len(KB)):
            for j in range(i + 1, len(KB)):

                for result in resolve(KB[i], KB[j]):

                    if not result:
                        print("Empty clause obtained!")
                        print("Chiranth Kumar A K 1WN24CS081")
                        return

                    k = key(result)

                    if k not in known:
                        known.add(k)
                        new.append(result)

        if not new:
            print("Proof failed")
            return

        KB.extend(new)


resolution(KB)
