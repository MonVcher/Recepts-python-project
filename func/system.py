from pathlib import Path
from shutil import rmtree
import os
import subprocess


def rem(put):
    for path in Path(put).glob('*'):
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()

def cmd_command(com):
    rus_list = ['кочанная капуста', 'яблоко', 'огурец', 'морковь', 'маракс',
                'яблоко', 'клубника', 'банан', 'цветная капуста', 'артишок',
                  'апельсин', 'лимон', 'болгарский перец', 'бедро', 'инжир',
                  'спагетти', 'ананас', 'яблоко', 'кардон', 'горшок', 'гранат',
                    'цуккини', 'крюк', 'чеснок']
    eng_list = ['head_cabbage', 'butternut_squash', 'cucumber', 'French_loaf',
                 'maraca', 'Granny_Smith', 'strawberry', 'banana', 'cauliflower', 
                 'artichoke', 'orange', 'lemon', 'bell_pepper', 'hip', 'fig', 'spaghetti_squash',
                 'pineapple', 'custard_apple', 'cardoon', 'pot', 'pomegranate',
                   'zucchini', 'hook', 'conch']
    # Команда, которую нужно выполнить
    command = com
    # Выполнение команды и получение результата
    result = subprocess.run(command, capture_output=True, shell=True, text=True)
    # Получение вывода команды
    output = result.stdout
    # Обработка вывода команды
    lines = output.split("\n")
    li=[]
    for line in lines:
        li.append(line)
    # print(rus_list)
    # print(eng_list)
    for i in range(len(rus_list)):
        # print(li[3][100:120].split()[1], eng_list[i], rus_list[i])
        if li[3].split()[4] == eng_list[i]:
            return rus_list[i]
    return 'лук'
    # print(li[3][100:120].split()[1])
    # [102: 120]
    # print(cone.split()[0])
    # # Вывод результата
    # print(result.decode('cp866'))