'''
generate_nn.py
Аргументы: -s <size>, -r <range_limit>, -o <output_name>
Создание множества 100 (по умолчанию) ранжированных  queries
x_1 y_1
x_m y_m
'''

import sys
import getopt

import dataset_builder as dataset_builder

def main():
    file_name = 'queries_nn.txt'
    size = 100
    rangeLimit = 500
    
    # парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"s:r:o:")
    for opt, para in options:
        if opt == '-s':
            size = int(para)
        if opt == '-r':
            rangeLimit = int(para)
        if opt == '-o':
            file_name = para

    f = open(file_name, 'wt')
    for i in range(1, size+1):
        dataset_builder.write_point(f, rangeLimit)
    
    f.close()
    print('Finished')

if __name__ == '__main__':
    main()
