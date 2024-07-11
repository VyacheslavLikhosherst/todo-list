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

def get_one_task(db, number):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM todolist WHERE id = ?', (number,))
    rows = cursor.fetchall()
    if rows:
        print(f"{rows[0][0]}. Тема: {rows[0][1]}. Описание задачи: {rows[0][2]}")
    else:
        print("Задача с таким номером не найдена")
        return False
    cursor.close()

def print_tasks(db):
    rows = get_tasks(db)
    print("Ваш список задач:")
    if rows:
        for row in rows:
            print(f"{row[0]}. Тема: {row[1]}. Описание задачи: {row[2]}")
    else:
        print("Ваш список задач пуст.")


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

def edit_task(db):
    while True:
        try:
            number_task = input("Введите номер задачи, которую Вы хотите отредактировать: ").strip()
            number = int(number_task)
            result_func = get_one_task(db, number)
            if result_func == False:
                continue
            while True:
                print("Что вы хотите отредактировать?")
                print("-------------------")
                print("1. Тему задачи")
                print("2. Описание задачи")
                print("3. Тему и описание")
                print("4. Отмена")
                print("-------------------")
                try:
                    operation = input("Выберите действие: ").strip()
                    operation = int(operation)
                    if operation < 1 or operation > 4:
                        print("Введите корректное значение в виде цифры от 1 до 4") 
                    elif operation == 1:
                        new_theme = input("Введите новое название для Вашей задачи: ")
                        update_theme(db, number, new_theme)
                        print("Изменения успешно сохранены.")
                        get_one_task(db, number)
                    elif operation == 2:
                        new_description = input("Введите новое описание для Вашей задачи: ")
                        update_description(db, number, new_description)
                        print("Изменения успешно сохранены.")
                        get_one_task(db, number)
                    elif operation == 3:
                        new_theme = input("Введите новое название для Вашей задачи: ")
                        new_description = input("Введите новое описание для Вашей задачи: ")
                        update_theme_and_description(db, number, new_theme, new_description)
                        print("Изменения успешно сохранены.")
                        get_one_task(db, number)
                    else:
                        print("Отмена изменений...")
                        break
                except TypeError:
                    print("Вам необходимо ввести число без лишних символов.")
            break
                
        except TypeError:
            print("Вам необходимо ввести число без лишних символов.")
#////////////////////////////////////////
def delete_all_tasks(db):
    with db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM todolist')
        rows = cursor.fetchall()
        if rows:
            #print(f"{rows[0][0]}. Тема: {rows[0][1]}. Описание задачи: {rows[0][2]}")
            db.execute('DELETE FROM todolist')
            reset_ids(db)
            print("Задачи успешно удалены.")
        else:
            print("Список задач уже пуст.")

def delete_one_task(db, number):
    with db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM todolist WHERE id = ?', (number,))
        rows = cursor.fetchall()
        if rows:
            #print(f"{rows[0][0]}. Тема: {rows[0][1]}. Описание задачи: {rows[0][2]}")
            db.execute('DELETE FROM todolist WHERE id = ?', (number,))
            reset_ids(db)
            print(f"Задача №{number} успешно удалена.")
        else:
            print("Задачи с таким номером не существует")
            return False

def delete_tasks(db):
    while True:
        print("-------------------")
        print("1. Удалить задачу")
        print("2. Удалить все задачи")
        print("3. Отмена")
        print("-------------------")
        try:
            operation = input("Выберите действие: ").strip()
            operation = int(operation)
            if operation < 1 or operation > 3:
                print("Введите корректное значение в виде цифры от 1 до 3") 
            elif operation == 1:
                number_task = input("Введите номер задачи, которую Вы хотите удалить: ").strip()
                number = int(number_task)
                result_func = delete_one_task(db, number)
                if result_func == False:
                    continue
                else:
                    break
            elif operation == 2:
                delete_all_tasks(db)
                break
            else:
                print("Отмена изменений...")
                break
        except TypeError:
            print("Вам необходимо ввести число без лишних символов.")

def reset_ids(db):
    with db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS todolist_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        db.execute('''
            INSERT INTO todolist_temp (name, description)
            SELECT name, description FROM todolist
        ''')
        db.execute('DROP TABLE todolist')
        db.execute('ALTER TABLE todolist_temp RENAME TO todolist')

def main():
    db = create_connection()
    create_table(db)

    actions = {
        "1": add_task,
        "2": print_tasks,
        "3": edit_task,
        "4": delete_tasks,
        #"5": "Закрыть приложение"
    }

    print("Добро пожаловать в трекер задач.")
    while True:
        print("-------------------")
        print("1. Добавить задачу")
        print("2. Посмотреть задачи")
        print("3. Редактировать задачу")
        print("4. Удаление задач из списка")
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