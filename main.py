from flask import Flask, render_template, request, redirect, url_for
import copy

app = Flask(__name__)

# Initial board setup
board = [
    [8, 0, 0, 4, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 1, 0, 0, 0, 0, 6, 5, 0],
    [5, 0, 9, 0, 3, 0, 7, 8, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 4, 8, 0, 2, 0, 1, 0, 3],
    [0, 5, 2, 0, 0, 0, 0, 9, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 9, 0, 2, 0, 0, 5]
]

# Helper functions
def findEmpty(bo):
    for r in range(9):
        for c in range(9):
            if bo[r][c] == 0:
                return r, c
    return False

def checkValid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True

def solve(bo):
    find = findEmpty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if checkValid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return bo
            bo[row][col] = 0
    return False

def displayErrors(bo, solvedBo):
    errors = []
    for r in range(9):
        for c in range(9):
            if bo[r][c] != solvedBo[r][c] and bo[r][c] != 0:
                errors.append((r, c))
    return errors

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'check':
            solved_board = copy.deepcopy(board)
            solve(solved_board)
            errors = displayErrors(board, solved_board)
            return render_template('index.html', board=board, errors=errors)
        elif action == 'solve':
            solved_board = copy.deepcopy(board)
            solve(solved_board)
            return render_template('index.html', board=solved_board, errors=[])
        else:
            for r in range(9):
                for c in range(9):
                    cell_value = request.form.get(f'cell-{r}-{c}')
                    board[r][c] = int(cell_value) if cell_value.isdigit() else 0
            return redirect(url_for('index'))
    return render_template('index.html', board=board, errors=[])

if __name__ == '__main__':
    app.run(debug=True)