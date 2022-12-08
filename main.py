# Huffman coding
import sys


class Verticle():
    def __init__(self, left_child, right_child, value, name):
        self.left_child = left_child
        self.right_child = right_child
        if (self.right_child == None) and (self.right_child == None):
            self.value = value
        else:
            self.value = self.right_child.value + self.left_child.value
        if (self.right_child == None) and (self.right_child == None):
            self.name = name
        else:
            self.name = self.left_child.name + self.right_child.name


def count_symbol_freq(input_file):
    symbol_freq = dict()
    with open(input_file, 'r') as f:
        for line in f.readlines():
            for i in line:
                if i in symbol_freq:
                    symbol_freq[i] += 1
                else:
                    symbol_freq.update({i: 1})
    return symbol_freq


def make_codes(root, s):
    if (root.left_child == None) and (root.right_child == None):
        codes_dict.update({root.name:s})
    else:
        make_codes(root.left_child, s + "0")
        make_codes(root.right_child, s + "1")

def make_graph(dict):
    verticles_list = []
    for i in dict.keys():
        verticles_list.append(Verticle(None, None, dict[i], i))
    verticles_list.sort(key=lambda verticle: verticle.value, reverse=True)
    for i in verticles_list:
        print(str(i.value) + " " + i.name)
    print("------------")
    while len(verticles_list) > 1:
        yet_another_vert = Verticle(verticles_list[-1], verticles_list[-2], None, None)
        # print(str(yet_another_vert.value) +" "+yet_another_vert.name)
        for i in range(len(verticles_list)):
            if verticles_list[i].value <= yet_another_vert.value:
                verticles_list.insert(i, yet_another_vert)
                break
        verticles_list.pop(-1)
        verticles_list.pop(-1)
    return verticles_list

def encode(input_file, output_file):
    dict = count_symbol_freq(input_file)
    verticles_list = make_graph(dict)
    make_codes(verticles_list[0],"")
    in_f = open(input_file, 'r')
    out_f = open(output_file, 'w')
    for line in in_f.readlines():
        for i in line:
            out_f.write(codes_dict[i])
    in_f.close()
    out_f.close()
# --encode input.txt output.txt
def decode(input_file, output_file):
    pass


codes_dict = {}
if len(sys.argv) != 4:
    print("Неверное число параметров")
else:
    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    if operation == '--encode':
        print(encode(input_file, output_file))
    elif operation == '--decode':
        decode(input_file, output_file)
    else:
        print(f'Неизвесный параметр {operation}')
