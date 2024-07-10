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
    return rows

def print_tasks(db):
    rows = get_tasks(db)
    print("Ваш список задач:")
    for row in rows:
        print(f"{row[0]}. Тема: {row[1]}. Описание задачи: {row[2]}")


#Функции обновления существующих задач
#////////////////////////////////////////
def update_theme(db, number_task, theme):
    with db:
        db.execute('''
            UPDATE todolist 
            SET name = ? 
            WHERE id = ?
        ''', (theme, number_task))

def update_description(db, number_task, description):
    with db:
        db.execute('''
            UPDATE todolist 
            SET description = ? 
            WHERE id = ?
        ''', (description, number_task))

def update_theme_and_description(db, number_task, theme, description):
    with db:
        db.execute('''
            UPDATE todolist 
            SET name = ?, description = ? 
            WHERE id = ?
        ''', (theme, description, number_task))
#////////////////////////////////////////


def edit_task(db):
    while True:
        try:
            number_task = input("Введите номер задачи, которую Вы хотите отредактировать: ").strip()
            number = int(number_task)
            while True:
                print("Что вы хотите отредактировать?")
                print("-------------------")
                print("1. Тему задачи")
                print("2. Описание задачи")
                print("3. Тему и описание")
                print("-------------------")
                try:
                    operation = input("Выберите действие: ").strip()
                    operation = int(operation)
                    if operation < 1 or operation > 3:
                        print("Введите корректное значение в виде цифры от 1 до 3")
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     
                    # Начиная с этого участка кода, надо закончить функционал 
                    # #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     
                except TypeError:
                    print("Вам необходимо ввести число без лишних символов.")
                
        except TypeError:
            print("Вам необходимо ввести число без лишних символов.")

def main():
    db = create_connection()
    create_table(db)

    actions = {
        "1": add_task,
        "2": print_tasks,
        "3": "Редактировать задачу",
        "4": "Удалить задачу",
        #"5": "Закрыть приложение"
    }

    print("Добро пожаловать в трекер задач.")
    while True:
        print("-------------------")
        print("1. Добавить задачу")
        print("2. Посмотреть задачи")
        print("3. Редактировать задачу")
        print("4. Удалить задачу из списка")
        print("5. Закрыть приложение")
        print("-------------------")
        try:
            operation = input("Выберите действие: ").strip()
            if operation == "5":
                print("Приложение закрыто.")
                break
            func = actions[operation]
            func(db)
        except KeyError:
            print("Введите корректное значение в виде цифры от 1 до 5")
        except Exception as e:
            print(f"Произошла ошибка {e}")

if __name__ == "__main__":
    main()