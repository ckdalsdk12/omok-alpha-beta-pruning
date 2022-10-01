import sys
import copy

import pygame
from stopit import ThreadingTimeout

from omok import Omok, OmokState
import user_agent
import ai_agent
from util import random_act

TIMEOUT = 5
HUMAN = True


def update(state : OmokState, omok_ui : Omok, x_pos, y_pos):
    state.update(x_pos, y_pos)  # state update
    omok_ui.update(state)       # ui update
    pygame.display.update()

    status = state.check_status()
    if status is not None:
        # 승리 표시 화면의 클릭 여부를 mouse_clicked로 반환 받음
        mouse_clicked = omok_ui.display_result(status)
        pygame.display.update()
        # 승리 표시 화면 클릭 시 재시작
        if mouse_clicked:
            state.reset() # 오목 state reset 
            omok_ui.board_draw() # 오목 바둑판 그리기
            omok_ui.title_msg() # 오목 타이틀 그리기
            omok_ui.turn_msg(state.turn) # 오목 턴 메시지 띄우기
            pygame.display.update()

def play_ai_vs_human(state : OmokState, omok_ui : Omok):
    while True:
        # 클릭 이벤트 처리
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    valid, pos = omok_ui.is_valid_click(state, mouse_pos)
                    mouse_clicked = valid

        if state.turn == 1:  # 흑돌 (AI)
            with ThreadingTimeout(TIMEOUT) as context_manager:
                y_pos, x_pos = user_agent.act(copy.deepcopy(state))

            if context_manager.state == context_manager.TIMED_OUT:
                print("Timeout!")
                y_pos, x_pos = random_act(state)

            do_action = True

        elif state.turn == -1 and mouse_clicked:  # 사람
            y_pos, x_pos = pos
            do_action = True

        if do_action:
            update(state, omok_ui, x_pos, y_pos)
            pos = None
            do_action = False

def play_ai_vs_ai(state : OmokState, omok_ui : Omok):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 종료
                pygame.quit()
                sys.exit()

        with ThreadingTimeout(TIMEOUT) as context_manager:
            if state.turn == 1:  # 흑돌 (AI)
                y_pos, x_pos = user_agent.act(copy.deepcopy(state))
            elif state.turn == -1:  # 백돌 (AI)
                y_pos, x_pos = ai_agent.act(copy.deepcopy(state))

        if context_manager.state == context_manager.TIMED_OUT:
            print("Timeout!")
            y_pos, x_pos = random_act(state)

        update(state, omok_ui, x_pos, y_pos)

if __name__ == '__main__':
    pygame.init()
    state = OmokState()
 
    omok_ui = Omok()
    omok_ui.board_draw() # 오목 바둑판 그리기
    omok_ui.title_msg() # 오목 타이틀 그리기
    omok_ui.turn_msg(state.turn) # 오목 턴 메시지 띄우기
    pygame.display.update()

    if HUMAN:
        play_ai_vs_human(state, omok_ui)
    else:
        play_ai_vs_ai(state, omok_ui)
