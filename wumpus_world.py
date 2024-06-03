import random
import copy

class WumpusWorld:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        self.agent_pos = (0, 0)  # 시작 위치를 왼쪽 하단 모서리로 변경 (0,0)
        self.agent_direction = 'East'
        self.arrows = 3
        self.generate_world()

    def generate_world(self):
        # 모든 격자에 대한 좌표 리스트 생성
        all_cells = [(x, y) for x in range(self.size) for y in range(self.size)]
        all_cells.remove((0, 0))  # 시작 위치는 안전한 격자로 남겨둠

        # 골드의 위치를 무작위로 정함
        gold_pos = random.choice(all_cells)
        all_cells.remove(gold_pos)  # 이미 골드가 있는 위치는 제거

        # 움퍼스의 위치를 무작위로 정함
        wumpus_pos = random.choice(all_cells)
        all_cells.remove(wumpus_pos)  # 이미 움퍼스가 있는 위치는 제거

        # 웅덩이의 위치를 무작위로 정함
        pit_pos = random.choice(all_cells)
        all_cells.remove(pit_pos)  # 이미 웅덩이가 있는 위치는 제거

        # 각 요소의 위치를 그리드에 할당
        self.grid[gold_pos[0]][gold_pos[1]].append('Glitter')
        self.grid[wumpus_pos[0]][wumpus_pos[1]].append('Wumpus')
        self.grid[pit_pos[0]][pit_pos[1]].append('Pit')

        # 추가적인 요소들을 무작위로 배치
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) == (0, 0) or (row, col) in [gold_pos, wumpus_pos, pit_pos]:
                    continue  # 시작 위치와 이미 배치된 위치는 건너뜀

                if random.random() < 0.1:
                    if 'Glitter' not in self.grid[row][col]:  # 이미 금이 있는 위치는 건너뜀
                        self.grid[row][col].append('Glitter')
                elif random.random() < 0.1:
                    if 'Wumpus' not in self.grid[row][col]:  # 이미 움퍼스가 있는 위치는 건너뜀
                        self.grid[row][col].append('Wumpus')
                elif random.random() < 0.1:
                    if 'Pit' not in self.grid[row][col]:  # 이미 웅덩이가 있는 위치는 건너뜀
                        self.grid[row][col].append('Pit')

    def is_valid_position(self, position):
        x, y = position
        return 0 <= x < self.size and 0 <= y < self.size

    def display_grid(self, agent_position, agent_direction):
        print("-" * (self.size * 4 + 1))
        for row in range(self.size - 1, -1, -1):
            print("|", end="")
            for col in range(self.size):
                cell = self.grid[row][col]
                symbol = ' '
                if 'Glitter' in cell:
                    symbol += 'G'
                if 'Wumpus' in cell:
                    symbol += 'W'
                if 'Pit' in cell:
                    symbol += 'B'
                if (row, col) == agent_position:
                    symbol += 'A'
                    if agent_direction == 'North':
                        symbol += '^'
                    elif agent_direction == 'East':
                        symbol += '>'
                    elif agent_direction == 'South':
                        symbol += 'v'
                    elif agent_direction == 'West':
                        symbol += '<'
                print(symbol.ljust(3) + "|", end=" ")
            print()
            print("-" * (self.size * 4 + 1))
        
        for row in range(self.size):
            for col in range(self.size):
                cell = self.grid[row][col]
                if (row + 1, col) == agent_position or (row - 1, col) == agent_position or \
                   (row, col + 1) == agent_position or (row, col - 1) == agent_position:
                    if 'Wumpus' in cell:
                        print('Wumpus 근처에 있습니다.')
                    elif 'Pit' in cell:
                        print('웅덩이 근처에 있습니다.')