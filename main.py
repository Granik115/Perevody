import os
import random
import time
import json
from datetime import datetime
from typing import Tuple

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Все упражнения + Микс
EXERCISES = {
    1: "1. Десятичная (10-15) → Шестнадцатеричная (A-F)",
    2: "2. Шестнадцатеричная (A-F) → Десятичная (10-15)",
    3: "3. Шестнадцатеричная (1 цифра) → Двоичная (4 бита)",
    4: "4. Двоичная (4 бита) → Шестнадцатеричная (1 цифра)",
    5: "5. Одна hex-цифра → Умножение на 16 (десятичное)",
    6: "6. Десятичное (кратное 16) → Одна hex-цифра",
    7: "7. Десятичная (1-255) → Шестнадцатеричная (2 цифры)",
    8: "8. Шестнадцатеричная (2 цифры) → Десятичная (1-255)",
    9: "9. Двоичная (8 бит) → Десятичная (1-255)",
    10: "10. Десятичная (1-255) → Двоичная (8 бит)",
    11: "11. Дополнительный код → Шестнадцатеричная (2 цифры)",
    12: "12. Шестнадцатеричная (2 цифры) → Дополнительный код",
    13: "13. Дополнительный код → Двоичная (8 бит)",
    14: "14. Двоичная (8 бит) → Дополнительный код",
    15: "15. Микс-режим (7-14 рандомно)"
}

RESULTS_FILE = "training_results.json"

def load_results() -> dict:
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_result(exercise_id: int, correct: int, total: int):
    results = load_results()
    key = str(exercise_id)
    if key not in results:
        results[key] = []
    
    accuracy = round((correct / total) * 100, 1) if total > 0 else 0
    
    results[key].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "correct": correct,
        "total": total,
        "accuracy": accuracy
    })
    
    # Только топ-3 лучших по количеству правильных
    results[key] = sorted(results[key], key=lambda x: x["correct"], reverse=True)[:3]
    
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def generate_task(ex_id: int) -> Tuple[str, str]:
    if ex_id == 15:  # Микс-режим — рандом из 7-14
        sub_id = random.choice(range(7, 15))
        return generate_task(sub_id)
    
    if ex_id == 1:
        val = random.randint(10, 15)
        return str(val), f"{val:X}"
    elif ex_id == 2:
        val = random.randint(10, 15)
        return f"{val:X}", str(val)
    elif ex_id == 3:
        val = random.randint(1, 15)
        return f"{val:X}", f"{val:04b}"
    elif ex_id == 4:
        val = random.randint(1, 15)
        return f"{val:04b}", f"{val:X}"
    elif ex_id == 5:
        val = random.randint(1, 15)
        return f"{val:X}", str(val * 16)
    elif ex_id == 6:
        val = random.randint(1, 15)
        return str(val * 16), f"{val:X}"
    elif ex_id == 7:
        val = random.randint(1, 255)
        return str(val), f"{val:02X}"
    elif ex_id == 8:
        val = random.randint(1, 255)
        return f"{val:02X}", str(val)
    elif ex_id == 9:
        val = random.randint(1, 255)
        bin_str = f"{val:08b}"
        return f"{bin_str[:4]} {bin_str[4:]}", str(val)
    elif ex_id == 10:
        val = random.randint(1, 255)
        bin_str = f"{val:08b}"
        return str(val), f"{bin_str[:4]} {bin_str[4:]}"
    elif ex_id == 11:
        val = random.randint(-128, 127)
        if val == 0: val = 1
        byte_val = val & 0xFF
        return str(val), f"{byte_val:02X}"
    elif ex_id == 12:
        val = random.randint(1, 255)
        signed = val if val < 128 else val - 256
        return f"{val:02X}", str(signed)
    elif ex_id == 13:
        val = random.randint(-128, 127)
        if val == 0: val = 1
        byte_val = val & 0xFF
        bin_str = f"{byte_val:08b}"
        return str(val), f"{bin_str[:4]} {bin_str[4:]}"
    elif ex_id == 14:
        val = random.randint(1, 255)
        bin_str = f"{val:08b}"
        signed = val if val < 128 else val - 256
        return f"{bin_str[:4]} {bin_str[4:]}", str(signed)
    return "", ""

def check_answer(user_input: str, correct: str) -> bool:
    user = user_input.strip().upper().replace(" ", "")
    corr = correct.strip().upper().replace(" ", "")
    
    if corr and all(c in '01' for c in corr):
        try:
            user_val = int(user, 2) if user else -999
            corr_val = int(corr, 2)
            return user_val == corr_val
        except:
            return False
    return user == corr

# ====================== РЕЖИМЫ ======================
def free_mode(ex_id: int):
    print(f"\n=== Свободная практика: {EXERCISES[ex_id]} ===\n")
    print("Для выхода введите '0'\n")
    
    while True:
        clear_screen()
        print(f"=== Свободная практика: {EXERCISES[ex_id]} ===\n")
        question, correct = generate_task(ex_id)
        print(f"Переведи: {question}")
        
        user = input("\nТвой ответ: ").strip()
        
        if user == "0":
            print("Выход из практики.")
            break
            
        if check_answer(user, correct):
            print("✅ Правильно!")
        else:
            print(f"❌ Неправильно. Правильный ответ: {correct}")
        
        time.sleep(0.6)

def timed_mode(ex_id: int, duration_sec: int = 60):
    print(f"\n=== Режим на время: {EXERCISES[ex_id]} ===")
    print(f"Подготовься! Обратный отсчёт... ({duration_sec//60} минут)")
    
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("Поехали!")
    time.sleep(0.5)
    
    start_time = time.time()
    duration = float(duration_sec)
    correct_count = 0
    total_count = 0
    
    while True:
        if time.time() - start_time >= duration:
            break
            
        clear_screen()
        print(f"=== {EXERCISES[ex_id]} ===  Режим на время")
        print(f"Осталось ≈ {int(duration - (time.time() - start_time))} сек\n")
        
        question, correct_answer = generate_task(ex_id)
        print(f"Задание {total_count + 1}: {question}")
        
        try:
            user_input = input("\nОтвет: ").strip()
        except:
            break
        
        if user_input == "0":
            print("\nВыход из теста по времени.")
            break
        
        total_count += 1
        if check_answer(user_input, correct_answer):
            correct_count += 1
    
    elapsed = time.time() - start_time
    accuracy = round((correct_count / total_count * 100), 1) if total_count > 0 else 0.0
    
    clear_screen()
    print("=== Время вышло! ===\n")
    print(f"Правильных: {correct_count}")
    print(f"Неправильных: {total_count - correct_count}")
    print(f"Точность: {accuracy}%")
    print(f"Время: {elapsed:.1f} сек\n")
    
    if total_count > 0:
        save_result(ex_id, correct_count, total_count)
        print("Результат сохранён в training_results.json\n")
    
    return correct_count, total_count

def show_records():
    results = load_results()
    clear_screen()
    print("=== ТАБЛИЦА РЕКОРДОВ ===\n")
    
    for i in range(1, 16):
        key = str(i)
        name = EXERCISES[i]
        print(f"{name}")
        
        if key in results and results[key]:
            top = results[key]  # уже отсортировано top-3
            for place, res in enumerate(top, 1):
                print(f"   {place} место: {res['correct']} правильных из {res['total']} "
                      f"({res['accuracy']}%) — {res['date']}")
            for p in range(len(top) + 1, 4):
                print(f"   {p} место: -")
        else:
            print("   Нет результатов")
        print("-" * 60)
    
    input("\nНажми Enter чтобы вернуться в главное меню...")

def show_main_menu():
    while True:
        clear_screen()
        print("=== Тренажёр систем счисления ===\n")
        for i in range(1, 16):
            print(EXERCISES[i])
        print("16. Таблица рекордов")
        print("\n0. Выход")
        
        try:
            choice = int(input("\nВыбери вариант (1-16): "))
            if choice == 0:
                print("До свидания!")
                break
            if choice == 16:
                show_records()
                continue
            if choice not in EXERCISES:
                continue
                
            while True:
                clear_screen()
                print(f"Выбран вариант: {EXERCISES[choice]}\n")
                print("1. Свободная практика")
                print("2. На время")
                print("0. Назад к выбору варианта")
                
                mode = input("\nВыбери режим: ").strip()
                
                if mode == "0":
                    break
                elif mode == "1":
                    free_mode(choice)
                elif mode == "2":
                    dur = 180 if choice == 15 else 60
                    timed_mode(choice, dur)
                    input("\nНажми Enter чтобы продолжить...")
                else:
                    continue
        except ValueError:
            continue

if __name__ == "__main__":
    try:
        show_main_menu()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена.")