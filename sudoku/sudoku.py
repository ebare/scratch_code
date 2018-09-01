from termcolor import cprint

def solve(board):
    print_board(board)
    made_progress = True
    while made_progress and not is_complete(board):
        made_progress = False
        # check for rows with 1 digit missing
        for idx,row in enumerate(board):
            missing = _get_missing(row)
            if len(missing) == 1:
                r_idx = row.index(0)
                row[r_idx] = missing.pop()
                made_progress = True
                print_board(board, (idx, r_idx))

        # check for cols with 1 digit missing
        for idx, col in enumerate(zip(*board)):
            missing = _get_missing(col)
            if len(missing) == 1:
                r_idx = col.index(0)
                board[r_idx][idx] = missing.pop()
                made_progress = True
                print_board(board, (r_idx, idx))

        # check for boxes with 1 digit missing

        # check for spaces with only 1 possibility
        boards = []
        for i in range(9):
            poss = get_possible(board, i+1)
            boards.append(poss)
        boards.append(board)
        for i in range(9):
            for j in range(9):
                nums = [b[i][j] for b in boards]
                nums = [n for n in filter(lambda x: x!=0, nums)]
                if len(nums) == 1:
                    if board[i][j] == 0:
                        board[i][j] = nums[0]
                        made_progress = True
                        print_board(board, (i,j))

        # check for sets with digit only possible in 1 place
        for n, poss in enumerate(boards):
            cur_digit = n+1
            # check for rows with digit only possible in 1 place
            for idx, row in enumerate(poss):
                if row.count(cur_digit) == 1:
                    board[idx][row.index(cur_digit)] = cur_digit
                    made_progress = True
                    print_board(board, (idx, row.index(cur_digit))) 

            # check for cols with digit only possible in 1 place
            for idx, col in enumerate(zip(*poss)):
                if col.count(cur_digit) == 1:
                    r_idx = col.index(cur_digit)
                    if board[r_idx][idx] == 0:
                        board[r_idx][idx] = cur_digit
                        made_progress = True
                        print_board(board, (r_idx, idx)) 

            # check for boxes with digit only possible in 1 place
            for idx, box in enumerate(_get_boxes(poss)):
                if box.count(cur_digit) == 1:
                    row_idx, col_idx = _rc_from_box(idx, box.index(cur_digit))
                    if board[row_idx][col_idx] == 0:
                        board[row_idx][col_idx] = cur_digit
                        made_progress = True
                        print_board(board, (row_idx, col_idx)) 

    return board


def _get_missing(l):
    return set([i+1 for i in range(9)]).difference(set([n for n in l if n != 0]))

def get_possible(board, n):
    possible = [[0 for i in range(9)] for i in range(9)]

    rows = board
    cols = [list(col) for col in zip(*board)]

    boxes = _get_boxes(board)

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                cur_box = boxes[int(i/3) * 3 + int(j/3)]
                if n not in rows[i] + cols[j] + cur_box:
                    possible[i][j] = n
    return possible

def _get_boxes(board):
    '''return boxes:
        0|1|2
        3|4|5
        6|7|8
    '''
    boxes = []
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            box = board[i][j:j+3] + board[i+1][j:j+3] + board[i+2][j:j+3]
            boxes.append(box)
    return boxes

def _rc_from_box(box_num, pos):
    '''return row,col given pos in box
    '''
    r = int(box_num/3) * 3 + int(pos/3)
    c = (pos % 3) + (box_num % 3) * 3

    return r,c

def is_complete(board):
    for row in board:
        if 0 in row:
            return False
    return True

def is_won(board): #board[i][j]
  ok = True
  # check rows
  for row in board:
    if 0 not in row and len(set(row)) != 9:
      ok = False
      break
  # check cols
  if ok:
    for col in zip(*board):
        if len(set(col)) != 9:
            ok = False
            break
  # check boxes
  if ok:
      for i in range(0, 9, 3):
          for j in range(0, 9, 3):
            box = board[i][j:j+3] + board[i+1][j:j+3] + board[i+2][j:j+3]
            if len(set(box)) != 9:
                ok = False
                break
  
  return ok

def print_board(board, highlight=None):
    if highlight is None:
        highlight = (-1,-1)
    for i, row in enumerate(board):
        if i % 3 == 0:
            print('-' * 17)
        if i == highlight[0]:
            for j,d in enumerate([d if d!=0 else ' ' for d in row]):
                end_ch = '|' if j in [2,5] else ' '
                if j == highlight[1]:
                    cprint(str(d), 'green', attrs=['bold'], end=end_ch)
                else:
                    cprint(str(d), end=end_ch)
            cprint('')
        else:
            print('{} {} {}|{} {} {}|{} {} {}'.format(*[d if d!=0 else ' ' for d in row]))
    print('-' * 17)