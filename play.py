import chess
import agent1
import numpy as np

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

def Evaluate(board, d, player, player_save, pick_best):
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
        return (player.ExecPosition(BoardState(board), player_save), move)
    
    (w, l) = (1.0, 1.0)
    
    probs = []
    total = 0.0
    
    best_val = -1.0
    if board.turn == chess.BLACK:
        best_val = 2.0
    best_move = None
    
    for mv in board.legal_moves:
        board.push(mv)
        cv = Evaluate(board, d-1, player, player_save, pick_best)[0]
        board.pop()
        
        val = Score(cv)
        if board.turn == chess.WHITE:
            w *= (1.0 - cv[0])
            l *= cv[2]
            
            if val > best_val:
                best_val = val
                best_move = mv
            
            val = val*val*val
            probs.append(val)
            total += val
        else:
            w *= cv[0]
            l *= (1.0 - cv[2])
            
            if val < best_val:
                best_val = val
                best_move = mv
            
            val = 1-val
            val = val*val*val
            probs.append(val)
            total += val
    
    move_prob = np.random.random()
    
    i = 0
    for mv in board.legal_moves:
        probs[i] = probs[i]/total
        
        if move_prob < probs[i]:
            move = mv
            break
        
        move_prob -= probs[i]
        i += 1
    
    if board.turn == chess.WHITE:
        v[0] = 1-w
        v[1] = w-l
        v[2] = l
    else:
        v[0] = w
        v[1] = l-w
        v[2] = 1-l
    
    if pick_best == False:
        return (v, move)
    return (v, best_move)

def PlayMatch(n, player, player1, player2, pick_best):
    board = chess.Board()
    board.set_fen('4k3/8/8/8/8/8/8/R3K2R w - - 0 1')
    
    data = []
    
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            (v, m) = Evaluate(board, 1, player, player1, pick_best)
        else:
            (v, m) = Evaluate(board, 1, player, player2, pick_best)
        data.append((BoardState(board), v))
        #print m
        #print v
        
        board.push(m)
        #print board
        #print "---"
    
    if board.turn == chess.WHITE:
        v = Evaluate(board, 0, player, player1, pick_best)[0]
    else:
        v = Evaluate(board, 0, player, player2, pick_best)[0]
    print v
    data.append((BoardState(board), v))
    
    if n > 0:
        big_match = np.load('match.npy')
        data = np.asarray(data)
        big_match = np.append(big_match, data, axis = 0)
        print big_match.shape
        np.save('match', big_match)
        return big_match.shape[0], Score(v)
    elif n==0:
        data = np.asarray(data)
        print data.shape
        np.save('match', data)
        return data.shape[0], Score(v)
    else:
        return Score(v)
