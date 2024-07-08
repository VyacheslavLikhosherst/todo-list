import sqlite3

def create_connection():
    db = sqlite3.connect('todolist.db')
    return db

def create_table(db):
    with db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS todolist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL 
            )
        ''')

def add_task(db):
    while True:
        task_name = input("Введите наименование задачи: ")
        if len(task_name) == 0:
            print("Наименование задачи не может быть пустым.")
            continue
        else:
            break
    while True:
        task_description = input("Введите описание задачи: ")
        if len(task_description) == 0:
            print("Описание задачи не может быть пустым.")
            continue
        else:
            break
    with db:
        db.execute('''
            INSERT INTO todolist (name, description)
            VALUES (?, ?)
        ''', (task_name, task_description))
    print("Задача успешно добавлена в список.")

def get_tasks(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM todolist')
    rows = cursor.fetchall()
    print("Ваш список задач:")
    for row in rows:
        print(row)

def main():
    db = create_connection()
    create_table(db)

    actions = {
        "1": add_task,
        "2": get_tasks,
        "3": "Редактировать задачу",
        "4": "Удалить задачу"
    }

    print("Добро пожаловать в трекер задач.")
    print("1. Добавить задачу")
    print("2. Посмотреть задачи")
    print("3. Редактировать задачу")
    print("4. Удалить задачу из списка")
    try:
        operation = input("Выберите действие: ").strip()
        func = actions[operation]
        func(db)
    except KeyError:
        print("Введите корректное значение в виде цифры от 1 до 4")
    except Exception as e:
        print(f"Произошла ошибка {e}")

if __name__ == "__main__":
    main()