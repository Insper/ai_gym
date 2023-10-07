import pygame
from main import KnightBoard

class KnightsTourVisualization:
    def __init__(self):
        pygame.init()
        
        self.setup_constants()
        self.setup_window()

    def setup_constants(self):
        self.WINDOW_SIZE = 600
        self.BOARD_SIZE = 8
        self.CELL_SIZE = self.WINDOW_SIZE // self.BOARD_SIZE
        self.KNIGHT_RADIUS = self.CELL_SIZE // 3
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.KNIGHT_COLOR = (0, 0, 255)
        self.PATH_COLOR = (255, 0, 0)

    def setup_window(self):
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Knight's Tour Visualization")

    def draw_board(self):
        colors = [(255, 255, 255), (0, 0, 0)]
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                pygame.draw.rect(self.screen, colors[(i + j) % 2], (i * self.CELL_SIZE, j * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def draw_path(self, board, move_limit=None):
        """Draw the knight's path up to a certain move number."""
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if 0 <= board[i][j] < move_limit:
                    pygame.draw.circle(self.screen, self.KNIGHT_COLOR, (i * self.CELL_SIZE + self.CELL_SIZE // 2, j * self.CELL_SIZE + self.CELL_SIZE // 2), self.KNIGHT_RADIUS)
                    font = pygame.font.SysFont(None, 36)
                    move_num = font.render(str(board[i][j]), True, (255, 255, 0))
                    self.screen.blit(move_num, (i * self.CELL_SIZE + self.CELL_SIZE // 4, j * self.CELL_SIZE + self.CELL_SIZE // 4))
                    
        # Drawing the current position with a slightly larger red circle
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if board[i][j] == move_limit-1:
                    pygame.draw.circle(self.screen, self.KNIGHT_COLOR, (i * self.CELL_SIZE + self.CELL_SIZE // 2, j * self.CELL_SIZE + self.CELL_SIZE // 2), self.KNIGHT_RADIUS + 5)
                    font = pygame.font.SysFont(None, 36)
                    move_num = font.render(str(board[i][j]), True, (0, 0, 255))
                    self.screen.blit(move_num, (i * self.CELL_SIZE + self.CELL_SIZE // 4, j * self.CELL_SIZE + self.CELL_SIZE // 4))


    def run(self, start_x=0, start_y=0):
        board_obj = KnightBoard()
        board_obj.board[start_x][start_y] = 0
        board_obj.solve_knight_tour(start_x, start_y, 1)

        move_count = 0
        total_moves = self.BOARD_SIZE * self.BOARD_SIZE
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if move_count < total_moves:
                move_count += 1

            self.draw_board()
            self.draw_path(board_obj.board, move_limit=move_count)
            pygame.display.flip()
            pygame.time.wait(500)

        pygame.quit()

if __name__ == '__main__':
    x = int(input("Enter the starting x position (0 to 7): "))
    y = int(input("Enter the starting y position (0 to 7): "))
    visualization = KnightsTourVisualization()
    visualization.run(x, y)
