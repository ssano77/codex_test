# Simple Reversi (Othello) game with Pygame
# Human plays black, AI plays white. Click on the board to make a move.
import pygame
import sys
from typing import List, Tuple, Optional

# Board constants
SIZE = 8  # 8x8 board
CELL_SIZE = 60
BORDER = 20
WINDOW_SIZE = SIZE * CELL_SIZE + BORDER * 2

BLACK = 1
WHITE = -1
EMPTY = 0

pygame.init()
FONT = pygame.font.SysFont(None, 24)


def init_board() -> List[List[int]]:
    board = [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]
    mid = SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board


def inside(x: int, y: int) -> bool:
    return 0 <= x < SIZE and 0 <= y < SIZE


def opponent(player: int) -> int:
    return -player


def valid_moves(board: List[List[int]], player: int) -> List[Tuple[int, int, List[Tuple[int, int]]]]:
    moves = []
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y][x] != EMPTY:
                continue
            captured: List[Tuple[int, int]] = []
            for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                nx, ny = x + dx, y + dy
                path: List[Tuple[int, int]] = []
                while inside(nx, ny) and board[ny][nx] == opponent(player):
                    path.append((nx, ny))
                    nx += dx
                    ny += dy
                if path and inside(nx, ny) and board[ny][nx] == player:
                    captured.extend(path)
            if captured:
                moves.append((x, y, captured))
    return moves


def apply_move(board: List[List[int]], x: int, y: int, player: int, captured: List[Tuple[int, int]]):
    board[y][x] = player
    for cx, cy in captured:
        board[cy][cx] = player


def draw_board(screen, board: List[List[int]], current_player: int, message: Optional[str] = None):
    screen.fill((0, 128, 0))
    for i in range(SIZE + 1):
        pygame.draw.line(screen, (0, 0, 0), (BORDER, BORDER + i * CELL_SIZE), (BORDER + SIZE * CELL_SIZE, BORDER + i * CELL_SIZE))
        pygame.draw.line(screen, (0, 0, 0), (BORDER + i * CELL_SIZE, BORDER), (BORDER + i * CELL_SIZE, BORDER + SIZE * CELL_SIZE))
    for y in range(SIZE):
        for x in range(SIZE):
            if board[y][x] != EMPTY:
                color = (0, 0, 0) if board[y][x] == BLACK else (255, 255, 255)
                pygame.draw.circle(screen, color, (BORDER + x * CELL_SIZE + CELL_SIZE // 2, BORDER + y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 4)
    if message:
        txt = FONT.render(message, True, (255, 0, 0))
        screen.blit(txt, (BORDER, WINDOW_SIZE - BORDER // 2))
    turn_text = 'Black (You)' if current_player == BLACK else 'White (AI)'
    info = FONT.render(f"Turn: {turn_text}", True, (255, 255, 255))
    screen.blit(info, (BORDER, 5))
    pygame.display.flip()


def ai_move(board: List[List[int]], player: int) -> Tuple[int, int, List[Tuple[int, int]]]:
    moves = valid_moves(board, player)
    # simple heuristic: choose move that captures most pieces
    best_move = max(moves, key=lambda m: len(m[2]))
    return best_move


def game_loop():
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 40))
    pygame.display.set_caption('Reversi')
    board = init_board()
    player = BLACK

    running = True
    while running:
        draw_board(screen, board, player)
        moves = valid_moves(board, player)
        if not moves:
            player = opponent(player)
            moves = valid_moves(board, player)
            if not moves:
                black_count = sum(row.count(BLACK) for row in board)
                white_count = sum(row.count(WHITE) for row in board)
                if black_count > white_count:
                    message = 'Black wins!'
                elif white_count > black_count:
                    message = 'White wins!'
                else:
                    message = 'Draw!'
                draw_board(screen, board, player, message)
                pygame.time.wait(3000)
                break
        if player == BLACK:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    x = (mx - BORDER) // CELL_SIZE
                    y = (my - BORDER) // CELL_SIZE
                    for mv in moves:
                        if mv[0] == x and mv[1] == y:
                            apply_move(board, mv[0], mv[1], player, mv[2])
                            player = opponent(player)
                            break
        else:
            # AI turn
            if moves:
                x, y, captured = ai_move(board, player)
                pygame.time.wait(500)
                apply_move(board, x, y, player, captured)
            player = opponent(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    game_loop()
