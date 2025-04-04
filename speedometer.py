import numpy as np
import matplotlib.pyplot as plt

class Speedometer:
    def __init__(self, max_value=360, radius=200):
        self.max_value = max_value
        self.current_value = 0
        self.radius = radius  # Фиксированный радиус
        
        # Создание полярной фигуры
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        #self.ax.set_ylim(0, self.max_value)  # Установка пределов радиуса
        self.ax.set_theta_zero_location('N')  # Установка нуля в верхней части
        self.ax.set_theta_direction(-1)  # Установка направления против часовой стрелки
        
        # Создание меток на спидометре
        self.ax.set_xticks(np.radians(np.linspace(0, 360, 12, endpoint=False)))  # 12 меток
        self.ax.set_xticklabels([f"{i}" for i in range(0, 360, 30)])  # Метки от 0 до 330

        # Создание линии спидометра
        self.line, = self.ax.plot([], [], 'o-', lw=2, color='red')  # Используем 'o-' для отображения точек

    def update(self, value):
        # Нормализация значения к диапазону от 0 до 360
        normalized_value = value % self.max_value
        
        self.current_value = normalized_value
        angle = np.radians(self.current_value)  # Преобразование в радианы
        
        # Обновление линии, чтобы указать на текущий угол
        self.line.set_data([angle, angle], [0, self.radius])  # Линия от 0 до фиксированного радиуса
        self.ax.draw_artist(self.line)  # Перерисовка линии
        #plt.pause(0.1)  # Небольшая задержка для визуализации

    def show(self):
        plt.show()
        
    def close(self):
        plt.close()

# Пример использования
if __name__ == "__main__":
    speedometer = Speedometer(radius=1)  # Установить радиус спидометра
    
    # Запуск обновления значений спидометра
    for value in range(0, 1000, 5):  # Изменение значения от 0 до 1000
        speedometer.update(value)
    
    speedometer.show()
