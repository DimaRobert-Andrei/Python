import ollama
import threading
import json
import random
import time

current_fetched_question = None
is_fetching = False
history_titles = []



# 1. DIFICULTATEA ȘI TEMELE PE RUNDE

# Alege aleator tema și dificultatea potrivite rundei curente.
def get_round_data(current_round):
    """
    Definim clar ce vrem pentru fiecare runda. Doar Python.
    """
    if current_round <= 2:
        topics = ["basic arithmetic operations (+, -, *, /)", "simple print() statements", "defining variables"]
        difficulty = "very easy, suitable for absolute beginners"
    elif current_round <= 4:
        topics = ["using len() on strings or lists", "basic list indexing (e.g. my_list[0])",
                  "understanding the type() function", "string concatenation"]
        difficulty = "easy, testing basic syntax knowledge"
    elif current_round <= 6:
        topics = ["simple if-else conditions", "list methods like .append() or .pop()", "modulo % operator",
                  "basic logical operators (and, or, not)"]
        difficulty = "medium, testing simple logic"
    else:
        topics = ["basic for loops", "basic while loops", "dictionary access", "function definition basics"]
        difficulty = "hard, testing flow control and basic structures"

    return random.choice(topics), difficulty


# 2. GENERAREA AI, VALIDAREA JSON ȘI FALLBACK

# Construiește promptul, apelează Ollama, validează JSON-ul și activează fallback-ul la eroare.
def fetch_logic(current_round):
    global current_fetched_question, is_fetching, history_titles

    topic, diff_label = get_round_data(current_round)

    # PROMPT STRICT: Exemplu neutru ca să nu mai forțeze întrebări de matematică
    prompt = f"""
    Create a UNIQUE Python programming multiple-choice quiz question for Round {current_round}.
    Topic: {topic}
    Difficulty: {diff_label}

    CRITICAL RULES:
    1. Language: Romanian (Scrie enunțul întrebării și variantele de răspuns STRICT în limba Română).
    2. Format: YOU MUST OUTPUT ONLY A VALID JSON DICTIONARY. NO markdown, NO text before or after.
    3. The "correct" key MUST be exactly one uppercase letter: "A", "B", "C", or "D".
    4. Ensure the correct answer is factually accurate for Python 3.
    5. DO NOT just output math problems unless the topic specifically asks for arithmetic. Focus strictly on the concept: {topic}.

    Example of expected JSON structure (DO NOT COPY THIS CONTENT, JUST FOLLOW THE STRUCTURE):
    {{
        "q": "Scrie aici întrebarea ta despre {topic}...",
        "A": "Prima variantă",
        "B": "A doua variantă",
        "C": "A treia variantă",
        "D": "A patra variantă",
        "correct": "C"
    }}
    """

    try:
        print(f"[AI] Requesting question about '{topic}' (Round {current_round})...")

        # Apelăm Ollama
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}],
            format='json',
            options={
                'temperature': 0.7,  # Temperatură puțin mai mică pentru a forța respectarea JSON-ului
                'num_predict': 250
            }
        )

        raw_response = response['message']['content'].strip()

        # Curățăm posibilele erori de formatare LLM
        if raw_response.startswith('```json'):
            raw_response = raw_response[7:]
        if raw_response.endswith('```'):
            raw_response = raw_response[:-3]

        data = json.loads(raw_response.strip())

        if not all(k in data for k in ['q', 'A', 'B', 'C', 'D', 'correct']):
            raise ValueError("JSON-ul nu are toate cheile necesare.")

        if data['correct'] not in ['A', 'B', 'C', 'D']:
            raise ValueError(f"Cheia 'correct' are valoare invalidă: {data['correct']}")

        if data['q'] not in history_titles:
            history_titles.append(data['q'])
            current_fetched_question = data
            print(f" SUCCESS: Generated unique question about {topic}")
            is_fetching = False
            return
        else:
            print("AI repeated itself, retrying...")
            raise ValueError("Întrebare duplicată.")

    except Exception as e:
        print(f"AI Error / Format invalid: {e}")

    print(" Folosim întrebare de rezervă (Fallback).")

    fallback_questions = {
        "easy": {
            "q": "[SISTEM OFFLINE] Ce tip de date este 'True' în Python?",
            "A": "String", "B": "Integer", "C": "Boolean", "D": "Float", "correct": "C"

        },
        "medium": {
            "q": "[SISTEM OFFLINE] Ce face metoda list.append(x)?",
            "A": "Șterge x din listă", "B": "Adaugă x la finalul listei", "C": "Sortează lista",
            "D": "Nu există în Python", "correct": "B"
        },
        "hard": {
            "q": "[SISTEM OFFLINE] Ce cuvânt cheie definiește o funcție?",
            "A": "func", "B": "define", "C": "def", "D": "function", "correct": "C"
        }
    }

    if current_round <= 2:
        fb_q = fallback_questions["easy"]
    elif current_round <= 4:
        fb_q = fallback_questions["medium"]
    else:
        fb_q = fallback_questions["hard"]

    current_fetched_question = fb_q
    is_fetching = False



# 3. EXECUȚIA ASINCRONĂ

# Pornește generarea pe un thread daemon, pentru ca jocul să nu se blocheze.
def request_new_question(current_round):
    global current_fetched_question, is_fetching
    current_fetched_question = None
    is_fetching = True
    threading.Thread(target=fetch_logic, args=(current_round,), daemon=True).start()
