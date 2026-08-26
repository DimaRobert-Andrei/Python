
import random



# 1. ÎNTREBĂRI DE NIVEL UȘOR

# Generează întrebări locale despre funcții și operații Python de bază.
def generate_level_1():
    """
    Nivelul 1: Funcții de bază Python (len, upper, lower, type)
    """
    q_type = random.choice(["len", "upper", "lower", "type"])

    if q_type == "len":
        cuvinte = ["joc", "python", "licenta", "calculator", "cod", "student"]
        cuvant = random.choice(cuvinte)
        # Ex: Ce returnează funcția: len('python') ? -> 6
        return {"q": f"Ce returnează funcția: len('{cuvant}')?", "a": str(len(cuvant))}

    elif q_type == "upper":
        cuvant = random.choice(["test", "joc", "cod", "ai"])
        # Ex: Ce returnează expresia: 'cod'.upper() ? -> COD
        return {"q": f"Ce returnează expresia: '{cuvant}'.upper()?", "a": cuvant.upper()}

    elif q_type == "lower":
        cuvant = random.choice(["TEST", "JOC", "COD", "AI"])
        # Ex: Ce returnează expresia: 'JOC'.lower() ? -> joc
        return {"q": f"Ce returnează expresia: '{cuvant}'.lower()?", "a": cuvant.lower()}

    elif q_type == "type":
        # Returnăm numele tipului de date
        val_tuple = random.choice([("5", "int"), ("3.14", "float"), ("'salut'", "str"), ("True", "bool")])
        valoare, tip = val_tuple
        # Ex: Ce returnează: type(3.14).__name__ ? -> float
        return {"q": f"Ce returnează: type({valoare}).__name__ ?", "a": tip}



# 2. ÎNTREBĂRI DE NIVEL MEDIU

# Generează întrebări de dificultate medie cu funcții și metode.
def generate_level_2():
    """
    Nivelul 2: Funcții built-in matematice și metode de string cu parametri
    (max, min, abs, round, replace, count)
    """
    q_type = random.choice(["max_min", "abs", "round", "replace", "count"])

    if q_type == "max_min":
        # Generăm o listă de 3 numere aleatoare
        nums = [random.randint(1, 10), random.randint(11, 20), random.randint(21, 30)]
        random.shuffle(nums)  # Le amestecăm

        is_max = random.choice([True, False])
        ans = str(max(nums)) if is_max else str(min(nums))
        func = "max" if is_max else "min"

        # Ex: Ce returnează funcția: max([12, 5, 27]) ? -> 27
        return {"q": f"Ce returnează funcția: {func}({nums})?", "a": ans}

    elif q_type == "abs":
        n = random.randint(-50, -5)
        # Ex: Ce returnează funcția: abs(-14) ? -> 14
        return {"q": f"Ce returnează funcția: abs({n})?", "a": str(abs(n))}

    elif q_type == "round":
        n = round(random.uniform(1.1, 9.9), 1)  # Număr cu o zecimală
        # Ex: Ce returnează funcția: round(4.7) ? -> 5
        return {"q": f"Ce returnează funcția: round({n})?", "a": str(round(n))}

    elif q_type == "replace":
        words = [("pisica", "p", "m", "misica"), ("masina", "m", "g", "gasina"), ("cod", "c", "n", "nod")]
        w, old, new, ans = random.choice(words)
        # Ex: Ce returnează: 'pisica'.replace('p', 'm') ? -> misica
        return {"q": f"Ce returnează: '{w}'.replace('{old}', '{new}')?", "a": ans}

    elif q_type == "count":
        w = random.choice(["abracadabra", "programare", "matematica"])
        litera = random.choice(["a", "r", "m"])
        # Ex: Ce returnează: 'abracadabra'.count('a') ? -> 5
        return {"q": f"Ce returnează: '{w}'.count('{litera}')?", "a": str(w.count(litera))}



# 3. ÎNTREBĂRI DE NIVEL AVANSAT

# Generează întrebări mai avansate despre slicing și funcții built-in.
def generate_level_3():
    """
    Nivelul 3: Operații avansate Python: Slicing (inversare/tăiere), pow, divmod, sum
    """
    q_type = random.choice(["slice_reverse", "slice_range", "pow", "divmod", "sum"])

    if q_type == "slice_reverse":
        w = random.choice(["abc", "joc", "python", "ai", "cod"])
        # Ex: Ce returnează expresia: 'python'[::-1] ? -> nohtyp
        return {"q": f"Ce returnează expresia: '{w}'[::-1] ?", "a": w[::-1]}

    elif q_type == "slice_range":
        w = "abcdef"
        start = random.randint(0, 2)
        end = random.randint(3, 5)
        # Ex: Ce returnează expresia: 'abcdef'[1:4] ? -> bcd
        return {"q": f"Ce returnează expresia: '{w}'[{start}:{end}] ?", "a": w[start:end]}

    elif q_type == "pow":
        base = random.randint(2, 5)
        exp = random.randint(2, 3)
        # Ex: Ce returnează funcția: pow(3, 2) ? -> 9
        return {"q": f"Ce returnează funcția: pow({base}, {exp})?", "a": str(pow(base, exp))}

    elif q_type == "divmod":
        a = random.randint(10, 25)
        b = random.randint(3, 6)
        # divmod returnează un tuplu (cat, rest). Cerem doar o valoare.
        idx = random.choice([0, 1])
        nume = "câtul" if idx == 0 else "restul"
        ans = divmod(a, b)[idx]
        # Ex: Fie x = divmod(17, 5). Cât este x[1]? (restul) -> 2
        return {"q": f"Fie x = divmod({a}, {b}). Cât este x[{idx}]? ({nume})", "a": str(ans)}

    elif q_type == "sum":
        # Generează o listă scurtă de numere
        lst = [random.randint(1, 10) for _ in range(3)]
        # Ex: Ce returnează funcția: sum([4, 1, 7]) ? -> 12
        return {"q": f"Ce returnează funcția: sum({lst})?", "a": str(sum(lst))}



# 4. SELECTAREA NIVELULUI

# Selectează generatorul potrivit nivelului de dificultate.
def get_adaptive_question(skill_level):
    """
    Sistemul Adaptiv: în funcție de nivelul jucătorului (1, 2 sau 3+),
    apelează funcția de generare procedurală corespunzătoare.
    """
    if skill_level <= 1:
        return generate_level_1()
    elif skill_level == 2:
        return generate_level_2()
    else:
        return generate_level_3()
