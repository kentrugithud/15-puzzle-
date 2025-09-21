from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from random import shuffle
import numpy as np

class PuzzleButton(Button):
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.text = str(number) if number != 16 else ""
        self.font_size = 30

class PuzzleGame(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 4
        self.spacing = 2
        self.buttons = []
        self.empty_pos = (3, 3)  # начальная позиция пустой клетки
        self.init_board()
        
    def init_board(self):
        self.clear_widgets()
        self.buttons = []
        
        # Создаем упорядоченную доску
        numbers = list(range(1, 17))
        
        # Перемешиваем числа, убедившись, что головоломка решаема
        while True:
            shuffle(numbers)
            if self.is_solvable(numbers):
                break
        
        # Создаем кнопки
        for i in range(16):
            row, col = i // 4, i % 4
            if numbers[i] == 16:
                self.empty_pos = (row, col)
                btn = PuzzleButton(numbers[i], background_color=(0.8, 0.8, 0.8, 1))
            else:
                btn = PuzzleButton(numbers[i])
            btn.bind(on_press=self.on_button_press)
            self.add_widget(btn)
            self.buttons.append(btn)
    
    def is_solvable(self, numbers):
        # Проверяем, является ли головоломка решаемой
        # Подсчитываем количество инверсий
        inversions = 0
        for i in range(len(numbers)):
            for j in range(i + 1, len(numbers)):
                if numbers[i] != 16 and numbers[j] != 16 and numbers[i] > numbers[j]:
                    inversions += 1
        
        # Для решаемости необходимо четное количество инверсий
        # и пустая клетка должна быть на четной строке снизу (считая с 1)
        empty_row = 4 - (numbers.index(16) // 4)
        return (inversions % 2 == 0) == (empty_row % 2 == 1)
    
    def on_button_press(self, instance):
        # Находим позицию нажатой кнопки
        index = self.buttons.index(instance)
        row, col = index // 4, index % 4
        
        # Проверяем, можно ли переместить кнопку
        if (abs(row - self.empty_pos[0]) == 1 and col == self.empty_pos[1]) or \
           (abs(col - self.empty_pos[1]) == 1 and row == self.empty_pos[0]):
            # Меняем местами с пустой клеткой
            empty_index = self.empty_pos[0] * 4 + self.empty_pos[1]
            self.buttons[empty_index].number = instance.number
            self.buttons[empty_index].text = str(instance.number) if instance.number != 16 else ""
            self.buttons[empty_index].background_color = (1, 1, 1, 1)
            
            instance.number = 16
            instance.text = ""
            instance.background_color = (0.8, 0.8, 0.8, 1)
            
            self.empty_pos = (row, col)
            
            # Проверяем, решена ли головоломка
            if self.is_solved():
                self.parent.add_widget(Label(text="Поздравляем! Вы решили головоломку!", 
                                           size_hint_y=0.2,
                                           font_size=20))
    
    def is_solved(self):
        # Проверяем, все ли числа на своих местах
        for i in range(15):
            if self.buttons[i].number != i + 1:
                return False
        return self.buttons[15].number == 16

class MainApp(App):
    def build(self):
        # Главный layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Кнопка перезапуска
        restart_btn = Button(text="Новая игра", size_hint_y=0.1)
        restart_btn.bind(on_press=self.restart_game)
        
        # Игровое поле
        self.game = PuzzleGame()
        
        main_layout.add_widget(restart_btn)
        main_layout.add_widget(self.game)
        
        return main_layout
    
    def restart_game(self, instance):
        # Удаляем сообщение о победе, если есть
        if len(self.root.children) > 2:
            self.root.remove_widget(self.root.children[0])
        
        # Перезапускаем игру
        self.root.remove_widget(self.game)
        self.game = PuzzleGame()
        self.root.add_widget(self.game)

if __name__ == '__main__':
    # Устанавливаем размер окна для мобильного устройства
    Window.size = (360, 640)
    MainApp().run()