def is_empty(board):
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] != " ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    front = False
    back = False
    tempYfront = y_end + d_y
    tempXfront = x_end + d_x
    tempYback = y_end - d_y*length
    tempXback = x_end - d_x*length
    if (tempYfront>= 0 and tempYfront<=len(board)-1) and (tempXfront>= 0 and tempXfront<=len(board)-1):
        if board[tempYfront][tempXfront] == " ":
            front = True
    if (tempYback>= 0 and tempYback<=len(board)-1) and (tempXback>= 0 and tempXback<=len(board)-1):
        if board[tempYback][tempXback] == " ":
            back = True
    if back == True and front == True:
        return "OPEN"
    elif back == False and front == False:
        return "CLOSED"
    else:
        return "SEMIOPEN"
    
def is_sequence_complete(board, col, y_start, x_start, length, d_y, d_x):
    for i in range(length):
        if board[y_start+i*d_y][x_start+i*d_x] != col: 
            return False
    return True    
  



def detect_row(board, col, y_start, x_start, length, d_y, d_x):  
    open_seq_count = 0              
    semi_open_seq_count = 0
    rowlength = 0
    y = y_start
    x = x_start
    while (x>=0 and x<=len(board)-1) and (y>=0 and y<=len(board)-1):
        rowlength +=1
        y += d_y
        x += d_x
    for i in range(rowlength):
        if board[y_start][x_start] != col:
            y_start+=d_y
            x_start+=d_x
            continue
        x_end = x_start+d_x*length-1*d_x
        y_end = y_start+d_y*length-1*d_y
        if (y_end>=0 and y_end<=len(board)-1) and (x_end>=0 and x_end<=len(board)-1):
            temp = True
            for j in range(length): 
                if board[y_start+j*d_y][x_start+j*d_x] != col:
                    temp = False
                    break
            if temp == False:
                y_start+=d_y
                x_start+=d_x
                continue
        else:
            y_start+=d_y
            x_start+=d_x
            continue
        if (y_end+d_y)>=0 and (y_end+d_y)<=len(board)-1 and (x_end+d_x)>=0 and (x_end+d_x)<=len(board)-1:
            if board[y_end+d_y][x_end+d_x] == col:
                y_start+=d_y
                x_start+=d_x
                continue
        if (y_start-d_y)>=0 and (y_start-d_y)<=len(board)-1 and (x_start-d_x)>=0 and (x_start-d_x)<=len(board)-1:
            if board[y_start-d_y][x_start-d_x] == col:
                y_start+=d_y
                x_start+=d_x
                continue
        if is_bounded(board, y_end, x_end, length, d_y,d_x) == "OPEN":
            open_seq_count +=1
        elif is_bounded(board, y_end, x_end, length, d_y,d_x) == "SEMIOPEN":
            semi_open_seq_count +=1
        x_start+=d_x
        y_start+=d_y
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    x_start = 0 
    y_start = 0
    for i in range(len(board)):
        open_seq_count+= detect_row(board, col, y_start, x_start, length, 0, 1)[0]
        semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 0, 1)[1]
        open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 1)[0]
        semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 1)[1]
        y_start+=1
    x_start = 0
    y_start = 0
    for i in range(len(board)):
        open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 0)[0]
        semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 0)[1]
        if x_start!=0:
            open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 1)[0]
            semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, 1)[1]
        x_start+=1
    x_start = len(board)-1
    y_start = 0
    for i in range(len(board)):
        open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, -1)[0]
        semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, -1)[1]
        y_start+=1
    x_start = len(board)-2
    y_start = 0
    for i in range(len(board)):
        open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, -1)[0]
        semi_open_seq_count+= detect_row(board, col, y_start, x_start, length, 1, -1)[1]
        x_start-=1
    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    optimal = -21471483648 
    move_y = None
    move_x = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]==" ":
                board[i][j] = "b"
                if score(board)>optimal:
                    optimal = score(board)
                    move_y = i
                    move_x = j
                board[i][j] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    open = 0
    for y in range(len(board)):
        for x in range(len(board[y])): 
            if board[y][x] == " ":
                open+=1 
            for d_y in range(-1,2):
                for d_x in range(-1,2):
                    if d_y == 0 and d_x == 0:
                        continue
                    temp = False
                    if (y+d_y*4)<=len(board)-1 and (y+d_y*4)>=0 and (x+d_x*4)>=0 and (x+d_x*4)<=len(board)-1:
                        if is_sequence_complete(board, "b", y, x, 5, d_y,d_x):
                            temp = False
                            if (y-d_y) >= 0 and (y-d_y)<=len(board)-1 and (x-d_x) >= 0 and (x-d_x)<=len(board)-1:
                                if board[y-d_y][x-d_x] == "b":
                                    temp = True
                            if (y+d_y*5)<=len(board)-1 and (y+d_y*5)>=0 and (x+d_x*5)<=len(board)-1 and (x+d_x*5)>=0:
                                if board[y+d_y*5][x+d_x*5] == "b":
                                    temp = True
                            if not(temp):
                                return "Black won"          
                        if is_sequence_complete(board, "w", y, x, 5, d_y,d_x):
                            temp = False
                            if (y-d_y) >= 0 and (y-d_y)<=len(board)-1 and (x-d_x) >= 0 and (x-d_x)<=len(board)-1:
                                if board[y-d_y][x-d_x] == "w":
                                    temp = True
                            if (y+d_y*5)<=len(board)-1 and (y+d_y*5)>=0 and (x+d_x*5)<=len(board)-1 and (x+d_x*5)>=0:
                                if board[y+d_y*5][x+d_x*5] == "w":
                                    temp = True
                            if not(temp):
                                return "White won"  
    if open!=0:  
        return "Continue playing" 
    return "Draw"

def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x
      
if __name__ == '__main__':
    play_gomoku(8)
