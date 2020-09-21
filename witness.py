import chess
import chess.svg
import agent1
import numpy as np

player = agent1.agent1()
player.BuildNetwork()

def BoardState(board):
    state = np.zeros([840])
    
    for i in range(64):
        state[i*13] = 1.0
    
    for x, y in board.piece_map().items():
        loc = x*13
        state[x*13] = 0.0
        
        if y.symbol() == 'P':
            loc += 1
        elif y.symbol() == 'R':
            loc += 2
        elif y.symbol() == 'N':
            loc += 3
        elif y.symbol() == 'B':
            loc += 4
        elif y.symbol() == 'Q':
            loc += 5
        elif y.symbol() == 'K':
            loc += 6
        elif y.symbol() == 'p':
            loc += 7
        elif y.symbol() == 'r':
            loc += 8
        elif y.symbol() == 'n':
            loc += 9
        elif y.symbol() == 'b':
            loc += 10
        elif y.symbol() == 'q':
            loc += 11
        else:
            loc += 12
        
        state[loc] = 1.0
    
    offset = 64*13
    if board.turn == chess.WHITE:
        state[offset] = 1.0
    else:
        state[offset+1] = 1.0
    
    if board.has_kingside_castling_rights(chess.WHITE):
        state[offset+2] = 1.0
    if board.has_queenside_castling_rights(chess.WHITE):
        state[offset+3] = 1.0
    if board.has_kingside_castling_rights(chess.BLACK):
        state[offset+4] = 1.0
    if board.has_queenside_castling_rights(chess.BLACK):
        state[offset+5] = 1.0
    if board.can_claim_threefold_repetition():
        state[offset+6] = 0.5
    if board.is_fivefold_repetition():
        state[offset+6] = 1.0
    state[offset+7] = board.halfmove_clock/150.0
    
    return state

def Score(v):
    return v[0]+(0.5*v[1])

def Evaluate(board, d):
    v = np.zeros([3])
    move = None
    
    if board.is_game_over():
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                v[0], v[2] = 0.0, 1.0
            else:
                v[0], v[2] = 1.0, 0.0
        else:
            v[1] = 1.0 
        return (v, move)
    
    if d == 0:
        return (player.ExecPosition(BoardState(board)), move)
    
    (w, l) = (1.0, 1.0)
    
    best_val = -1.0
    if board.turn == chess.BLACK:
        best_val = 2.0
    
    for mv in board.legal_moves:
        board.push(mv)
        cv = Evaluate(board, d-1)[0]
        board.pop()
        
        #print cv, Score(cv), best_val
        
        val = Score(cv)
        if board.turn == chess.WHITE:
            w *= (1.0 - cv[0])
            l *= cv[2]
            
            if val > best_val:
                best_val = val
                move = mv
        else:
            w *= cv[0]
            l *= (1.0 - cv[2])
            
            if val < best_val:
                best_val = val
                move = mv
    
    if board.turn == chess.WHITE:
        v[0] = 1-w
        v[1] = w-l
        v[2] = l
    else:
        v[0] = w
        v[1] = l-w
        v[2] = 1-l
    
    return (v, move)



def PlayMatch():
    board = chess.Board()
    
    data = []
    
    while not board.is_game_over():
        (v, m) = Evaluate(board, 1)
        data.append((BoardState(board), v))
        print m
        print v
        
        board.push(m)
        print board
        print "---"
    
    v = Evaluate(board, 0)[0]
    print v
    data.append((BoardState(board), v))

PlayMatch()
