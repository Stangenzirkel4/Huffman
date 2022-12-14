# Huffman coding
import sys      # Подключаем библиотеку sys (работа с параметрами командной строки)


class Verticle():       # Класс для создания графа
    def __init__(self, left_child, right_child, value, name):
        self.left_child = left_child        # Ссылка на левого ребенка вершины
        self.right_child = right_child      # Ссылка на правого ребенка вершины
        if (self.right_child == None) and (self.right_child == None):   # Если у вершины есть дети, то ее вес равен
            self.value = value                                          # сумме их весов
        else:                                                           # Иначе вес задается извне
            self.value = self.right_child.value + self.left_child.value
        self.name = name                   # Имя необходимо для опознания кодируемых символов, задается только для листьев


def write_bytes(current_byte,out_f):    # Отдельный метод для записи строки длиннее 8 бит.
    while len(current_byte)>8:          # Переводим 8 символов в двоичный int и конвертируем в 1 байт, параметр "big"
        out_f.write(int(current_byte[0:8],2).to_bytes(1,"big")) # параметр "big" отвечает за то, с какой стороны начинается запись
                                                                # нам он не важен, т.к. байт только один
        current_byte = current_byte[8:] # Отбрасываем записанную часть
    return current_byte                 # Возвращаем то, что не записали


def count_symbol_freq(input_file):      # Метод для подсчета частоты появления символов.
    symbol_freq = dict()                # Создаем пустой словарь
    with open(input_file, 'r') as f:
        for line in f.readlines():
            for i in line:              # Для каждого символа в файле проверяем его наличие в словаре
                if i in symbol_freq:    # Если есть
                    symbol_freq[i] += 1 # увеличиваем счетчик
                else:                   # Если нет - обновляем словарь
                    symbol_freq.update({i: 1})
    return symbol_freq                  # Возвращаем словарь вида "Символ: Количество вхождений"


def make_codes(root, s):                        # Метод для обхода дерева и создания кодирующего словаря
    if (root.left_child == None) and (root.right_child == None):
        codes_dict.update({root.name:s})        # Если лист - обновляем словарь
    else:                                       # Если нет -
        make_codes(root.left_child, s + "0")    # Повторяем с левым ребенком, добавляя к коду 0
        make_codes(root.right_child, s + "1")   # Повторяем с правым ребенком, добавляя к коду 1


def make_graph(dict):
    verticles_list = []             # Создаем пустой список вершин
    for i in dict.keys():           # Заполняем его листьями
        verticles_list.append(Verticle(None, None, dict[i], i))

    verticles_list.sort(key=lambda verticle: verticle.value, reverse=True)      # Сортируем массив по убыванию

    while len(verticles_list) > 1:              # Пока не останется только корень дерева
        yet_another_vert = Verticle(verticles_list[-1], verticles_list[-2], None, None) # Создаем новую вершину из двух самых маленьких
        for i in range(len(verticles_list)):    # Вставляем ее так, чтобы не нарушилась сортировка
            if verticles_list[i].value <= yet_another_vert.value:
                verticles_list.insert(i, yet_another_vert)
                break
        verticles_list.pop(-1)      # Удаляем две самые маленькие вершины
        verticles_list.pop(-1)
    return verticles_list           # Возвращаем ссылку на корень


def encode(input_file, output_file):
    dict = count_symbol_freq(input_file)    # Считаем кол-во уникальных символов
    verticles_list = make_graph(dict)       # Создаем граф, ищем корень
    make_codes(verticles_list[0], "")       # Формируем словарь шифров

    in_f = open(input_file, 'r')            # Открываем файл на чтение
    out_f = open(output_file, 'wb')         # Открываем файл на запись в байтовом режиме

    current_line = str(len(codes_dict))+"\n"    # Формируем первую строку (танцы с бубном нужны, т.к. запись в байтовом режиме)
    out_f.write(current_line.encode("UTF-8"))   # Записываем в файл

    for i in codes_dict.keys():                             # Записываем словарь шифров в виде "<символ> <код>"
        current_line = i + " " + codes_dict[i] + "\n"
        out_f.write(current_line.encode("UTF-8"))

    current_byte = ""   # Строка для побайтовой записи (содержит только "0" и "1", которые переводятся в int, а затем в byte)
    for line in in_f.readlines():
        for i in line:
            current_byte += codes_dict[i]       # Для каждого символа записываем в current_byte его код в виде строки
            current_byte = write_bytes(current_byte, out_f)  # Отправляем в метод для побайтовой записи

    extra_bits = 8-len(current_byte)                    # В конце у нас могут остаться недозаписанные биты
    current_byte = current_byte + "0"*extra_bits        # Дозаполняем строку нулями
    out_f.write(int(current_byte,2).to_bytes(1,"big"))  # Записываем это в файл
    out_f.write(extra_bits.to_bytes(1,"big"))           # Сохраняем то, сколько битов дописали

    in_f.close()        # Не забываем закрыть файлы
    out_f.close()


def decode(input_file, output_file):
    in_f = open(input_file, 'rb')       # Открываем файл на чтение в байтовом режиме
    out_f = open(output_file, 'w')      # Открываем файл на запись

    decode_dict = {}        # Словарь для дешифрации вида "Шифр: Символ"
    current_byte = ""       # Строка из "0" и "1" для поиска в ней шифров
    current_code = ""       # Строка для обхода файла и проверки на соответствие с ключами словаря дешифрации

    n = int(in_f.readline())    # Считываем первый символ, отвечающий за размер словаря дешифрации
    for i in range(n):          # Формируем словарь дешифрации
        current_line = in_f.readline()          # Считываем очередную строку
        if current_line == b'\n':               # Проверяем, не является ли она переносом строки
            current_line = in_f.readline()      # Если да, считываем строку линию и обновляем словарь
            key = str(current_line[1:-1])[2:-1] # При записи отбрасываем служебные символы
            char = "\n"                         # Необработанная строка имеет вид " b'0101'\n"
            decode_dict.update({key: char})
            continue
        key = str(current_line[2:-1])[2:-1]     # Если нет, то отбрасываем служебные символы по-другому
        char = chr(current_line[0])             # Необработанная строка имеет вид "A b'0101'\n"
        decode_dict.update({str(key): char})

    for line in in_f.readlines():       # Переводим каждый байт входного файла в строку
        for i in line:
            current_byte += "0"*(10 - len(str(bin(i)))) + str(bin(i))[2:]  #Если необходимо дописываем ведущие нули, т.к. int() их затирает

    extra_bits = int(current_byte[-8:], 2)  # Проверяем последний байт, в котором содержится кол-во "лишних" бит
    current_byte = current_byte[:-(8+extra_bits)]   # Удаляем бит с количеством и "лишние" биты

    for i in current_byte:
        current_code += i               # Наращиваем current_code пока не станет соответствовать одному из шифров
        if current_code in decode_dict.keys():  # Когда соответствует - дешифруем
            out_f.write(decode_dict[current_code])
            current_code = ""                   # Сам current_code обнуляем

    in_f.close()            # Не забываем закрыть файлы
    out_f.close()



# Это чтобы было удобнее вводить параметры:
# --encode input.txt output.txt
# --decode output.txt input1.txt


codes_dict = {}     # Словарь для кодировки файла вида: "Символ: двоичный код"
if len(sys.argv) != 4:  # Проверка на наличие 4 входных аргументов: название программы, вид операции, входной и выходной файл
    print("Неверное число параметров")
else:
    operation = sys.argv[1]         # Вид операции
    input_file = sys.argv[2]        # Входной файл
    output_file = sys.argv[3]       # Выходной файл
    if operation == '--encode':
        encode(input_file, output_file)     # Закодировать
    elif operation == '--decode':
        decode(input_file, output_file)     # Декодировать
    else:
        print(f'Неизвесный параметр {operation}')       # Неизвестная операция
