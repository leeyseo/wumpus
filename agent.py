import random

class Agent:
    def __init__(self, start_position):
        self.position = start_position
        self.direction = 'East'
        self.arrows = 3
        self.dead = False
        self.has_gold = False
        self.visited = set()
        self.remembered_danger = set()
        self.wumpus_killed = False
        self.previous_states = []

    def save_state(self):
        self.previous_states.append((self.position, self.direction, self.arrows, self.dead, self.has_gold))

    def display_status(self):
        print(f"현재 위치: {self.position}, 방향: {self.direction}, 화살: {self.arrows}, 금 획득: {self.has_gold}")

    def execute_action(self, action, world):
        if action == 'GoForward':
            self.move_forward(world)
        elif action == 'TurnLeft':
            self.turn_left()
        elif action == 'TurnRight':
            self.turn_right()
        elif action == 'Grab':
            self.grab(world)
        elif action == 'Shoot':
            self.shoot(world)
        elif action == 'Climb':
            self.climb()
        
        # Check if agent is in the same position as the Wumpus
        if 'Wumpus' in world.grid[self.position[0]][self.position[1]]:
            print("Wumpus에게 죽었습니다.")
            self.dead = True
            self.remembered_danger.add(self.position)
            return True
        return self.dead

    def move_forward(self, world):
        new_position = self.position
        if self.direction == 'North':
            new_position = (self.position[0] + 1, self.position[1])
        elif self.direction == 'East':
            new_position = (self.position[0], self.position[1] + 1)
        elif self.direction == 'South':
            new_position = (self.position[0] - 1, self.position[1])
        elif self.direction == 'West':
            new_position = (self.position[0], self.position[1] - 1)

        if world.is_valid_position(new_position):
            self.position = new_position
            self.visited.add(self.position)
        else:
            print("벽과 충돌")

    def turn_left(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]

    def turn_right(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1) % 4]

    def grab(self, world):
        if 'Glitter' in world.grid[self.position[0]][self.position[1]]:
            self.has_gold = True
            world.grid[self.position[0]][self.position[1]].remove('Glitter')
            print("금을 획득")

    def shoot(self, world):
        if self.arrows > 0:
            self.arrows -= 1
            print("화살 발사!!")
            # wumpus와 마주보고 있는가?
            if self.direction == 'North':
                wumpus_position = (self.position[0] + 1, self.position[1])
            elif self.direction == 'East':
                wumpus_position = (self.position[0], self.position[1] + 1)
            elif self.direction == 'South':
                wumpus_position = (self.position[0] - 1, self.position[1])
            elif self.direction == 'West':
                wumpus_position = (self.position[0], self.position[1] - 1)
            
            if world.is_valid_position(wumpus_position) and 'Wumpus' in world.grid[wumpus_position[0]][wumpus_position[1]]:
                print("WUMPUS 사냥 성공!!")
                world.grid[wumpus_position[0]][wumpus_position[1]].remove('Wumpus')
                self.wumpus_killed = True
        else:
            print("화살 없음 --> 다 썼음")

    def climb(self):
        if self.position == (0, 0):
            if self.has_gold:
                print("금과 함께 탈출 성공!")
                self.dead = True
            else:
                print("금 없이 탈출하셨네요...")
                self.dead = True
        else:
            print("여기서는 탈출이 안됩니다.")

    def revert_state(self):
        if self.previous_states:
            self.position, self.direction, self.arrows, self.dead, self.has_gold = self.previous_states.pop()

    def decide_next_action(self, world):
        # Simple Reflex with State agent logic
        current_cell = world.grid[self.position[0]][self.position[1]]
        adjacent_cells = [
            (self.position[0] + 1, self.position[1]),
            (self.position[0] - 1, self.position[1]),
            (self.position[0], self.position[1] + 1),
            (self.position[0], self.position[1] - 1)
        ]

        # If gold is here, grab it
        if 'Glitter' in current_cell:
            return 'Grab'

        # Check adjacent cells for Wumpus or Pit
        for cell in adjacent_cells:
            if world.is_valid_position(cell):
                if 'Wumpus' in world.grid[cell[0]][cell[1]] and not self.wumpus_killed:
                    if self.arrows > 0:
                        return 'Shoot'
                if 'Pit' in world.grid[cell[0]][cell[1]]:
                    continue  # Skip dangerous cell

        # Move to the next unvisited cell
        for cell in adjacent_cells:
            if world.is_valid_position(cell) and cell not in self.visited and cell not in self.remembered_danger:
                if cell == (self.position[0] + 1, self.position[1]):
                    self.direction = 'North'
                elif cell == (self.position[0], self.position[1] + 1):
                    self.direction = 'East'
                elif cell == (self.position[0] - 1, self.position[1]):
                    self.direction = 'South'
                elif cell == (self.position[0], self.position[1] - 1):
                    self.direction = 'West'
                return 'GoForward'

        # Try to move to a visited cell if no unvisited cell is found
        for cell in adjacent_cells:
            if world.is_valid_position(cell) and cell not in self.remembered_danger:
                if cell == (self.position[0] + 1, self.position[1]):
                    self.direction = 'North'
                elif cell == (self.position[0], self.position[1] + 1):
                    self.direction = 'East'
                elif cell == (self.position[0] - 1, self.position[1]):
                    self.direction = 'South'
                elif cell == (self.position[0], self.position[1] - 1):
                    self.direction = 'West'
                return 'GoForward'

        # If no valid move is found, turn to explore new directions
        return random.choice(['TurnLeft', 'TurnRight'])
