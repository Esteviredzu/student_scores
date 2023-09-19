import functions
import os
import goose

functions.first_execute()

subjects = {1:"Латышский язык", 2:"История Мадагаскара", 3:"Язык программирования Brainfuck"}

def main_cycle():
    os.system("cls")
    print(goose.goose)
    while True:
        print("Выберите студента, с которым вы хотите работать\n")
        student_id = functions.select_student()
        os.system("cls")
        print(goose.goose)
        print('''
            
1 - Добавить студенту оценку
2 - Удалить студента
3 - Показать оценки студента
4 - Назад
>>> ''')
        que = input("Выберите действие >>> ")
        if que == '1':
            print(subjects)
            sub = int(input("Выберите предмет >>> "))
            if sub < 1 or sub > len(subjects):
                print("error")
                continue
            score = int(input("Введите оценку >>> "))
            functions.add_score(student_id, subjects[sub], score)
            os.system("cls")
            print(goose.goose)
            print(f"Оценка {score} успешно добавлена для студента {student_id}\n")

            pass
        elif que == '2':
            functions.delete_student(student_id)
        elif que == '3':
            functions.show_student_scores(student_id)
        elif que == '4':
            break
        else:
            print("Неверный выбор, попробуйте ещё раз")
        pass


while True:
    os.system("cls")
    print(goose.goose)
    que = input('''
                
1 - Начать работу
2 - Добавить нового студента
3 - Выход
>>> ''')

    if que == '2':
        name = input("Введите имя для нового студента >>> ")
        os.system("cls")
        print(goose.goose)
        functions.create_student(name)
    elif que == '3':
        break
    elif que == '1':
        main_cycle()



