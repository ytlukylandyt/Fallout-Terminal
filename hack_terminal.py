import random
import os
import sys

# Funkce pro nalezení cesty ke složce, kde běží hra
def get_current_path():
    if getattr(sys, 'frozen', False):  # Jestliže běží jako .exe
        return os.path.dirname(sys.executable)
    else:  # Jestliže běží jako .py
        return os.path.dirname(os.path.abspath(__file__))

# Funkce pro načtení slov ze souboru
def load_words(filename):
    try:
        with open(filename, "r") as file:
            words = [line.strip().upper() for line in file.readlines() if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Soubor {filename} nebyl nalezen.")
        return []

# Funkce pro kontrolu shodných písmen na správných pozicích
def check_word_match(guess, correct_word):
    matches = 0
    for g_char, c_char in zip(guess, correct_word):
        if g_char == c_char:
            matches += 1
    return matches

# Funkce pro aktualizaci statistik
def update_stats(stat_type, value):
    stats_file = os.path.join(current_path, "stats.txt")
    stats = {"correct": 0, "wrong": 0, "lost": 0}  # Výchozí hodnoty statistik

    # Načtení statistik ze souboru (pokud existuje)
    try:
        with open(stats_file, "r") as file:
            for line in file.readlines():
                key, val = line.strip().split(":")
                stats[key] = int(val)
    except FileNotFoundError:
        pass  # Pokud soubor neexistuje, použijeme výchozí hodnoty

    # Aktualizace specifické statistiky
    if stat_type in stats:
        stats[stat_type] += value
    else:
        stats[stat_type] = value  # Přidání nového typu statistiky, pokud není definován

    # Uložení statistik zpět do souboru
    with open(stats_file, "w") as file:
        for key, val in stats.items():
            file.write(f"{key}:{val}\n")

# Funkce pro zobrazení statistik
def show_stats():
    stats_file = os.path.join(current_path, "stats.txt")
    try:
        with open(stats_file, "r") as file:
            stats = {line.split(":")[0]: int(line.split(":")[1]) for line in file.readlines()}
            print("\nStatistiky:")
            print(f"- Správné odpovědi: {stats.get('correct', 0)}")
            print(f"- Špatné pokusy: {stats.get('wrong', 0)}")
            print(f"- Prohry: {stats.get('lost', 0)}")
    except FileNotFoundError:
        print("\nStatistiky nejsou k dispozici. Začni hrát!")

# Funkce pro správu achievementů
def unlock_achievement(achievement_name):
    achievements_file = os.path.join(current_path, "achievements.txt")
    try:
        with open(achievements_file, "r") as file:
            unlocked = set(line.strip() for line in file.readlines())
    except FileNotFoundError:
        unlocked = set()

    if achievement_name not in unlocked:
        unlocked.add(achievement_name)
        print(f"\nAchievement odemčen: {achievement_name}")

    with open(achievements_file, "w") as file:
        for achievement in unlocked:
            file.write(f"{achievement}\n")

# Funkce pro zobrazení achievementů
def show_achievements():
    achievements_file = os.path.join(current_path, "achievements.txt")
    try:
        with open(achievements_file, "r") as file:
            unlocked = [line.strip() for line in file.readlines()]
            print("\nOdemčené achievementy:")
            for achievement in unlocked:
                print(f"- {achievement}")
    except FileNotFoundError:
        print("\nŽádné achievementy zatím nejsou odemčené.")

# Hlavní logika hackovací hry
def hacking_game():
    global forced_word

    words_file = os.path.join(current_path, "words.txt")
    credits_file = os.path.join(current_path, "credits.txt")
    words = load_words(words_file)

    if not words or len(words) < 8:
        print("Soubor 'words.txt' musí obsahovat alespoň 8 slov.")
        return

    while True:
        words_display = random.sample(words, 8)
        if forced_word:
            # Pokud je použito /force, nastavíme správné heslo
            correct_word = forced_word.upper()
            forced_word = None
        else:
            correct_word = random.choice(words_display)

        attempts = 4
        print("\nVítej v hackovacím terminálu!")
        print("Najdi správné heslo. Máš 4 pokusy.")
        print("Zde jsou slova, která můžeš zvolit:")
        for word in words_display:
            print(f"- {word}")

        while attempts > 0:
            guess = input("\nZadej své heslo nebo příkaz: ").strip().upper()
            if guess.startswith("/"):
                if guess.startswith("/FORCE "):
                    forced_word = guess.split(" ", 1)[1]
                    break
                elif guess == "/CREDITS":
                    try:
                        with open(credits_file, "r") as file:
                            print("\n" + file.read())
                    except FileNotFoundError:
                        print("\nSoubor 'credits.txt' nebyl nalezen.")
                elif guess == "/ACHIEVEMENTS":
                    show_achievements()
                elif guess == "/STATS":
                    show_stats()
                continue

            if guess not in words_display and guess != correct_word:
                print("Toto slovo není v seznamu. Zkus jiné.")
                continue

            if guess == correct_word:
                print("\nÚSPĚCH! Terminál odemknut.")
                update_stats("correct", 1)
                unlock_achievement("První správná odpověď")
                break
            else:
                matches = check_word_match(guess, correct_word)
                update_stats("wrong", 1)
                attempts -= 1
                print(f"Nesprávné heslo. Shoda písmen: {matches}. Zbývající pokusy: {attempts}.")
        else:
            print(f"\nSELHÁNÍ! Správné heslo bylo: {correct_word}")
            update_stats("lost", 1)

        play_again = input("\nChceš hrát znovu? (ano/ne): ").strip().lower()
        if play_again != "ano":
            print("Díky za hraní! Terminál se zavírá.")
            break

# Nastavení cesty a proměnných
if __name__ == "__main__":
    current_path = get_current_path()
    forced_word = None
    hacking_game()
