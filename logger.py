#logger.py

def write_log(message, filename="log.txt"):
    """Записывает сообщение в файл, пересоздавая его."""
    with open(filename, 'w') as file:
        #file.write(message + '\n')  # Записываем сообщение и добавляем перевод строки
        pass

def append_log(message, filename="log.txt"):
    """Добавляет сообщение в конец файла."""
    with open(filename, 'a') as file:
        file.write(message + '\n')  # Записываем сообщение и добавляем перевод строки

# Пример использования
if __name__ == "__main__":
    # Пересоздаем файл и записываем первую строку
    write_log("Это первая строка в логе.")
    
    # Добавляем дополнительные строки
    append_log("Это вторая строка в логе.")
    append_log("Это третья строка в логе.")
