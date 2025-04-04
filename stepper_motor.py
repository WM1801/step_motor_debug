# stepper_motor.py
import time


class StepperMotor:
    def __init__(self, steps_to_360=200, microstep=1):
        self.steps_to_360 = steps_to_360
        self.microstep = microstep
        self.direction = 1  # 1 для вперед, -1 для назад
        self.step_time = 0.01  # Время между шагами в секундах // пин step 
        self.current_position = 0  # Текущая позиция вала (в шагах)
        self.speed = 0  # Скорость в оборотах в секунду
 
    def set_direction(self, direction):
        if direction not in [-1, 1]:
            raise ValueError("Направление должно быть 1 (вперед) или -1 (назад)")
        self.direction = direction

    def set_step_time(self, step_time):
        if step_time < 0:
            raise ValueError("Время шага должно быть положительным")
        elif step_time == 0: 
            self.step_time = 0
            self.speed = 0
        else: 
            self.step_time = step_time
            self.speed = 1 / (step_time * self.steps_to_360*self.microstep)  # Расчет скорости в оборотах в секунду

    def step(self, step_time):
        self.set_step_time(step_time)
        self.current_position += self.direction

    def run(self, steps):
        for _ in range(steps):
            self.step()
            
    def state(self): 
        print(f"pos: {self.get_position()}, speed: {self.get_speed()}, dir: {self.get_direction()}")
        
    def stateString(self): 
        return (f"pos: {self.get_position()}, speed: {self.get_speed()}, dir: {self.get_direction()}")
        
    def get_speed(self):
        return self.speed
    
    def get_position(self):
        return self.current_position
        
    def get_direction(self): 
        return self.direction

# Пример использования
if __name__ == "__main__":
    motor = StepperMotor(steps_to_360=200, microstep=16)
    motor.set_direction(1)  # Установить направление вперед
    #motor.set_direction(-1)
    for _ in range(400): 
        motor.step(0.0001)  # Сделать шаг
        motor.state()
