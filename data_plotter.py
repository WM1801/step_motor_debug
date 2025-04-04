import numpy as np
import matplotlib.pyplot as plt


class DataPlotter:
    def __init__(self, filename="log.txt"):
        self.filename = filename
        self.x_data = []  # Итерации
        self.position_data = []  # Позиция
        self.speed_data = []  # Скорость
        self.direction_data = []  # Направление
        
        # Создание фигуры и осей для трех графиков
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8))
        self.ax1.set_title("Положение")
        self.ax1.set_xlabel("Итерации")
        self.ax1.set_ylabel("Позиция")
        
        self.ax2.set_title("Скорость")
        self.ax2.set_xlabel("Итерации")
        self.ax2.set_ylabel("Скорость")
        
        self.ax3.set_title("Направление")
        self.ax3.set_xlabel("Итерации")
        self.ax3.set_ylabel("Направление")

    def read_data(self):
        """Считывает данные из файла и обновляет списки."""
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                self.x_data.clear()  # Очищаем предыдущие данные
                self.position_data.clear()  # Очищаем предыдущие данные
                self.speed_data.clear()  # Очищаем предыдущие данные
                self.direction_data.clear()  # Очищаем предыдущие данные
                
                for i, line in enumerate(lines):
                    # Извлекаем данные из строки
                    parts = line.split(',')
                    pos = int(parts[0].split(':')[1].strip())
                    speed = float(parts[1].split(':')[1].strip())
                    direction = int(parts[2].split(':')[1].strip())
                    
                    self.x_data.append(i)  # Используем индекс как x
                    self.position_data.append(pos)  # Добавляем позицию
                    self.speed_data.append(speed)  # Добавляем скорость
                    self.direction_data.append(direction)  # Добавляем направление
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    def plot(self):
        """Строит графики на основе считанных данных."""
        self.read_data()  # Считываем данные из файла
        
        # Очищаем оси перед рисованием
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        # Строим графики
        self.ax1.plot(self.x_data, self.position_data, color='blue', label='Положение')
        self.ax1.set_title("Положение")
        self.ax1.set_xlabel("Итерации")
        self.ax1.set_ylabel("Позиция")
        self.ax1.legend()

        self.ax2.plot(self.x_data, self.speed_data, color='green', label='Скорость')
        self.ax2.set_title("Скорость")
        self.ax2.set_xlabel("Итерации")
        self.ax2.set_ylabel("Скорость")
        self.ax2.legend()

        self.ax3.plot(self.x_data, self.direction_data, color='red', label='Направление')
        self.ax3.set_title("Направление")
        self.ax3.set_xlabel("Итерации")
        self.ax3.set_ylabel("Направление")
        self.ax3.legend()

         # Удаляем предыдущее текстовое поле, если оно существует
        if hasattr(self, 'text_box'):
            self.text_box.remove()

        # Добавление текстового поля с текущими значениями
        if self.x_data:  # Проверяем, есть ли данные
            last_position = self.position_data[-1]
            last_speed = self.speed_data[-1]
            last_direction = self.direction_data[-1]

            # Создаем текстовое поле
            textstr = ' '.join((
                f'Позиция: {last_position:<8}',
                f'Скорость: {last_speed:8.2f}',
                f'Направление: {last_direction}'
            ))

            # Добавляем текстовое поле под графиками
            self.text_box = self.fig.text(0.15, 0.03, textstr, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))
            
            # Добавляем метки на графики
            self.ax1.text(self.x_data[-1], last_position, f'{last_position}', color='blue', fontsize=10, ha='left')
            self.ax2.text(self.x_data[-1], last_speed, f'{last_speed:.2f}', color='green', fontsize=10, ha='left')
            self.ax3.text(self.x_data[-1], last_direction, f'{last_direction}', color='red', fontsize=10, ha='left')

        plt.tight_layout()  # Уплотнение графиков
        plt.draw()  # Перерисовка графиков

    def show(self):
        """Показывает график."""
        plt.show()

# Пример использования
if __name__ == "__main__":
    plotter = DataPlotter(filename="log.txt")  # Укажите имя вашего файла с данными

    plt.ion()  # Включение интерактивного режима
    plotter.show()  # Показываем график

    try:
        while True:
            plotter.plot()  # Обновляем график
            plt.pause(1)  # Задержка для обновления графика
    except KeyboardInterrupt:
        print("Программа прервана вручную.")
    
    plt.ioff()  # Выключение интерактивного режима
    plt.show()  # Показываем финальный график
