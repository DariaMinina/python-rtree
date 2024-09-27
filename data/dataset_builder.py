'''
dataset_builder.py
Аргументы: -s <size>, -r <range_limit>, -o <output_name>
Создание датасета
id_1 x_1 y_1
id_m x_m y_m
'''
import sys
import getopt
import random

# Генерация координат для rtreePoint
def write_point(f, range_limit):
    x = round(random.uniform(-range_limit, range_limit),2)
    y = round(random.uniform(-range_limit, range_limit),2)
    f.write(str(x) + ' ' + str(y) + '\r\n')

# Построение датасета
def build_dataset(file_name, size, range_limit):
    f = open(file_name, 'wt')
    f.write(str(size) + '\r\n') # first line
    # заполнение строк
    for i in range(1, size+1):
        f.write(str(i) + ' ')
        write_point(f, range_limit)

    f.close()
    print('Size: ', size, '. Range: ', -range_limit, ':', range_limit)

def main():
    # дефолтное название файла
    file_name = 'dataset.txt'
    size = 10000 
    range_limit = 500
    
    # парсинг параметров
    options,args = getopt.getopt(sys.argv[1:],"s:r:o:")
    for opt, para in options:
        if opt == '-s':
            size = int(para)
        if opt == '-r':
            range_limit = int(para)
        if opt == '-o':
            file_name = para
    
    # построение датасета
    build_dataset(file_name, size, range_limit)
    
if __name__ == '__main__':
    main()
