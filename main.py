import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 400, 450
TILE_SIZE = 100
GRID_SIZE = 4
MARGIN = 2
BG_COLOR = (50, 50, 50)
TILE_COLOR = (100, 149, 237)  # Cornflower blue
TEXT_COLOR = (255, 255, 255)
EMPTY_TILE = GRID_SIZE * GRID_SIZE

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пятнашки")
font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

class Game:
    def __init__(self):
        self.board = list(range(1, EMPTY_TILE + 1))
        self.empty_pos = EMPTY_TILE - 1
        self.moves = 0
        self.shuffle()
        
    def shuffle(self):
        # Делаем несколько случайных ходов для перемешивания
        for _ in range(1000):
            possible_moves = []
            row, col = self.empty_pos // GRID_SIZE, self.empty_pos % GRID_SIZE
            
            if row > 0:
                possible_moves.append(-GRID_SIZE)
            if row < GRID_SIZE - 1:
                possible_moves.append(GRID_SIZE)
            if col > 0:
                possible_moves.append(-1)
            if col < GRID_SIZE - 1:
                possible_moves.append(1)
                
            move = random.choice(possible_moves)
            self.swap_tiles(self.empty_pos + move)
        
        self.moves = 0
        
    def is_solved(self):
        return all(self.board[i] == i + 1 for i in range(EMPTY_TILE))
        
    def swap_tiles(self, pos):
        if 0 <= pos < len(self.board):
            # Проверяем, является ли плитка соседней с пустой
            row1, col1 = self.empty_pos // GRID_SIZE, self.empty_pos % GRID_SIZE
            row2, col2 = pos // GRID_SIZE, pos % GRID_SIZE
            
            if (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2):
                self.board[self.empty_pos], self.board[pos] = self.board[pos], self.board[self.empty_pos]
                self.empty_pos = pos
                self.moves += 1
                return True
        return False
        
    def draw(self, screen):
        screen.fill(BG_COLOR)
        
        # Рисуем плитки
        for i in range(len(self.board)):
            if self.board[i] != EMPTY_TILE:
                row, col = i // GRID_SIZE, i % GRID_SIZE
                pygame.draw.rect(screen, TILE_COLOR, 
                                (col * (TILE_SIZE + MARGIN) + MARGIN, 
                                 row * (TILE_SIZE + MARGIN) + MARGIN, 
                                 TILE_SIZE, TILE_SIZE))
                
                text = font.render(str(self.board[i]), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(col * (TILE_SIZE + MARGIN) + TILE_SIZE//2 + MARGIN, 
                                                 row * (TILE_SIZE + MARGIN) + TILE_SIZE//2 + MARGIN))
                screen.blit(text, text_rect)
        
        # Отображаем количество ходов
        moves_text = small_font.render(f"Ходы: {self.moves}", True, TEXT_COLOR)
        screen.blit(moves_text, (10, HEIGHT - 40))
        
        # Если игра решена
        if self.is_solved():
            solved_text = font.render("Поздравляем! Вы решили головоломку!", True, (0, 255, 0))
            text_rect = solved_text.get_rect(center=(WIDTH//2, HEIGHT - 20))
            screen.blit(solved_text, text_rect)

def main():
    game = Game()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.shuffle()
                elif event.key == pygame.K_ESCAPE:
                    running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    col = x // (TILE_SIZE + MARGIN)
                    row = y // (TILE_SIZE + MARGIN)
                    
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                        pos = row * GRID_SIZE + col
                        game.swap_tiles(pos)
        
        game.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()