import random
import copy
import numpy as np
from omok import OmokState

DEPTH = 1


def get_next_stones(node):
    '''
    0이 아닌걸 고르고
    걔 주변 좌우 상하 대각 -1 ~ +1
    '''

    state = node[0]
    next_stones = set()
    cur_stone = node[1] # last history
        
    x_min = cur_stone[0] - 1 if cur_stone[0] - 1 > 0 else 0
    x_max = cur_stone[0] + 1 if cur_stone[0] + 1 < 18 else 18
    x_pos = np.arange(x_min, x_max+1)
    
    y_min = cur_stone[1] - 1 if cur_stone[1] - 1 > 0 else 0
    y_max = cur_stone[1] + 1 if cur_stone[1] + 1 < 18 else 18
    y_pos = np.arange(y_min, y_max+1)

    avail_stones = np.where(state == 0)
    avail_stones = set([(x,y) for x, y in zip(avail_stones[0], avail_stones[1])])

    [next_stones.add((x,y)) for x in x_pos for y in y_pos]

    next_stones = next_stones & avail_stones
    
    return list(next_stones)
    

def a_b(node, depth, a, b, player):
    if depth == 0 :         # evaluation

        x_pos, y_pos = node[1]
        # print("pos") 
        # print(x_pos, y_pos)

        state = node[0]

        cur_stone = state[x_pos][y_pos]

        x_min = x_pos - 5 if x_pos - 5 > 0 else 0
        x_max = x_pos + 5 if x_pos + 5 < 18 else 18

        y_min = y_pos - 5 if y_pos - 5 > 0 else 0
        y_max = y_pos + 5 if y_pos + 5 < 18 else 18

        score = 1   
        for x in range(x_min+1, x_max+1):
            for y in range(y_min+1, y_max+1):
                if state[x][y] == cur_stone:
                    if state[x-1][y-1] == state[x][y]:
                        score += 1
                    if state[x][y-1] == state[x][y]:
                        score += 1
                    if state[x-1][y] == state[x][y]:
                        score += 1
        
        return (score, None)
    if player == -1:        # 나(백)의 입장
        stones = get_next_stones(node)
        state = node[0]
        v = float("-inf")

        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)    # deep copy
            child_state[stone[0]][stone[1]] = 1             # 상대는 어떻게
            child_node = (child_state, stone, 0)
            v = max(v, a_b(child_node, depth-1, a, b, 1)[0] )
            a = max(a, v)
            if b <= a:
                break
        
        return (v, pos)
    elif player == 1:       # 상대(흑)의 입장
        state = node[0]
        v = float("inf")
        stones = get_next_stones(node)
        pos = None
        for stone in stones:
            pos = stone
            child_state = np.copy(state)
            child_state[stone[0]][stone[1]] = -1 # 백 이라면
            child_node = (child_state, stone, 0)

            v = min(v, a_b(child_node, depth-1, a, b, -1)[0] )
            b = min(b, v)

            if b <= a:
                break
            
        return (v, pos)


    
#나 백돌
def act(state : OmokState):
    
    if len(state.history) == 0:
        return 9,9
    while True:
        prev_stone = state.history[-1]  # 흑돌
        node = (state.game_board, prev_stone, 0)
        # 노드 구성 : 
        #           game_board, 이전 돌, cost

        v, pos = a_b(node, DEPTH, 1, 2, state.turn*-1) # a-b prunning
        # v : value
        # pos : 돌 위치
        
        x_pos, y_pos = pos[0], pos[1]        

        # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
        if state.is_valid_position(x_pos, y_pos):
            break
    

    return y_pos, x_pos