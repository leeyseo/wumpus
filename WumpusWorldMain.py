from wumpus_world import WumpusWorld
from agent import Agent
import copy

def main():
    world = WumpusWorld()
    agent = Agent(start_position=(0, 0))

    while True:
        previous_world = copy.deepcopy(world)
        previous_agent_state = (agent.position, agent.direction, agent.arrows, agent.dead, agent.has_gold)

        world.display_grid(agent.position, agent.direction)
        agent.display_status()

        agent.save_state()

        # Decide next action automatically
        action = agent.decide_next_action(world)
        print(f"Selected action: {action}")

        agent_dead = agent.execute_action(action, world)

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
                # Remember the dangers discovered so far
                agent.remembered_danger.add(agent.position)
                world = previous_world  # 게임 맵도 초기 상태로 돌아감

if __name__ == "__main__":
    main()
