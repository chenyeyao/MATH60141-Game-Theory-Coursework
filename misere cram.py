from functools import lru_cache

N = 4
M = 4

DIRS = [(0, 1), (1, 0)]

def make_empty_board():
    return tuple([tuple([0]*M) for _ in range(N)])

def place_domino(board, r1, c1, r2, c2):
    b = [list(row) for row in board]
    b[r1][c1] = 1
    b[r2][c2] = 1
    return tuple(tuple(row) for row in b)

def generate_moves(board):
    moves = []
    for r in range(N):
        for c in range(M):
            if board[r][c] == 0:
                for dr, dc in DIRS:
                    r2 = r + dr
                    c2 = c + dc
                    if 0 <= r2 < N and 0 <= c2 < M and board[r2][c2] == 0:
                        moves.append((r, c, r2, c2))
    return moves

def board_symmetries(board):
    b = board

    syms = set()

    def rot90(bd):
        return tuple(zip(*bd[::-1]))

    def flip_h(bd):
        return tuple(row[::-1] for row in bd)

    cur = b
    for _ in range(4):
        syms.add(cur)
        syms.add(flip_h(cur))
        cur = rot90(cur)

    return syms

def canonical(board):
    return min(board_symmetries(board))

@lru_cache(None)
def misere_cram_win(board):

    board = canonical(board)

    moves = generate_moves(board)

    if not moves:
        return True

    for r1, c1, r2, c2 in moves:
        new_board = place_domino(board, r1, c1, r2, c2)
        if not misere_cram_win(new_board):  
            return True

    return False


init_board = make_empty_board()
result = misere_cram_win(init_board)