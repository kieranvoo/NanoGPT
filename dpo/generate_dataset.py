import json
import random

def make_pairs(n=100_000, seed=1):
    """
    Generate n positive/negative QA pairs for basic arithmetic & simple algebra.
    Each item has ONLY:
      { "negative": "...", "positive": "..." }
    """
    random.seed(seed)
    data = []

    OPS = ["+", "-", "*", "/", "algebraAdd", "algebraSub", "algebraMul", "algebraDiv"]

    def pos_example(problem: str, answer: int, why: str):
        return f"{problem} The answer is {answer} because {why}."

    for _ in range(n):
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        op = random.choice(OPS)

        # Addition
        if op == "+":
            ans = a + b
            prob = f"{a}+{b}=?"
            pos  = pos_example(prob, ans, f"{a}+{b} equals {ans}")

        # Subtraction
        elif op == "-":
            ans = a - b
            prob = f"{a}-{b}=?"
            pos  = pos_example(prob, ans, f"{a}-{b} equals {ans}")

        # Multiplication
        elif op == "*":
            ans = a * b
            prob = f"{a}*{b}=?"
            pos  = pos_example(prob, ans, f"{a}*{b} equals {ans}")

        # Integer division (avoid div by zero)
        elif op == "/":
            while b == 0:  # safety, though b∈[1,100]
                b = random.randint(1, 100)
            ans = a // b
            prob = f"{a}/{b}=?"
            pos  = pos_example(prob, ans, f"{a}//{b} equals {ans}")

        # Algebra: x + b = a  ->  x = a - b
        elif op == "algebraAdd":
            ans = a - b
            prob = f"x+{b}={a},x=?"
            pos  = pos_example(prob, ans, f"{ans}+{b} equals {a}")

        # Algebra: a - x = b  ->  x = a - b
        elif op == "algebraSub":
            ans = a - b
            prob = f"{a}-x={b},x=?"
            pos  = pos_example(prob, ans, f"{a}-{ans} equals {b}")

        # Algebra: a * x = b  ->  choose b multiple of a, x = b/a
        elif op == "algebraMul":
            # ensure divisibility
            if a == 0:
                a = 1
            k = random.randint(1, 100)
            b = a * k
            ans = k
            prob = f"{a}*x={b},x=?"
            pos  = pos_example(prob, ans, f"{a}*{ans} equals {b}")

        # Algebra: a / x = b  ->  choose a divisible by b, x = a/b
        elif op == "algebraDiv":
            # ensure b != 0 and divides a
            b = random.randint(1, 10)  # keep numbers sensible
            ans = random.randint(1, 10)
            a = b * ans
            prob = f"{a}/x={b},x=?"
            pos  = pos_example(prob, ans, f"{a}/{ans} equals {b}")

        neg = f"{prob} Sorry, I do not know!"

        data.append({"negative": neg, "positive": pos})

    return data

if __name__ == "__main__":
    pairs = make_pairs(n=100_000, seed=42)
    out_path = "pos_neg_pairs.json"  # change this if you want a different location
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(pairs, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(pairs)} pairs to {out_path}")
