'''
generate_range.py
Аргументы: -s <size>, -r <range_limit>, -l <sideLengthLimit>, -o <outputFile>
Создание множества 100 (по умолчанию) ранжированных  queries
x_1 x'_1 y_1 y'_1
x_m x'_m y_m y'_m
'''
import sys
import getopt
import random

# генерация случайного треугольника и запись в файл
def build_rectangular(file_handle, range_limit, len_limit):
    length = random.uniform(-len_limit, len_limit)
    x1 = round(random.uniform(-range_limit, range_limit),2)
    x2 = round(x1 + length, 2)
    length = random.uniform(-len_limit, len_limit)
    y1 = round(random.uniform(-range_limit, range_limit),2)
    y2 = round(y1 + length, 2)
    
    content = str(x1) + ' ' + str(x2) + ' ' + str(y1) + ' ' + str(y2)
    file_handle.write(content + '\r\n')

def main():
    file_name = 'queries_range.txt'
    size = 100
    range_limit = 500
    len_limit = 100
    
    # parse arguements
    options, args = getopt.getopt(sys.argv[1:],"s:r:o:l:")
    for opt, para in options:
        if opt == '-s':
            size = int(para)
        if opt == '-r':
            range_limit = int(para)
        if opt == '-l':
            len_limit = int(para)
        if opt == '-o':
            file_name = para

    f = open(file_name, 'wt')
    
    for _ in range(1, size+1):
        build_rectangular(f, range_limit, len_limit)
    
    f.close()
    print('Finished')

if __name__ == '__main__':
    main()
