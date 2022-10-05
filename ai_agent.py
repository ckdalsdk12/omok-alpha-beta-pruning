import numpy as np
from omok import OmokState
import copy


def act(state: OmokState):
    # DO something

    # 첫 턴이면 한 가운데에 돌 두기
    if state.num_stones == 0:
        return 9, 9

    # 자가 복제 배틀을 위한 코드 (백 돌 일때 첫 수)
    if state.num_stones == 1:
        while True:
            opponent_last_stone = state.history[-1]
            x_pos = opponent_last_stone[0] + np.random.randint(-1, 2)
            y_pos = opponent_last_stone[1] + np.random.randint(-1, 2)
            if x_pos >= 19 or x_pos <= -1 or y_pos >= 19 or y_pos <= -1:
                continue
            if x_pos != 0 or y_pos != 0:
                break
        return y_pos, x_pos

    # 알파 베타 가지치기를 호출, 가능한 좌표 중에서 최선의 수 좌표를 받고 리턴
    # 아래 라인에서 depth 조정
    depth = 2  # TODO : 깊이가 3 이상일 경우 타임아웃 및 여러 가지 문제로 제대로 작동하지 않음.
    a = float('-inf')
    b = float('+inf')
    returned_tuple = alphabeta(state, depth, a, b, True)  # 리턴 값 = (점수, (x좌표, y좌표))
    returned_node = returned_tuple[1]
    y_pos = returned_node[1]
    x_pos = returned_node[0]
    # print("점수 :", returned_tuple[0])  # 디버깅 용
    # print("좌표 :", returned_node)  # 디버깅 용
    return y_pos, x_pos


def alphabeta(state: OmokState, depth, a, b, maximizingPlayer):
    if depth == 0 or state.num_stones == state.board_size * state.board_size:
        sum_score = 0  # 현 상태의 스코어 합
        if state.turn == -1:
            my_last_stone = state.history[-2]  # 마지막 백 돌 좌표 튜플
            opponent_last_stone = state.history[-1]  # 마지막 흑 돌 좌표 튜플
        if state.turn == 1:
            my_last_stone = state.history[-1]  # 마지막 백 돌 좌표 튜플
            opponent_last_stone = state.history[-2]  # 마지막 흑 돌 좌표 튜플

        # score01 = 마지막 돌 5x5 반경에 돌이 있는 개수만큼 점수 부여
        score01 = 0

        # 공격
        # for row in range(my_last_stone[0] - 2, my_last_stone[0] + 3):
        #     for col in range(my_last_stone[1] - 2, my_last_stone[1] + 3):
        #         if row >= 19 or row <= -1 or col >= 19 or col <= -1:
        #             continue
        #         if state.game_board[row][col] == 1:
        #             score01 += 1

        # 방어
        # for row in range(opponent_last_stone[0] - 2, opponent_last_stone[0] + 3):
        #     for col in range(opponent_last_stone[1] - 2, opponent_last_stone[1] + 3):
        #         if row >= 19 or row <= -1 or col >= 19 or col <= -1:
        #             continue
        #         if state.game_board[row][col] == -1:
        #             score01 -= 1

        sum_score += score01

        # score02 = 2개 연속을 만들 수 있으면 가능한 개수만큼 점수 부여
        score02 = 0

        # 공격
        base_score = 100
        # 가로
        for col in range(my_last_stone[0] - 1, my_last_stone[0] + 1):
            row = my_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 2]) == -2:
                out_01 = col - 1
                out_02 = col + 2
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score02 += base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score02 += base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score02 += base_score * 0.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score02 += base_score * 1.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score02 += base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score02 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score02 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == -1:
                    score02 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(my_last_stone[1] - 1, my_last_stone[1] + 1):
            col = my_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 2, col]) == -2:
                out_01 = row - 1
                out_02 = row + 2
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score02 += base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score02 += base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score02 += base_score * 0.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score02 += base_score * 1.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score02 += base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == -1:
                    score02 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-1, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(2):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 2:
                out_01 = (row - 1, col - 1)
                out_02 = (row + 2, col + 2)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-1, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(2):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 2:
                out_01 = (row + 1, col - 1)
                out_02 = (row - 2, col + 2)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        # 방어
        base_score = 100 - 1
        # 가로
        for col in range(opponent_last_stone[0] - 1, opponent_last_stone[0] + 1):
            row = opponent_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 2]) == 2:
                out_01 = col - 1
                out_02 = col + 2
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score02 -= base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score02 -= base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score02 -= base_score * 1.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score02 -= base_score * 0.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score02 -= base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score02 -= base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score02 -= base_score * 0.75
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 1:
                    score02 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(opponent_last_stone[1] - 1, opponent_last_stone[1] + 1):
            col = opponent_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 2, col]) == 2:
                out_01 = row - 1
                out_02 = row + 2
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score02 -= base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 1:
                    score02 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-1, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(2):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 2:
                out_01 = (row - 1, col - 1)
                out_02 = (row + 2, col + 2)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-1, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(2):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 2:
                out_01 = (row + 1, col - 1)
                out_02 = (row - 2, col + 2)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score02 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score02 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        sum_score += int(score02)

        # score03 = 3개 연속을 만들 수 있으면 가능한 개수만큼 점수 부여
        score03 = 0

        # TODO : 상하좌우 중 우, 하는 제대로 작동하지만 좌, 상은 제대로 작동하지 않음. 좌표 관련해 수정 필요
        # 공격
        base_score = 10000
        # 가로
        for col in range(my_last_stone[0] - 2, my_last_stone[0] + 1):
            row = my_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 3]) == -3:
                out_01 = col - 1
                # out_02 = col + 4
                out_02 = col + 3
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score03 += base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score03 += base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score03 += base_score * 0.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score03 += base_score * 1.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score03 += base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score03 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score03 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == -1:
                    score03 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(my_last_stone[1] - 2, my_last_stone[1] + 1):
            col = my_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 3, col]) == -3:
                out_01 = row - 1
                # out_02 = row + 4
                out_02 = row + 3
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score03 += base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score03 += base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score03 += base_score * 0.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score03 += base_score * 1.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score03 += base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == -1:
                    score03 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-2, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(3):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 3:
                out_01 = (row - 1, col - 1)
                # out_02 = (row + 4, col + 4)
                out_02 = (row + 3, col + 3)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-2, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(3):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 3:
                out_01 = (row + 1, col - 1)
                # out_02 = (row - 4, col + 4)
                out_02 = (row - 3, col + 3)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        # 방어
        base_score = 10000 - 1
        # 가로
        for col in range(opponent_last_stone[0] - 2, opponent_last_stone[0] + 1):
            row = opponent_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 3]) == 3:
                out_01 = col - 1
                # out_02 = col + 4
                out_02 = col + 3
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score03 -= base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score03 -= base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score03 -= base_score * 1.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score03 -= base_score * 0.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score03 -= base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score03 -= base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score03 -= base_score * 0.75
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 1:
                    score03 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(opponent_last_stone[1] - 2, opponent_last_stone[1] + 1):
            col = opponent_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 3, col]) == 3:
                out_01 = row - 1
                # out_02 = row + 4
                out_02 = row + 3
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score03 -= base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 1:
                    score03 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-2, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(3):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 3:
                out_01 = (row - 1, col - 1)
                # out_02 = (row + 4, col + 4)
                out_02 = (row + 3, col + 3)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-2, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(3):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 3:
                out_01 = (row + 1, col - 1)
                # out_02 = (row - 4, col + 4)
                out_02 = (row - 3, col + 3)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score03 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score03 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        sum_score += int(score03)

        # score04 = 4개 연속을 만들 수 있으면 가능한 개수만큼 점수 부여
        score04 = 0

        # TODO : 상하좌우 중 우, 하는 제대로 작동하지만 좌, 상은 제대로 작동하지 않음. 좌표 관련해 수정 필요
        # 공격
        base_score = 1000000
        # 가로
        for col in range(my_last_stone[0] - 3, my_last_stone[0] + 1):
            row = my_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 4]) == -4:
                out_01 = col - 1
                # out_02 = col + 5
                out_02 = col + 4
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score04 += base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score04 += base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score04 += base_score * 0.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score04 += base_score * 1.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score04 += base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score04 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score04 += base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == -1:
                    score04 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(my_last_stone[1] - 3, my_last_stone[1] + 1):
            col = my_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 4, col]) == -4:
                out_01 = row - 1
                # out_02 = row + 5
                out_02 = row + 4
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score04 += base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score04 += base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score04 += base_score * 0.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score04 += base_score * 1.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score04 += base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == -1:
                    score04 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-3, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(4):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 4:
                out_01 = (row - 1, col - 1)
                # out_02 = (row + 5, col + 5)
                out_02 = (row + 4, col + 4)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-3, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(4):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 4:
                out_01 = (row + 1, col - 1)
                # out_02 = (row - 5, col + 5)
                out_02 = (row - 4, col + 4)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 += base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 += base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 += base_score * 2
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        # 방어
        base_score = 1000000 - 1
        # 가로
        for col in range(opponent_last_stone[0] - 3, opponent_last_stone[0] + 1):
            row = opponent_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 4]) == 4:
                out_01 = col - 1
                # out_02 = col + 5
                out_02 = col + 4
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 0:
                    score04 -= base_score
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == 1:
                    score04 -= base_score * 1.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 0:
                    score04 -= base_score * 1.5
                elif state.game_board[row][out_01] == 0 and state.game_board[row][out_02] == -1:
                    score04 -= base_score * 0.5
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 0:
                    score04 -= base_score * 0.5
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == -1:
                    score04 -= base_score * 0.75
                elif state.game_board[row][out_01] == -1 and state.game_board[row][out_02] == 1:
                    score04 -= base_score * 0.75
                elif state.game_board[row][out_01] == 1 and state.game_board[row][out_02] == 1:
                    score04 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(opponent_last_stone[1] - 3, opponent_last_stone[1] + 1):
            col = opponent_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 4, col]) == 4:
                out_01 = row - 1
                # out_02 = row + 5
                out_02 = row + 4
                if out_01 >= 19 or out_01 <= -1 or out_02 >= 19 or out_02 <= -1:
                    continue
                if state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 0:
                    score04 -= base_score
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == 1:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 0:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01][col] == 0 and state.game_board[out_02][col] == -1:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 0:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == -1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01][col] == -1 and state.game_board[out_02][col] == 1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01][col] == 1 and state.game_board[out_02][col] == 1:
                    score04 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-3, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(4):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 4:
                out_01 = (row - 1, col - 1)
                # out_02 = (row + 5, col + 5)
                out_02 = (row + 4, col + 4)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-3, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(4):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 4:
                out_01 = (row + 1, col - 1)
                # out_02 = (row - 5, col + 5)
                out_02 = (row - 4, col + 4)
                if out_01[0] >= 19 or out_01[0] <= -1 or out_01[1] >= 19 or out_01[1] <= -1:
                    continue
                if out_02[0] >= 19 or out_02[0] <= -1 or out_02[1] >= 19 or out_02[1] <= -1:
                    continue
                if state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score * 1.5
                elif state.game_board[out_01[0]][out_01[1]] == 0 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 0:
                    score04 -= base_score * 0.5
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == -1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == -1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 0.75
                elif state.game_board[out_01[0]][out_01[1]] == 1 and state.game_board[out_02[0]][out_02[1]] == 1:
                    score04 -= base_score * 2
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        sum_score += int(score04)

        # score05 = 5개 연속을 만들 수 있으면 점수 부여
        score05 = 0

        # 공격
        base_score = 100000000 * 10
        # 가로
        for col in range(my_last_stone[0] - 4, my_last_stone[0] + 1):
            row = my_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 5]) == -5:
                score05 += base_score
                # return score05, (0, 0)
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅

        # 세로
        for row in range(my_last_stone[1] - 4, my_last_stone[1] + 1):
            col = my_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 5, col]) == -5:
                score05 += base_score
                # return score05, (0, 0)
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-4, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(5):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 5:
                score05 += base_score
                # return score05, (0, 0)
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-4, 1):
            row = my_last_stone[1]
            col = my_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(5):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == -1:
                    count_sum += 1
            if count_sum == 5:
                score05 += base_score
                # return score05, (0, 0)
                # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅

        # 방어
        base_score = 100000000 - 1
        # 가로
        for col in range(opponent_last_stone[0] - 4, opponent_last_stone[0] + 1):
            row = opponent_last_stone[1]
            if col >= 19 or col <= -1:
                continue
            if np.sum(state.game_board[row, col:col + 5]) == 5:
                score05 -= base_score
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("가로")  # 디버깅
                # print(f"score01 : {score01}, score02 : {score02}, score03 : {score03}, score04 : {score04}, "
                #       f"score05 : {score05}")  # 디버깅

        # 세로
        for row in range(opponent_last_stone[1] - 4, opponent_last_stone[1] + 1):
            col = opponent_last_stone[0]
            if row >= 19 or row <= -1:
                continue
            if np.sum(state.game_board[row:row + 5, col]) == 5:
                score05 -= base_score
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("세로")  # 디버깅
                # print(f"score01 : {score01}, score02 : {score02}, score03 : {score03}, score04 : {score04}, "
                #       f"score05 : {score05}")  # 디버깅

        # 대각선 좌(상)우(하)
        for i in range(-4, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row += i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(5):
                copied_row = row + j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 5:
                score05 -= base_score
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(좌우)")  # 디버깅
                # print(f"score01 : {score01}, score02 : {score02}, score03 : {score03}, score04 : {score04}, "
                #       f"score05 : {score05}")  # 디버깅

        # 대각선 우(상)좌(하)
        for i in range(-4, 1):
            row = opponent_last_stone[1]
            col = opponent_last_stone[0]
            count_sum = 0
            row -= i
            col += i
            if row >= 19 or row <= -1:
                continue
            if col >= 19 or col <= -1:
                continue
            for j in range(5):
                copied_row = row - j
                copied_col = col + j
                if copied_row >= 19 or copied_row <= -1:
                    continue
                if copied_col >= 19 or copied_col <= -1:
                    continue
                if state.game_board[copied_row, copied_col] == 1:
                    count_sum += 1
            if count_sum == 5:
                score05 -= base_score
                # print(f"x : {opponent_last_stone[0]}, y : {opponent_last_stone[1]}")  # 디버깅
                # print("대각선(우좌)")  # 디버깅
                # print(f"score01 : {score01}, score02 : {score02}, score03 : {score03}, score04 : {score04}, "
                #       f"score05 : {score05}")  # 디버깅

        sum_score += score05

        # 점수 계산 뒤에 리턴
        return sum_score, (0, 0)  # 리프 노드의 좌표는 사용하지 않으므로 state.history[-2] 대신 (0, 0) 리턴

    if maximizingPlayer:
        value = float('-inf')
        returned_node = tuple()  # 빈 튜플
        # 지금까지 뒀던 흑돌들의 좌표에서 5x5 범위의 빈 좌표를 파악
        # TODO : 3x3, 5x5, 7x7 순으로 범위를 넓혀가면 정확도를 높일 수 있을 것
        avail = set()
        for i in range(-2, -state.num_stones - 1, -2):
            start = -3
            end = 4
            for x in range(start, end):
                for y in range(start, end):
                    y_pos = state.history[i][1] + y
                    x_pos = state.history[i][0] + x

                    # is_valid_position 메소드가 완벽하지 않으므로 체크 한단계 추가
                    if x_pos >= 19 or x_pos <= -1 or y_pos >= 19 or y_pos <= -1:
                        continue

                    # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
                    if state.is_valid_position(x_pos, y_pos):
                        avail.add((x_pos, y_pos))  # 모두 통과하면 avail에 추가
        for node in avail:
            copied_state = copy.deepcopy(state)  # 다음 시도가 영향 받지 않도록 상태 복사하여 사용
            copied_state.update(node[0], node[1])
            # TODO : depth에 따라 값 변경 필요. 수정 필요.
            if depth == 3:
                if check_win(copied_state):
                    return float('inf'), node
            # max일때의 점수 값과 좌표를 튜플로 리턴
            child_value = alphabeta(copied_state, depth - 1, a, b, False)[0]
            value = max(value, child_value)
            if value == child_value:
                returned_node = node
                # print(value, node)  # 디버깅
            # print(a, b)  # 디버깅
            a = max(a, value)
            if value > b:
                # print(f"{value} > {b}")  # 디버깅
                # print("---브레이크---")  # 디버깅
                break
        # print(returned_node)  # 디버깅
        return value, returned_node
    else:
        value = float('inf')
        returned_node = tuple()  # 빈 튜플
        # 지금까지 뒀던 백돌들의 좌표에서 5x5 범위의 빈 좌표를 파악
        # TODO : 3x3, 5x5, 7x7 순으로 범위를 넓혀가면 정확도를 높일 수 있을 것
        avail = set()
        for i in range(-2, -state.num_stones, -2):
            start = -3
            end = 4
            for x in range(start, end):
                for y in range(start, end):
                    y_pos = state.history[i][1] + y
                    x_pos = state.history[i][0] + x

                    # is_valid_position 메소드가 완벽하지 않으므로 체크 한단계 추가
                    if x_pos >= 19 or x_pos <= -1 or y_pos >= 19 or y_pos <= -1:
                        continue

                    # state에서 생성된 좌표에 돌이 올려져 있는지 여부 체크
                    if state.is_valid_position(x_pos, y_pos):
                        avail.add((x_pos, y_pos))  # 모두 통과하면 avail에 추가
        for node in avail:
            copied_state = copy.deepcopy(state)  # 다음 시도가 영향 받지 않도록 상태 복사하여 사용
            copied_state.update(node[0], node[1])
            # min일때의 점수 값과 좌표를 튜플로 리턴
            child_value = alphabeta(copied_state, depth - 1, a, b, True)[0]
            value = min(value, child_value)
            if value == child_value:
                returned_node = node
                # print(value, node)  # 디버깅
            # print(a, b)  # 디버깅
            b = min(b, value)
            if value < a:
                # print(f"{value} < {a}")  # 디버깅
                # print("---브레이크---")  # 디버깅
                break
        # print(returned_node)  # 디버깅
        return value, returned_node


def check_win(state):
    win = False

    if state.turn == -1:
        my_last_stone = state.history[-2]  # 마지막 백 돌 좌표 튜플
    if state.turn == 1:
        my_last_stone = state.history[-1]  # 마지막 백 돌 좌표 튜플

    # 가로
    for col in range(my_last_stone[0] - 4, my_last_stone[0] + 1):
        row = my_last_stone[1]
        if col >= 19 or col <= -1:
            continue
        if np.sum(state.game_board[row, col:col + 5]) == -5:
            win = True
            # score05 = float('inf')
            # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
            # print("가로")  # 디버깅

    # 세로
    for row in range(my_last_stone[1] - 4, my_last_stone[1] + 1):
        col = my_last_stone[0]
        if row >= 19 or row <= -1:
            continue
        if np.sum(state.game_board[row:row + 5, col]) == -5:
            win = True
            # score05 = float('inf')
            # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
            # print("세로")  # 디버깅

    # 대각선 좌(상)우(하)
    for i in range(-4, 1):
        row = my_last_stone[1]
        col = my_last_stone[0]
        count_sum = 0
        row += i
        col += i
        if row >= 19 or row <= -1:
            continue
        if col >= 19 or col <= -1:
            continue
        for j in range(5):
            copied_row = row + j
            copied_col = col + j
            if copied_row >= 19 or copied_row <= -1:
                continue
            if copied_col >= 19 or copied_col <= -1:
                continue
            if state.game_board[copied_row, copied_col] == -1:
                count_sum += 1
        if count_sum == 5:
            win = True
            # score05 = float('inf')
            # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
            # print("대각선(좌우)")  # 디버깅

    # 대각선 우(상)좌(하)
    for i in range(-4, 1):
        row = my_last_stone[1]
        col = my_last_stone[0]
        count_sum = 0
        row -= i
        col += i
        if row >= 19 or row <= -1:
            continue
        if col >= 19 or col <= -1:
            continue
        for j in range(5):
            copied_row = row - j
            copied_col = col + j
            if copied_row >= 19 or copied_row <= -1:
                continue
            if copied_col >= 19 or copied_col <= -1:
                continue
            if state.game_board[copied_row, copied_col] == -1:
                count_sum += 1
        if count_sum == 5:
            win = True
            # score05 = float('inf')
            # print(f"x : {my_last_stone[0]}, y : {my_last_stone[1]}")  # 디버깅
            # print("대각선(우좌)")  # 디버깅

    return win
