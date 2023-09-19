import sqlite3


#Для первоначальной настройки базы данных, если она не существует
def first_execute():
    # Открываем базу
    database = sqlite3.connect("students.db")

    # Курсор
    cursor = database.cursor()

    # Таблица с именами студентов и айди
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_names (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    #Таблица с айди студентов и их оценками
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_scores (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject TEXT NOT NULL,
        score INTEGER,
        FOREIGN KEY (student_id) REFERENCES students_names (id)
    )
    """)
    database.commit()
    database.close()

# Функция принимает имя студента и вносит его в базу данных
def create_student(student_name):
    # Открываем базу
    database = sqlite3.connect("students.db")
    cursor = database.cursor()

    try:
        # Добавляем студента в таблицу с именами
        cursor.execute("INSERT INTO students_names (name) VALUES (?)", (student_name,))
        
        # Получаем id
        student_id = cursor.lastrowid
        
        database.commit()
        database.close()
        
        print(f"Студент {student_name} успешно добавлен с ID {student_id}")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при добавлении студента: {e}")
        database.rollback()
    finally:
        database.close()

# Функция для добавления оценки студенту по предмету
def add_score(student_id, subject, score):
    # Открываем базу
    database = sqlite3.connect("students.db")
    cursor = database.cursor()

    try:
        # Добавляем оценку для студента
        cursor.execute("INSERT INTO students_scores (student_id, subject, score) VALUES (?, ?, ?)",
                       (student_id, subject, score))
        
        database.commit()
        database.close()
        
        print(f"Оценка {score} по предмету '{subject}' успешно добавлена для студента с ID {student_id}")
    except sqlite3.Error as e:
        print(f"Произошла ошибка при добавлении оценки: {e}")
        database.rollback()
    finally:
        database.close()

# Функция для вывода оценок студента
def show_student_scores(student_id):
    database = sqlite3.connect("students.db")
    cursor = database.cursor()

    try:
        cursor.execute("SELECT name FROM students_names WHERE id=?", (student_id,))
        student_name = cursor.fetchone()

        if student_name:
            # Получаем оценки студента
            cursor.execute("SELECT DISTINCT subject FROM students_scores WHERE student_id=?", (student_id,))
            subjects = cursor.fetchall()

            if subjects:
                print(f"\nОценки для студента {student_name[0]}:")
                for subject in subjects:
                    subject = subject[0]
                    cursor.execute("SELECT score FROM students_scores WHERE student_id=? AND subject=?",
                                   (student_id, subject))
                    scores = cursor.fetchall()
                    scoress = ', '.join(str(score[0]) for score in scores)
                    print(f"{subject}: {scoress}")
            else:
                print(f"У студента {student_name[0]} ещё нет оценок")
        else:
            print("Студента с таким ID не существует.")
    except sqlite3.Error as e:
        print(f"Произошла ошибка: {e}")
    finally:
        database.close()

#Функция для выбора студента и получения его ID
def select_student():
    database = sqlite3.connect("students.db")
    cursor = database.cursor()

    try:
        #Список всех студентов
        cursor.execute("SELECT * FROM students_names")
        students = cursor.fetchall()
        if students:
            print("Список студентов:")
            for student in students:
                student_id, student_name = student
                print(f"id: {student_id}, Имя: {student_name}")

            while True:
                try:
                    selected_id = int(input("Введите id студента, которого вы хотите выбрать: "))
                    #Проверяем что айди существует
                    cursor.execute("SELECT * FROM students_names WHERE id=?", (selected_id,))
                    selected_student = cursor.fetchone() #fetchone чтобы получить первую запись
                    if selected_student:
                        return selected_id
                    else:
                        print("Студента не существует")
                except ValueError:
                    print("Ошибка")
        else:
            return None
    except sqlite3.Error as e:
        print(f"Произошла ошибка: {e}")
    finally:
        database.close()

# Функция для удаления студента и всех его оценок
def delete_student(student_id):
    database = sqlite3.connect("students.db")
    cursor = database.cursor()

    try:
        # Получаем имя студента
        cursor.execute("SELECT name FROM students_names WHERE id=?", (student_id,))
        student_name = cursor.fetchone()

        if student_name:
            # Удаляем студента из таблицы с именами
            cursor.execute("DELETE FROM students_names WHERE id=?", (student_id,))

            # Удаляем оценки студента
            cursor.execute("DELETE FROM students_scores WHERE student_id=?", (student_id,))
            
            database.commit()
            print(f"Студент {student_name[0]} удалён")
        else:
            print("Студента не существует")
    except sqlite3.Error as e:
        print(f"Произошла ошибка: {e}")
        database.rollback()
    finally:
        database.close()



if __name__ == "__main__":
    print("Это модуль с функциями для программы по учёту оценок студента, его не следует запускать, у вас всё равно ничего не выйдет.")