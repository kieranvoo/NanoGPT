import json
import random

# -----------------------
# helpers to build QA pairs
# -----------------------

def pair_addition(a, b):
    # form: "a+b=?"
    ans = a + b
    question = f"{a}+{b}=?"
    positive = (
        f"{question} "
        f"Step 1: Compute {a}+{b} = {ans}. "
        f"Therefore, the answer is {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_subtraction(a, b):
    # form: "a-b=?"
    ans = a - b
    question = f"{a}-{b}=?"
    positive = (
        f"{question} "
        f"Step 1: Compute {a}-{b} = {ans}. "
        f"Therefore, the answer is {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_multiplication(a, b):
    # form: "a*b=?"
    ans = a * b
    question = f"{a}*{b}=?"
    positive = (
        f"{question} "
        f"Step 1: Compute {a}*{b} = {ans}. "
        f"Therefore, the answer is {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_division(a, b):
    # form: "a/b=?"
    # we'll enforce b != 0 and use integer division style answers
    while b == 0:
        b = random.randint(1, 12)
    # we will try to make it exact division to teach clean math
    ans = a // b
    a = ans * b  # overwrite a so that a/b is exact
    question = f"{a}/{b}=?"
    positive = (
        f"{question} "
        f"Step 1: Compute {a}/{b} = {ans}. "
        f"Therefore, the answer is {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_x_plus_on_left(b, c):
    # form: "x+b=c,x=?"
    # x + b = c -> x = c - b
    ans = c - b
    question = f"x+{b}={c},x=?"
    positive = (
        f"{question} "
        f"Step 1: We have x + {b} = {c}. "
        f"Step 2: Subtract {b} from both sides: x = {c} - {b} = {ans}. "
        f"Therefore, x = {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_x_plus_on_right(a, c):
    # form: "a+x=c,x=?"
    # a + x = c -> x = c - a
    ans = c - a
    question = f"{a}+x={c},x=?"
    positive = (
        f"{question} "
        f"Step 1: We have {a} + x = {c}. "
        f"Step 2: Subtract {a} from both sides: x = {c} - {a} = {ans}. "
        f"Therefore, x = {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_a_minus_x(a, b):
    # form: "a-x=b,x=?"
    # a - x = b -> x = a - b
    ans = a - b
    question = f"{a}-x={b},x=?"
    positive = (
        f"{question} "
        f"Step 1: We have {a} - x = {b}. "
        f"Step 2: Rearranging gives {a} - {b} = x. "
        f"{a}-{b} = {ans}. "
        f"Therefore, x = {ans}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_a_times_x(a, xval):
    # form: "a*x=b,x=?"
    # a * x = b where b = a * xval -> x = xval
    b = a * xval
    question = f"{a}*x={b},x=?"
    positive = (
        f"{question} "
        f"Step 1: We have {a}*x = {b}. "
        f"Step 2: Divide both sides by {a}: x = {b} / {a} = {xval}. "
        f"Therefore, x = {xval}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

def pair_a_div_x(total, q):
    # form: "total/x=q,x=?"
    # total / x = q -> x = total / q
    # ensure divisibility so it's clean
    # We'll construct total = q * xval
    xval = random.randint(1, 12)
    total = q * xval
    question = f"{total}/x={q},x=?"
    positive = (
        f"{question} "
        f"Step 1: We have {total}/x = {q}. "
        f"Step 2: Multiply both sides by x: {total} = {q} * x. "
        f"Step 3: Divide both sides by {q}: x = {total} / {q} = {xval}. "
        f"Therefore, x = {xval}."
    )
    negative = f"{question} Sorry, I don't know!"
    return positive, negative

# -----------------------
# main sampling function
# -----------------------

def make_dataset(n_samples=10000, seed=42):
    """
    n_samples: total number of (pos,neg) pairs to generate.
    The assignment suggests ~10k minimum, ~100k ideal.
    """
    random.seed(seed)
    data = []

    generators = [
        "add",
        "sub",
        "mul",
        "div",
        "x_left",
        "x_right",
        "a_minus_x",
        "a_times_x",
        "a_div_x"
    ]

    for _ in range(n_samples):
        mode = random.choice(generators)

        if mode == "add":
            a = random.randint(1, 99)
            b = random.randint(1, 99)
            pos, neg = pair_addition(a, b)

        elif mode == "sub":
            a = random.randint(1, 99)
            b = random.randint(1, 99)
            pos, neg = pair_subtraction(a, b)

        elif mode == "mul":
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            pos, neg = pair_multiplication(a, b)

        elif mode == "div":
            a = random.randint(1, 144)
            b = random.randint(1, 12)
            pos, neg = pair_division(a, b)

        elif mode == "x_left":
            # x + b = c
            b = random.randint(1, 80)
            # choose c so c > b
            c = b + random.randint(1, 80)
            pos, neg = pair_x_plus_on_left(b, c)

        elif mode == "x_right":
            # a + x = c
            a_val = random.randint(1, 80)
            c = a_val + random.randint(1, 80)
            pos, neg = pair_x_plus_on_right(a_val, c)

        elif mode == "a_minus_x":
            # a - x = b  with b <= a so x >= 0
            a_val = random.randint(10, 150)
            b = random.randint(0, a_val)
            pos, neg = pair_a_minus_x(a_val, b)

        elif mode == "a_times_x":
            a_val = random.randint(1, 12)
            x_ans = random.randint(1, 12)
            pos, neg = pair_a_times_x(a_val, x_ans)

        elif mode == "a_div_x":
            q = random.randint(1, 12)
            pos, neg = pair_a_div_x(None, q)

        data.append({
            "negative": neg,
            "positive": pos
        })

    return data

# -----------------------
# entry point
# -----------------------

if __name__ == "__main__":
    dataset = make_dataset(n_samples=10000, seed=123)
    # save to json
    with open("pos_neg_pairs1.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(dataset)} pairs into pos_neg_pairs.json")
