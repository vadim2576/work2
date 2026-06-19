import sys
import os
import string

# список самых популярных плохих паролей (взял из интернета)
weak_list = ["123456", "password", "qwerty", "12345", "12345678", "111111", 
             "1234567890", "password1", "abc123", "123123", "admin", 
             "letmein", "welcome", "monkey", "dragon"]

def check_pass(pwd, user=None):
    # проверяем длину
    len_good = len(pwd) >= 8
    
    # проверяем наличие цифр
    has_digit = False
    for c in pwd:
        if c.isdigit():
            has_digit = True
            break
    
    # заглавные буквы
    has_upper = False
    for c in pwd:
        if c.isupper():
            has_upper = True
            break
    
    # спецсимволы
    has_special = False
    for c in pwd:
        if c in string.punctuation:
            has_special = True
            break
    
    # проверка на слабый пароль
    is_weak = pwd.lower() in weak_list
    
    # проверка на имя пользователя
    contains_user = False
    if user != None:
        if user.lower() in pwd.lower():
            contains_user = True
    
    # считаем сколько критериев выполнено
    points = 0
    if len_good:
        points += 1
    if has_digit:
        points += 1
    if has_upper:
        points += 1
    if has_special:
        points += 1
    
    # определяем сложность
    if is_weak:
        level = "Weak"
    else:
        if points == 4:
            level = "Strong"
        elif points >= 2:
            level = "Medium"
        else:
            level = "Weak"
    
    # если пароль содержит имя пользователя - понижаем
    if contains_user and level == "Strong":
        level = "Medium"
    
    # собираем рекомендации
    rec = []
    if is_weak:
        rec.append("Слабый пароль, смените")
    if not len_good:
        rec.append("Нужно минимум 8 символов")
    if not has_digit:
        rec.append("Добавьте цифры")
    if not has_upper:
        rec.append("Добавьте большие буквы")
    if not has_special:
        rec.append("Добавьте символы (@#$%...)")
    if contains_user:
        rec.append("Не пишите имя в пароле")
    
    if len(rec) == 0:
        rec.append("Норм пароль")
    
    # результат
    return {
        "len": len(pwd),
        "dig": has_digit,
        "up": has_upper,
        "spec": has_special,
        "weak": is_weak,
        "has_user": contains_user,
        "level": level,
        "rec": ", ".join(rec)
    }

# главная функция
def main():
    # проверяем аргументы
    if len(sys.argv) < 2:
        print("Надо так: python checkpass.py passwords.txt [username]")
        return
    
    filename = sys.argv[1]
    username = None
    if len(sys.argv) > 2:
        username = sys.argv[2]
    
    # проверяем существует ли файл
    if not os.path.exists(filename):
        print("Ошибка! Файл", filename, "не найден")
        return
    
    # читаем пароли
    try:
        f = open(filename, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
    except:
        print("Ошибка при открытии файла")
        return
    
    # чистим пароли
    passwords = []
    for line in lines:
        p = line.strip()
        if p != "":  # пропускаем пустые строки
            passwords.append(p)
    
    if len(passwords) == 0:
        print("Файл пустой, нет паролей")
        return
    
    # выводим таблицу
    print("\n" + "="*110)
    print(" №  Пароль              Дл Цифры Загл Спец Скомпр ИмяПольз Оценка   Рекомендации")
    print("-"*110)
    
    n = 1
    for p in passwords:
        res = check_pass(p, username)
        
        # сокращаем длинный пароль
        show_pass = p
        if len(p) > 18:
            show_pass = p[:15] + "..."
        
        # готовим поля для вывода
        dig_txt = "Да" if res["dig"] else "Нет" #есть цифры digit
        up_txt = "Да" if res["up"] else "Нет"   # upper есть заглавные 
        spec_txt = "Да" if res["spec"] else "Нет" # special спецсимволы
        weak_txt = "Да" if res["weak"] else "Нет" #скомпрометирован
        user_txt = "Да" if res["has_user"] else "Нет"  #содержит_имя contains_user
    
        print(f"{n:<3} {show_pass:<18} {res['len']:<3} {dig_txt:<5} {up_txt:<4} {spec_txt:<5} {weak_txt:<6} {user_txt:<8} {res['level']:<8} {res['rec']}")
        
        n += 1
    
    print("="*110)

if __name__ == "__main__":
    main()
  