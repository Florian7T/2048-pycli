import os,random,math

BG_COLOR = (1,37,40)
BORDER_COLOR = (1,30,41)

def clrscr():
    if os.name == "nt": os.system("cls")
    else: os.system("clear")

def getColor(_font = 1, _front = 37, _back = 40) -> str: return f'\x1b[{_font};{_front};{_back}m'
resetColor = '\x1b[0m'
def colorStr(msg:str,_font = 1, _front = 37, _back = 40) -> str:
    return f'{getColor(_font,_front,_back)}{msg}{resetColor}'
def numStr(n:int) -> str:
    if n == 0: return "0".rjust(4)
    pwr = int(math.log(n,2))
    rjust = str(n).rjust(4)
    if pwr <= 2: return colorStr(rjust)
    if pwr <= 4: return colorStr(rjust,_front=33)
    if pwr <= 6: return colorStr(rjust,_front=31)
    if pwr <= 8: return colorStr(rjust,_back=41)
    if pwr == 9: return colorStr(rjust, _front=33,_back=41)
    if pwr == 10: return colorStr(rjust, _front=32,_back = 42)
    return colorStr(rjust,_back=42)

TITLE = "2048"

FRAME = ""
MATRIX = []

def blankMatrix(size_x:int, size_y:int) -> list:
    MATRIX_BLANK = []
    for i in range(size_y):
        row = []
        for x in range(size_x): row.append(0)
        MATRIX_BLANK.append(row)
    return [[0 for i in range(size_x)] for j in range(size_y)]

def createLine(firstch:str,fillch:str,midch:str,lastch:str,size_x:int):
    line = firstch
    for i in range(size_x): line += fillch*8 + midch
    line = line[:len(line)-1] + lastch + '\n'
    return line

def createNumLine(line:str, row:int, size_x:int):
    for i in range(size_x):
        line = line[:9*i+3] + f"{i+1}{i+1}{row+1}{row+1}" + line[9*i+7:]
    return line

def promptSize():
    global FRAME
    size_x = 0
    size_y = 0
    while True:
        try:
            size_x = int(input("Width of the game (2-20): "))
            size_y = int(input("Height of the game (2-20): "))
            if 1 < size_y < 21 and 1 < size_x < 21: break
            print("Given size of the game was either to big or too small!")
        except ValueError:
            print(colorStr("No valid number was given!",1,37,41))
    tot_x = 9*size_x + 1
    tot_y = 4*size_y - 1
    FRAME = " "*int(tot_x/2 - len(TITLE)/2) + TITLE +" "*int(tot_x/2 - len(TITLE)/2) + "\n"
    top_line = createLine('╔','═','╦','╗',size_x)
    fil_line = createLine('║',' ','║','║',size_x)
    mid_line = createLine('╠','═','╬','╣',size_x)
    bot_line = createLine('╠','═','╩','╝',size_x)
    FRAME += top_line
    for i in range(tot_y):
        if (i - 3) % 4 == 0: FRAME += mid_line
        elif (i - 1) % 4 == 0: FRAME += createNumLine(fil_line,int((i-1)/4),size_x)
        else: FRAME += fil_line
    FRAME += bot_line[:len(bot_line)-1]
    return size_x, size_y

def addRandomNum() -> bool:
    tries = 0
    while tries < 16:
        _x = random.randint(0,cols-1)
        _y = random.randint(0,rows-1)
        if MATRIX[_y][_x] == 0:
            if random.randint(0,10) <= 2: MATRIX[_y][_x] = 4
            else: MATRIX[_y][_x] = 2
            return True
        tries += 1
    return False

def print_frame():
    clrscr()
    tmp_tr = FRAME
    for _y in range(rows):
        for _x in range(cols):
            tmp_tr = tmp_tr.replace(f"{_x+1}{_x+1}{_y+1}{_y+1}",numStr(MATRIX[_y][_x]))
    print(tmp_tr)

def moveUp():
    moved = True
    while moved:
        moved = False
        for row in range(rows):
            for x in range(cols):
                if row != 0 and MATRIX[row][x] != 0:
                    if MATRIX[row-1][x] == 0:
                        MATRIX[row-1][x] = MATRIX[row][x]
                        MATRIX[row][x] = 0
                        moved = True
                    elif MATRIX[row-1][x] == MATRIX[row][x]:
                        MATRIX[row - 1][x] *= 2
                        MATRIX[row][x] = 0
                        moved = True

def moveDown():
    moved = True
    while moved:
        moved = False
        for row in reversed(range(rows)):
            for x in range(cols):
                if row != (rows - 1) and MATRIX[row][x] != 0:
                    if MATRIX[row + 1][x] == 0:
                        MATRIX[row + 1][x] = MATRIX[row][x]
                        MATRIX[row][x] = 0
                        moved = True
                    elif MATRIX[row + 1][x] == MATRIX[row][x]:
                        MATRIX[row + 1][x] *= 2
                        MATRIX[row][x] = 0
                        moved = True

def moveRight():
    moved = True
    while moved:
        moved = False
        for col in range(cols):
            for y in range(rows):
                if col != 0 and MATRIX[y][col] != 0:
                    if MATRIX[y][col - 1] == 0:
                        MATRIX[y][col - 1] = MATRIX[y][col]
                        MATRIX[y][col] = 0
                        moved = True
                    elif MATRIX[y][col - 1] == MATRIX[y][col]:
                        MATRIX[y][col - 1] *= 2
                        MATRIX[y][col] = 0
                        moved = True

def moveLeft():
    moved = True
    while moved:
        moved = False
        for col in reversed(range(cols)):
            for y in range(rows):
                if col != (cols - 1) and MATRIX[y][col] != 0:
                    if MATRIX[y][col + 1] == 0:
                        MATRIX[y][col + 1] = MATRIX[y][col]
                        MATRIX[y][col] = 0
                        moved = True
                    elif MATRIX[y][col + 1] == MATRIX[y][col]:
                        MATRIX[y][col + 1] *= 2
                        MATRIX[y][col] = 0
                        moved = True

def handleMove() -> bool:
    inp = input("║\n╠═[W] up\n"
                "╠═[A] left\n"
                "╠═[S] down\n"
                "╠═[D] right\n"
                "║\n╚═ ")
    ch = inp.lower()
    if ch == 'w': moveUp()
    elif ch == 'a': moveRight()
    elif ch == 's': moveDown()
    elif ch == 'd': moveLeft()
    else: return False
    return True

def checkLost() -> bool:
    for y in range(rows):
        for x in range(cols):
            if y - 1 > 0 and MATRIX[y][x] == MATRIX[y - 1][x]: return False
            if y + 1 < rows and MATRIX[y][x] == MATRIX[y + 1][x]: return False
            if x - 1 > 0 and MATRIX[y][x] == MATRIX[y][x - 1]: return False
            if x + 1 < cols and MATRIX[y][x] == MATRIX[y][x + 1]: return False
    return True

if __name__ == "__main__":
    while True:
        frame_x, frame_y = promptSize()
        MATRIX = blankMatrix(frame_x,frame_y)
        rows = len(MATRIX)
        cols = len(MATRIX[0])
        addRandomNum()

        while True:
            print_frame()
            if handleMove() and not addRandomNum() and checkLost():
                print(colorStr("No move left to play you lost!",_front=30,_back=41))
                break


