import pygame
import numpy as np
import sys


class OmokState:
    def __init__(self, game_board=None, board_size=19, win_stones=5):
        self.game_board = game_board if game_board is not None else np.zeros([board_size, board_size])
        self.board_size = board_size
        self.win_stones = win_stones
        self.num_stones = 0
        self.history = []
        self.turn = 1  # black turn: 1, white turn: -1

    def reset(self):
        self.game_board = np.zeros([self.board_size, self.board_size])
        self.num_stones = 0
        self.history = []
        self.turn = 1

    def check_status(self):
        if self.num_stones == self.board_size * self.board_size:
            return 3

        # 수평선 상에서 5개가 연속인 경우
        for row in range(self.board_size):
            for col in range(self.board_size - self.win_stones + 1):
                # 흑 승!
                if np.sum(self.game_board[row, col:col + self.win_stones]) == self.win_stones:
                    return 1
                # 백 승!
                if np.sum(self.game_board[row, col:col + self.win_stones]) == -self.win_stones:
                    return 2

        # 수직선 상에서 5개가 연속인 경우
        for row in range(self.board_size - self.win_stones + 1):
            for col in range(self.board_size):
                # 흑 승!
                if np.sum(self.game_board[row: row + self.win_stones, col]) == self.win_stones:
                    return 1
                # 백 승!
                if np.sum(self.game_board[row: row + self.win_stones, col]) == -self.win_stones:
                    return 2

        # 대각선 상에서 5개가 연속인 경우
        for row in range(self.board_size - self.win_stones + 1):
            for col in range(self.board_size - self.win_stones + 1):
                count_sum = 0
                for i in range(self.win_stones):
                    if self.game_board[row + i, col + i] == 1:
                        count_sum += 1
                    if self.game_board[row + i, col + i] == -1:
                        count_sum -= 1

                # 흑 승!
                if count_sum == self.win_stones:
                    return 1

                # 백 승!
                if count_sum == -self.win_stones:
                    return 2

        for row in range(self.win_stones - 1, self.board_size):
            for col in range(self.board_size - self.win_stones + 1):
                count_sum = 0
                for i in range(self.win_stones):
                    if self.game_board[row - i, col + i] == 1:
                        count_sum += 1
                    if self.game_board[row - i, col + i] == -1:
                        count_sum -= 1

                # 흑 승!
                if count_sum == self.win_stones:
                    return 1

                # 백 승!
                if count_sum == -self.win_stones:
                    return 2

    def is_valid_position(self, x_pos, y_pos):
        if x_pos == -1 or y_pos == -1:
            return False

        if self.game_board[y_pos, x_pos] == 1 or self.game_board[y_pos, x_pos] == -1:
            return False

        return True

    def update(self, x_pos, y_pos):
        self.game_board[y_pos, x_pos] = 1 if self.turn == 1 else -1
        self.history.append((x_pos, y_pos))
        self.turn *= -1  # reverse
        self.num_stones += 1


class Omok:
    def __init__(self, board_size=19):
        # self.screen_width, self.screen_height = 640, 780  # 게임화면 너비, 높이 설정
        self.screen_width, self.screen_height = 840, 980  # 게임화면 너비, 높이 설정

        self.side_margin = 20  # 옆 여백
        self.top_margin = 140  # 위 여백
        self.board_margin = 40  # 판 여백

        # 게임 화면 설정
        self.game_screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.board_size = board_size
        self.board_color = (220, 179, 92)
        # 판 사이즈
        self.grid_size = self.screen_width - 2 * (self.board_margin + self.side_margin)

        # 초기 X, Y 칸 사이즈 설정
        self.X_coord = [self.side_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))
                        for i in range(self.board_size)]
        self.Y_coord = [self.top_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))
                        for i in range(self.board_size)]

        # 색 모음 (R, G, B)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def update(self, state):
        game_board = state.game_board
        # 바둑돌 표시
        for i in range(game_board.shape[0]):
            for j in range(game_board.shape[1]):
                if game_board[i, j] == 1:
                    pygame.draw.circle(self.game_screen, self.black, (self.X_coord[j], self.Y_coord[i]), 15, 0)

                if game_board[i, j] == -1:
                    pygame.draw.circle(self.game_screen, self.white, (self.X_coord[j], self.Y_coord[i]), 15, 0)

        self.turn_msg(state.turn)

    def board_draw(self):
        # 바둑판 그리기
        pygame.draw.rect(
            self.game_screen,
            self.board_color,
            pygame.Rect(self.side_margin, self.top_margin, self.screen_width - 2 * self.side_margin,
                        self.screen_width - 2 * self.side_margin)
        )

        # 수직선
        for i in range(self.board_size):
            pygame.draw.line(self.game_screen, self.black, (self.side_margin + self.board_margin,
                                                            self.top_margin + self.board_margin + i * int(
                                                                self.grid_size / (self.board_size - 1))), (
                                 self.screen_width - (self.side_margin + self.board_margin),
                                 self.top_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1))),
                             1)

        # 수평선
        for i in range(self.board_size):
            pygame.draw.line(self.game_screen, self.black, (
                self.side_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1)),
                self.top_margin + self.board_margin), (
                                 self.side_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1)),
                                 self.top_margin + self.board_margin + self.grid_size), 1)

        # 가운데 점
        for i in range(self.board_size):
            for j in range(self.board_size):
                if i in [3, 9, 15] and j in [3, 9, 15]:
                    pygame.draw.circle(self.game_screen, self.black, (
                        self.side_margin + self.board_margin + i * int(self.grid_size / (self.board_size - 1)),
                        self.top_margin + self.board_margin + j * int(self.grid_size / (self.board_size - 1))), 5, 0)

    def is_valid_click(self, state, pos):
        x_pos, y_pos = -1, -1
        for i, x in enumerate(self.X_coord):
            if x - 20 < pos[0] < x + 20:
                x_pos = i

        for i, y in enumerate(self.Y_coord):
            if y - 20 < pos[1] < y + 20:
                y_pos = i

        valid_pos = state.is_valid_position(x_pos, y_pos)
        return valid_pos, (y_pos, x_pos)

    def title_msg(self):
        font = pygame.font.Font('freesansbold.ttf', 20)  # 글꼴
        title_surf = font.render('Omok', True, self.white)
        title_rect = title_surf.get_rect()
        title_rect.topleft = (30, 10)
        self.game_screen.blit(title_surf, title_rect)

    def turn_msg(self, turn):
        font = pygame.font.Font('freesansbold.ttf', 20)  # 글꼴
        # 검은돌 차례
        turn_surf = font.render("Black's Turn!" if turn == 1 else "White's Turn!", True, self.white)
        turn_rect = turn_surf.get_rect()
        position = (30, 110) if turn == 1 else (self.screen_width - 175, 110)
        pygame.draw.rect(
            self.game_screen,
            self.black,
            pygame.Rect(position[0], position[1], 150, 30)
        )
        turn_rect.topleft = (self.screen_width - 175, 110) if turn == 1 else (30, 110)
        self.game_screen.blit(turn_surf, turn_rect)


    # # 흑돌 남은 시간 표시
    # def time_msg(self, wait_time):
    #     font = pygame.font.SysFont('malgungothic', 20)  # 글꼴 지정
    #     titleSurf = font.render(f"흑돌은 {wait_time}초 후에 자동으로 둡니다", True, self.white)
    #     titleRect = titleSurf.get_rect()
    #     titleRect.topleft = (30, 50)
    #     self.game_screen.blit(titleSurf, titleRect)

    def display_result(self, status):
        font_title = pygame.font.SysFont('malgungothic', 54)
        font_clicktext = pygame.font.SysFont('malgungothic', 20)

        # Black Win
        if status == 1:
            self.game_screen.fill(self.white)
            win_surf = font_title.render("Black Win!", True, self.black)
            clk_surf = font_clicktext.render("Click anywhere to restart!", True, self.black)
        elif status == 2:
            self.game_screen.fill(self.black)
            win_surf = font_title.render("White Win!", True, self.white)
            clk_surf = font_clicktext.render("Click anywhere to restart!", True, self.white)
        elif status == 3:
            self.game_screen.fill(self.white)
            win_surf = font_title.render("DRAW!", True, self.black)
            clk_surf = font_clicktext.render("Click anywhere to restart!", True, self.black)
        else:
            return

        win_rect = win_surf.get_rect()
        win_rect.midtop = (self.screen_width / 2, self.screen_height / 2 - 70)
        self.game_screen.blit(win_surf, win_rect)

        clk_rect = clk_surf.get_rect()
        clk_rect.midtop = (self.screen_width / 2, self.screen_height / 2)
        self.game_screen.blit(clk_surf, clk_rect)
        pygame.display.update()

        # 클릭 이벤트 처리
        mouse_clicked = False
        while not mouse_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # 종료
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_clicked = True # 클릭하였으면 True로 표시하고 반복문 종료

        return mouse_clicked # 클릭하였다는 True 값을 반환
