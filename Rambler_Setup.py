import datetime
from time import sleep
from Rambler_Program import Program

# Это скрипт запуска
# ставим бесконечный цикл, в нужный момент времени - запускается скрипт

# можно было поискать другой способ, чтоб было не так колхозно, но это надо искать
while True:
    time = str(datetime.datetime.now())
    time = time[11:]
    if time == "01:01:01.101111":
        sleep(2)
        ramblerparser = Program()
