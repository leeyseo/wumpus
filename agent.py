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
        self.escaped = False
        self.recent_moves = []      #최근 움직임 기록
        self.recent_positions = []  #최근 위치 기록
        self.dangerous_paths = set()   #위험한 위치 기록

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

        if action != 'Shoot':  #액션이 'Shoot'이 아닌 경우에만 체크
            #에이전트가 wumpus 위치에 있는지 확인
            if 'Wumpus' in world.grid[self.position[0]][self.position[1]]:
                print("Wumpus에게 죽었습니다.")
                self.dead = True
                self.remembered_danger.add(self.position)
                self.dangerous_paths.add(tuple(self.visited))  #위험한 경로 추가
                return True
            #에이전트가 웅덩이 위치에 있는지 확인
            if 'Pit' in world.grid[self.position[0]][self.position[1]]:
                print("Pit에 빠졌습니다.")
                self.dead = True
                self.remembered_danger.add(self.position)
                self.dangerous_paths.add(tuple(self.visited))  #위험한 경로 추가
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
            self.recent_moves.append(self.direction)
            if len(self.recent_moves) > 4: 
                self.recent_moves.pop(0)
        else:
            print("벽과 충돌")

    def turn_left(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index + 1) % 4]
        self.recent_moves.append('TurnLeft')
        if len(self.recent_moves) > 4: 
            self.recent_moves.pop(0)

    def turn_right(self):
        directions = ['North', 'West', 'South', 'East']
        current_index = directions.index(self.direction)
        self.direction = directions[(current_index - 1) % 4]
        self.recent_moves.append('TurnRight')
        if len(self.recent_moves) > 4:
            self.recent_moves.pop(0)

    def grab(self, world):
        if 'Glitter' in world.grid[self.position[0]][self.position[1]]:
            self.has_gold = True
            world.grid[self.position[0]][self.position[1]].remove('Glitter')
            print("금을 획득")

    def shoot(self, world):
        if self.arrows > 0:
            self.arrows -= 1
            print("화살 발사!!")
            #wumpus와 마주보고 있는가?
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
                self.escaped = True
            else:
                print("금 없이 탈출하셨네요...")
                self.dead = True
        else:
            print("여기서는 탈출이 안됩니다.")

    def revert_state(self):
        if self.previous_states:
            self.position, self.direction, self.arrows, self.dead, self.has_gold = self.previous_states.pop()

    def get_next_position(self):
        if self.direction == 'North':
            return (self.position[0] + 1, self.position[1])
        elif self.direction == 'East':
            return (self.position[0], self.position[1] + 1)
        elif self.direction == 'South':
            return (self.position[0] - 1, self.position[1])
        elif self.direction == 'West':
            return (self.position[0], self.position[1] - 1)

    #다음 행동 선택
    def decide_next_action(self, world):
        #만약 금을 가지고 있다면, 출발 위치로 돌아가 탈출 시도
        if self.has_gold:
            return self.return_to_start()

        current_cell = world.grid[self.position[0]][self.position[1]]

        adjacent_cells = [
            (self.position[0] + 1, self.position[1]),  # North
            (self.position[0] - 1, self.position[1]),  # South
            (self.position[0], self.position[1] + 1),  # East
            (self.position[0], self.position[1] - 1)   # West
        ]

        #현재 위치에 금이 있다면 금을 잡기
        if 'Glitter' in current_cell:
            return 'Grab'

        #주변 칸에 웅덩이 있다면 기억해 두기
        for cell in adjacent_cells:
            if world.is_valid_position(cell) and 'Pit' in world.grid[cell[0]][cell[1]]:
                self.remembered_danger.add(cell)

        #안전한 이동이 불가능한 경우, 주변 칸에 움퍼스가 있다면 화살 쏘기
        for cell in adjacent_cells:
            if world.is_valid_position(cell) and 'Wumpus' in world.grid[cell[0]][cell[1]]:
                if self.arrows > 0:
                    if cell == (self.position[0] + 1, self.position[1]):
                        self.direction = 'North'
                    elif cell == (self.position[0], self.position[1] + 1):
                        self.direction = 'East'
                    elif cell == (self.position[0] - 1, self.position[1]):
                        self.direction = 'South'
                    elif cell == (self.position[0], self.position[1] - 1):
                        self.direction = 'West'
                    return 'Shoot'
        
        #안전하고 방문하지 않은 첫 번째 칸으로 이동
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

        #방문하지 않은 안전한 칸이 없다면 새로운 방향 탐색
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

        #무한 루프 감지되면 방향을 바꿈
        if self.detect_loop():
            return random.choice(['TurnLeft', 'TurnRight'])

        #선택 가능한 모든 방향이 웅덩이거나 이미 방문한 경우 회전 선택
        return 'TurnLeft' if self.recent_moves[-1] != 'TurnLeft' else 'TurnRight'

    #시작 지점으로 이동
    def return_to_start(self):
        if self.position == (0, 0):
            return 'Climb'
        else:
            if self.position[0] > 0:
                self.direction = 'South'
            elif self.position[1] > 0:
                self.direction = 'West'
            return 'GoForward'

    #무한 루프 감지
    def detect_loop(self):
        #최근 위치와 움직임 패턴을 체크하여 무한 루프 감지
        if len(self.recent_positions) < 4:
            return False

        #같은 위치를 여러 번 방문하는지 확인
        if len(set(self.recent_positions[-4:])) < 4:
            print("무한 루프 감지: 위치 반복!")
            return True

        #같은 방향으로 반복해서 움직이는지 확인
        if len(self.recent_moves) >= 4:
            last_moves = self.recent_moves[-4:]
            if last_moves in [
                ['North', 'South', 'North', 'South'],
                ['South', 'North', 'South', 'North'],
                ['East', 'West', 'East', 'West'],
                ['West', 'East', 'West', 'East']
            ]:
                print("무한 루프 감지: 방향 반복!")
                return True

            #동일한 이동 패턴이 반복되는지 확인
            if last_moves in [
                ['GoForward', 'TurnLeft', 'GoForward', 'TurnRight'],
                ['GoForward', 'TurnRight', 'GoForward', 'TurnLeft']
            ]:
                print("무한 루프 감지: 이동 패턴 반복!")
                return True

        return False

    #웅덩이가 없는 방향 찾기
    def avoid_pit(self, world, adjacent_cells):
        safe_cells = []
        for cell in adjacent_cells:
            if world.is_valid_position(cell) and 'Pit' not in world.grid[cell[0]][cell[1]] and cell not in self.remembered_danger:
                safe_cells.append(cell)

        if safe_cells:
            next_cell = random.choice(safe_cells)
            if next_cell == (self.position[0] + 1, self.position[1]):
                self.direction = 'North'
            elif next_cell == (self.position[0], self.position[1] + 1):
                self.direction = 'East'
            elif next_cell == (self.position[0] - 1, self.position[1]):
                self.direction = 'South'
            elif next_cell == (self.position[0], self.position[1] - 1):
                self.direction = 'West'
            return 'GoForward'
    
        #안전한 칸이 없다면 방향을 바꿔 새로운 방향 탐색
        return random.choice(['TurnLeft', 'TurnRight'])