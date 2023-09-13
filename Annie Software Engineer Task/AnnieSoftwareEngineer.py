import os
import random

class RabbitGame:
    def __init__(self, size, num_carrots, num_holes):
        self.size = size
        self.num_carrots = num_carrots
        self.num_holes = num_holes
        self.grid = [['-' for _ in range(size)] for _ in range(size)]
        self.rabbit_x, self.rabbit_y = random.randint(0, size - 1), random.randint(0, size - 1)
        self.grid[self.rabbit_y][self.rabbit_x] = 'r'

        self.carrot_positions = []
        self.place_items('c', self.num_carrots)

        self.rabbit_hole_positions = []
        self.place_items('O', self.num_holes)

        self.carrot_picked = False
        self.game_complete = False
        self.game_esc_exit = False

    def place_items(self, item, num_items):
        while num_items > 0:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if self.grid[y][x] == '-':
                self.grid[y][x] = item
                if item == 'c':
                    self.carrot_positions.append((x, y))
                elif item == 'O':
                    self.rabbit_hole_positions.append((x, y))
                num_items -= 1

    def move(self, direction):
        if self.game_complete:
            return

        new_x, new_y = self.rabbit_x, self.rabbit_y

        if direction == 'w':
            new_y -= 1
        elif direction == 'a':
            new_x -= 1
        elif direction == 's':
            new_y += 1
        elif direction == 'd':
            new_x += 1

        if self.is_valid_move(new_x, new_y):
            self.grid[self.rabbit_y][self.rabbit_x] = '-'
            self.rabbit_x, self.rabbit_y = new_x, new_y

            if self.grid[self.rabbit_y][self.rabbit_x] == 'c':
                self.pick_carrot()
            elif self.grid[self.rabbit_y][self.rabbit_x] == 'O':
                self.jump()

            self.grid[self.rabbit_y][self.rabbit_x] = 'r'
            self.print_map()

    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.grid[y][x] != 'O'

    def pick_carrot(self):
        if self.game_complete:
            return

        if self.carrot_picked:
            return

        self.carrot_positions.remove((self.rabbit_x, self.rabbit_y))
        self.grid[self.rabbit_y][self.rabbit_x] = 'R'
        self.carrot_picked = True
        self.print_map()

        if not self.carrot_positions:
            self.game_complete = True
            print("Congratulations! You won!")

    def jump(self):
        if self.game_complete:
            return

        if not self.carrot_picked:
            return

        for hole_x, hole_y in self.rabbit_hole_positions:
            if hole_x != self.rabbit_x and hole_y != self.rabbit_y:
                continue

            self.grid[self.rabbit_y][self.rabbit_x] = '-'
            self.rabbit_x, self.rabbit_y = hole_x, hole_y
            self.grid[self.rabbit_y][self.rabbit_x] = 'R'
            self.print_map()
            self.game_complete = True
            print("Congratulations! You won!")

    def print_map(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.grid:
            print(' '.join(row))

def main():
    size = int(input("Enter the size of the grid: "))
    num_carrots = int(input("Enter the number of carrots: "))
    num_holes = int(input("Enter the number of rabbit holes: "))

    game = RabbitGame(size, num_carrots, num_holes)

    print("\nInstructions:")
    print("Press Enter to Play the game; Press any other key to Quit.")
    input()

    while not game.game_complete and not game.game_esc_exit:
        move = input("Enter movement (w/a/s/d/j/p or 'esc' to quit): ")
        if move == "esc":
            game.game_esc_exit = True
            break
        elif move in ['w', 'a', 's', 'd']:
            game.move(move)
        elif move == "j":
            game.jump()
        elif move == "p":
            game.pick_carrot()

if __name__ == "__main__":
    main()
