from core import run, send
import os
from datetime import date
from secrets import VACANCY_LIST

now = date.today()
dir_name = './' + str(now.day) + str(now.strftime("%b")) + '/'
filename_tail = "_" + str(now.day) + "_" + str(now.month) + "_new_vacancies.txt"
i = 0
files = []
file_all = ""

for vacancy in VACANCY_LIST:
    run(vacancy)
    vacancy_split = "_".join(vacancy.split())
    fl = open(dir_name + f'{vacancy_split}' + f'{filename_tail}', 'r', encoding='utf-8' )
    files.append(fl.read())
    file_all += (vacancy.upper() + " VACANCIES:\n\n")* bool(files[i]) + files[i] * bool(files[i])
    fl.close()
    i += 1

if file_all == "":
    print("Nothing to send")
else:  
    file_name = dir_name + "all" + f"{filename_tail}"
    f_all = open(f"{file_name}", "w+", encoding="utf-8" )
    f_all.write(file_all)
    f_all.close()
    send(file_name)