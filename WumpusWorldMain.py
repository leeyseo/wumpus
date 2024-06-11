from wumpus_world import WumpusWorld
from agent import Agent
import copy

def main():
    world = WumpusWorld()
    agent = Agent(start_position=(0, 0))

    #초기 설정에서 WUMPUS가 있는지 확인
    adjacent_cells = [
        (0, 1),  # East
        (1, 0)   # North
    ]

    for cell in adjacent_cells:
        if world.is_valid_position(cell) and 'Wumpus' in world.grid[cell[0]][cell[1]]:
            if agent.arrows > 0:
                agent.direction = 'East' if cell == (0, 1) else 'North'
                action = 'Shoot'
                agent.execute_action(action, world)
                break

    while True:
        previous_world = copy.deepcopy(world)
        previous_agent_state = (agent.position, agent.direction, agent.arrows, agent.dead, agent.has_gold)

        world.display_grid(agent.position, agent.direction)
        agent.display_status()

        agent.save_state()

        #자동으로 다음 행동 결정
        action = agent.decide_next_action(world)
        print(f"Selected action: {action}\n")

        agent_dead = agent.execute_action(action, world)

        if agent.escaped:
            break
 
        if agent_dead:
            print("에이전트가 죽었습니다. 게임 오버!")
            choice = input("게임을 끝내시겠습니까? (yes/no): ") 
            if choice.lower() == 'yes':
                print("게임을 종료합니다.")
                break
            else:
                print("에이전트가 시작 위치로 돌아갑니다.")
                agent.position = (0, 0)
                agent.direction = 'East'
                agent.dead = False
                agent.visited = set()
                agent.visited.add((0, 0))
                agent.has_gold = False
                agent.recent_moves = []
                agent.previous_states = []
                world = previous_world  #게임 맵도 초기 상태로 돌아감

if __name__ == "__main__":
    main()