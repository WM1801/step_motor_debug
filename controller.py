#controller.py
from enum import Enum 

class MoveState(Enum): 
    Stop = 1
    Acceler = 2
    Braking = 3
    Move = 4
    
class Direction(Enum):
    Left = -1 
    Right = 1 

class Controller:
    def __init__(self, init_pos=0, init_dir=Direction.Right, init_acc = 2047, init_dcc = 2047, init_speed_max = 6700, init_speed_min = 100):
        self.position = init_pos #начальное положение
        self.target_position = init_pos #целевое положение
        self.direction = init_dir #направление
        self.acc = init_acc #ускорение разгона
        self.dcc = init_dcc #ускорение торможения
        self.speed_max = init_speed_max #максимальная скорость 
        self.speed_min = init_speed_min #минимальная скорость  
        self.state = MoveState.Stop #состояние (разгон, торможение, остановлен, вращение с постоянной скоростью)
        self.speed = 0 #текущая скорость (по сути частота импульсов в секунду)
        self.period = 0  #период между импульсами, определяется скоростью
        
    def set_abs_position(self, new_position):
        self.target_position = new_position
        
    def set_rel_position(self, offset):
        self.position += offset
    
    def update_period(self): 
        if self.speed < 0:
            raise ValueError("Скорость должна быть положительной")
        elif self.speed == 0: 
            self.period = 0
        else: 
            self.period = 1/self.speed 
        
    def get_direction(self):
        return self.direction.value 
        
        
    def calculate_speed(self):
    	self.speed = 100
        
    def move(self): 
        if self.position < self.target_position:
            self.direction = Direction.Right
            self.calculate_speed()
            self.state = MoveState.Move
            self.position += 1  # Увеличиваем позицию (можно заменить на более сложную логику)
        elif self.position > self.target_position:
            self.direction = Direction.Left
            self.calculate_speed()
            self.state = MoveState.Move
            self.position -= 1  # Уменьшаем позицию (можно заменить на более сложную логику)
        else:
            self.state = MoveState.Stop
            self.speed = 0
        
    def run(self):
        self.move()
        self.update_period() 
        return self.state, self.direction.value, self.period
