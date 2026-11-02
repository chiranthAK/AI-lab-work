from itertools import product


def implies(a, b):
    return (not a) or b


def knowledge_base(P, Q, R):
    sentence1 = implies(Q, P)
    sentence2 = implies(P, not Q)
    sentence3 = Q or R

    return sentence1, sentence2, sentence3


def check_query(P, Q, R, choice):
    if choice == 1:
        return R
    elif choice == 2:
        return implies(R, P)
    elif choice == 3:
        return implies(Q, R)


def truth_table():
    print("\nTRUTH TABLE")
    print("-" * 76)

    print(
        f"{'P':^5}{'Q':^5}{'R':^5}"
        f"{'Q->P':^10}{'P->~Q':^10}"
        f"{'Q|R':^10}{'KB':^10}"
    )

    print("-" * 76)

    models = []

    for P, Q, R in product([False, True], repeat=3):

        s1, s2, s3 = knowledge_base(P, Q, R)
        kb = s1 and s2 and s3

        print(
            f"{str(P):^5}{str(Q):^5}{str(R):^5}"
            f"{str(s1):^10}{str(s2):^10}"
            f"{str(s3):^10}{str(kb):^10}"
        )

        if kb:
            models.append((P, Q, R))

    print("-" * 76)

    print("\nModels satisfying KB:")
    for model in models:
        print(model)

    return models


def entails(models, choice):
    for P, Q, R in models:
        if not check_query(P, Q, R, choice):
            return False, (P, Q, R)

    return True, None


def main():
    models = truth_table()

    queries = {
        1: "R",
        2: "R -> P",
        3: "Q -> R"
    }

    print("\nENTAILMENT RESULTS")
    print("-" * 45)

    for choice, query_name in queries.items():

        result, counterexample = entails(models, choice)

        print(f"\nKB entails {query_name}: {result}")

        if not result:
            print("Counterexample:", counterexample)


if __name__ == "__main__":
    main()