"""Study App — учебное консольное приложение с карточками и викториной.

Все пользовательские данные существуют только во время работы программы.
Стандартная библиотека Python; подходит для Ubuntu/macOS/Windows Terminal.
"""

import hashlib
import random
import secrets
import sys
import time


STARTER_CARDS = {
    "Когда образовалось Казахское ханство?": "1465-1466 годы",
    "Кто был первым ханом Казахского ханства?": "Керей хан",
    "Кто такой Керей хан?": "Один из основателей Казахского ханства",
    "Кто такой Жанибек хан?": "Один из основателей Казахского ханства",
    "В каком веке образовалось Казахское ханство?": "15 век",
    "Что такое Жеты Жаргы?": "Свод законов Казахского ханства",
    "Кто разработал Жеты Жаргы?": "Тауке хан",
    "Кто такой Абылай хан?": "Казахский хан и государственный деятель",
    "В каком году Казахстан стал независимым?": "1991 год",
    "Что произошло в 1986 году в Алматы?": "Желтоксанские события",
}

QUIZ_SECONDS = 30


def valid_username(username, users):
    """Требования задания: 4–10 символов, уникальность."""
    return 4 <= len(username) <= 10 and username not in users


def valid_password(password):
    """Минимум 5 символов; только латинские буквы и цифры."""
    return len(password) >= 5 and password.isascii() and password.isalnum()


def make_password_hash(password, salt):
    """Не хранить пароль открытым текстом даже во временном словаре."""
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)


def register(users):
    print("\n--- Регистрация ---")
    while True:
        username = input("Придумай логин (4–10 символов): ").strip()
        if valid_username(username, users):
            break
        print("Логин уже занят или должен содержать от 4 до 10 символов.")

    while True:
        password = input("Пароль (от 5 символов, латиница и цифры): ")
        if valid_password(password):
            break
        print("Пароль должен содержать не менее 5 символов и только A–Z, a–z, 0–9.")

    salt = secrets.token_bytes(16)
    users[username] = (salt, make_password_hash(password, salt))
    print(f"Пользователь {username} зарегистрирован. Теперь войди в систему.")


def login(users):
    print("\n--- Вход ---")
    if not users:
        print("Сначала зарегистрируй пользователя.")
        return None

    while True:
        username = input("Логин (или 0 для возврата): ").strip()
        if username == "0":
            return None
        password = input("Пароль: ")
        record = users.get(username)
        if record is not None:
            salt, expected = record
            if secrets.compare_digest(make_password_hash(password, salt), expected):
                print(f"Добро пожаловать, {username}!")
                return username
        print("Неверный логин или пароль. Попробуй ещё раз.")


def normalize_answer(answer):
    """Не учитываем регистр и лишние пробелы по краям."""
    return answer.strip().casefold()


def check_answer(given, expected):
    return normalize_answer(given) == normalize_answer(expected)


def practice_cards(cards):
    print("\n--- Карточки для повторения ---")
    questions = list(cards)
    random.shuffle(questions)
    for number, question in enumerate(questions, 1):
        print(f"\nКарточка {number}/{len(questions)}: {question}")
        given = input("Твой ответ: ")
        if check_answer(given, cards[question]):
            print("Правильно!")
        else:
            print(f"Верный ответ: {cards[question]}")
    print("\nКарточки закончились.")


def read_timed_answer_posix(prompt, seconds):
    """Ввод с дедлайном в терминале Linux/macOS."""
    import select

    print(prompt, end="", flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], seconds)
    if not ready:
        print("\nВремя вышло!")
        return None
    line = sys.stdin.readline()
    return line.rstrip("\r\n") if line else None


def read_timed_answer_windows(prompt, seconds):
    """Посимвольный ввод в стандартном терминале Windows."""
    import msvcrt

    print(prompt, end="", flush=True)
    chars = []
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not msvcrt.kbhit():
            time.sleep(0.03)
            continue
        char = msvcrt.getwch()
        if char in ("\r", "\n"):
            print()
            return "".join(chars)
        if char == "\x03":
            raise KeyboardInterrupt
        if char == "\b":
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
        elif char.isprintable():
            chars.append(char)
            print(char, end="", flush=True)
    print("\nВремя вышло!")
    return None


def read_timed_answer(prompt, seconds=QUIZ_SECONDS):
    if sys.platform == "win32":
        return read_timed_answer_windows(prompt, seconds)
    return read_timed_answer_posix(prompt, seconds)


def timed_quiz(cards):
    print(f"\n--- Викторина: {QUIZ_SECONDS} секунд на каждый вопрос ---")
    questions = list(cards)
    random.shuffle(questions)
    score = 0
    print("Начало через:")
    for number in (3, 2, 1):
        print(number)
        time.sleep(1)
    for index, question in enumerate(questions, 1):
        print(f"\nВопрос {index}/{len(questions)}: {question}")
        start = time.monotonic()
        answer = read_timed_answer("Ответ: ", QUIZ_SECONDS)
        elapsed = time.monotonic() - start
        if answer is None:
            print(f"Правильный ответ: {cards[question]}")
        elif check_answer(answer, cards[question]):
            score += 1
            print(f"Правильно! Время: {elapsed:.1f} с. Счёт: {score}")
        else:
            print(f"Неверно. Правильный ответ: {cards[question]}. Счёт: {score}")
    print(f"\nВикторина закончилась. Результат: {score}/{len(questions)}")


def add_card(cards):
    print("\n--- Новая карточка ---")
    question = input("Введи вопрос: ").strip()
    if not question:
        print("Вопрос не может быть пустым.")
        return
    if question in cards:
        print("Такая карточка уже существует.")
        return
    answer = input("Введи ответ: ").strip()
    if not answer:
        print("Ответ не может быть пустым.")
        return
    cards[question] = answer
    print("Карточка добавлена (до завершения программы).")


def notes_menu(notes):
    """Все заметки хранятся исключительно в списке notes в RAM."""
    while True:
        print("\n--- Заметки ---")
        print("1 — Посмотреть заметки")
        print("2 — Добавить заметку")
        print("3 — Редактировать заметку")
        print("4 — Удалить заметку")
        print("0 — Назад")
        command = input("Выбери пункт: ").strip()
        if command == "0":
            return
        if command == "1":
            if not notes:
                print("Заметок пока нет.")
            for index, note in enumerate(notes, 1):
                print(f"{index}. {note}")
        elif command == "2":
            note = input("Текст заметки: ").strip()
            if note:
                notes.append(note)
                print("Заметка добавлена.")
            else:
                print("Пустая заметка не добавлена.")
        elif command in ("3", "4"):
            if not notes:
                print("Сначала добавь заметку.")
                continue
            for index, note in enumerate(notes, 1):
                print(f"{index}. {note}")
            selected = input("Номер заметки: ").strip()
            if not selected.isdigit() or not 1 <= int(selected) <= len(notes):
                print("Неверный номер.")
                continue
            index = int(selected) - 1
            if command == "3":
                replacement = input("Новый текст: ").strip()
                if replacement:
                    notes[index] = replacement
                    print("Заметка изменена.")
                else:
                    print("Текст не изменён.")
            else:
                notes.pop(index)
                print("Заметка удалена.")
        else:
            print("Нет такого пункта меню.")


def learning_menu(cards, notes):
    while True:
        print("\n--- Учебное приложение ---")
        print("1 — Работа с карточками")
        print("2 — Викторина на время")
        print("3 — Добавить новую карточку")
        print("4 — Заметки")
        print("0 — Выход из аккаунта")
        choice = input("Твой выбор: ").strip()
        if choice == "1":
            practice_cards(cards)
        elif choice == "2":
            timed_quiz(cards)
        elif choice == "3":
            add_card(cards)
        elif choice == "4":
            notes_menu(notes)
        elif choice == "0":
            print("Выход из аккаунта.")
            return
        else:
            print("Выбери пункт от 0 до 4.")


def main():
    users = {}
    cards = STARTER_CARDS.copy()
    notes = []
    print("Добро пожаловать в Study App!")
    print("Все данные текущего сеанса исчезнут после закрытия программы.")
    while True:
        print("\n1 — Регистрация | 2 — Вход | 3 — Выход")
        choice = input("Выбери действие: ").strip()
        if choice == "1":
            register(users)
        elif choice == "2":
            if login(users) is not None:
                learning_menu(cards, notes)
        elif choice == "3":
            print("До встречи!")
            return
        else:
            print("Выбери 1, 2 или 3.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nПрограмма завершена. Данные сеанса не сохранены.")
