import time 
import threading
from stepper_motor import StepperMotor 
from speedometer import Speedometer
from logger import write_log, append_log
from data_plotter import DataPlotter
from controller import Controller, MoveState

import matplotlib.pyplot as plt

# шагов в одном обороте 
def_steps_oborot = 200
# микрошаг (1,2,4,8,16,32,64,128)
def_microstep = 2
# заданное положение 
target_position = 0
#прошлое положение шд для вывода в консоль
console_send_position = None
#
flagRun = True


# переход от шагов к градусам 
def normalise(val): 
    global def_microstep, def_steps_oborot
    # максимальное количество шагов на оборот 
    step_oborot = def_steps_oborot * def_microstep
    # переход к диапазону 0-1
    n_val = val / step_oborot
    # переход к диапазону 0-360 
    grad_val = n_val * 360
    return grad_val 

def input_thread():
    global target_position, flagRun 
    while True:
        try:
            new_position = input("Введите новое целевое положение (или 'exit' для выхода): ")
            if new_position.lower() == 'exit':
                flagRun = False
                print("Завершение работы.")
                break
            target_position = int(new_position)
        except ValueError:
            print("Пожалуйста, введите корректное целевое положение.")

def main(): 
    global target_position, console_send_position, flagRun 
    flagRun = True
    console_send_position = 0xFFFF
    # график вращения 
    speedometer = Speedometer()
    # создание файла лога
    write_log("")
    # запуск графиков положения скорости и т.д.
    plotter = DataPlotter(filename="log.txt") 
    # Запуск графиков в отдельном потоке
    plt.ion()  # Включение интерактивного режима
    speedometer.show()  # Показываем график

    # конфигурируем шаговый двигатель
    motor = StepperMotor(steps_to_360=def_steps_oborot, microstep=def_microstep)
    # контроллер управления 
    ctrl = Controller(init_pos=0, init_acc=2047, init_dcc=2047, init_speed_max=6700, init_speed_min=400)
    # начальное направление 
    motor.set_direction(ctrl.get_direction()) 
    
    # Запуск потока для считывания ввода
    thread = threading.Thread(target=input_thread)
    thread.daemon = True  # Позволяет завершить поток при выходе из программы
    thread.start()
    
    while flagRun:
        ctrl.set_abs_position(target_position)
        state, direction, period = ctrl.run()
        if state != MoveState.Stop:
            #print("шаг") 
            motor.set_direction(direction)
            motor.step(period) 
            #motor.state()  # статистика движка 
            append_log(motor.stateString())  # сохраняем шаг в лог
        
            plotter.plot()  # обновление данных положения, скорости и направления из файла 
            value = motor.get_position()  # чтение положения для графика вращения 
            n_value = normalise(value)  # перевод шагов в градусы  
            # Обновление значений спидометра
            speedometer.update(n_value)
            plt.draw()  # Перерисовка графика
        else:
            if console_send_position != motor.get_position():  
                print("\nШД остановлен, ", end='')
                motor.state() #статистика движка    
                console_send_position = motor.get_position()
        plt.pause(0.1)  # Небольшая задержка для визуализации 
    
    speedometer.close()
    plt.ioff()  # Выключение интерактивного режима
    plt.close()
        
if __name__ == "__main__": 
    main()
