
import copy
import random


class Board:
    
    def __resetBoard(self): #we use this to empty out the board
        self.board= [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]

        return self.board


    def __init__(self, code=None):
        self.__resetBoard()
        
        if code:
            self.code = code

            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(code[0])
                    code = code[1:]
        else:
            self.code = None


    # def boardToCode(self, input_board=None): # turn a pre-existing board into a code
    #     if input_board:
    #         _code = ''.join([str(i) for j in input_board for i in j])
    #         return _code
    #     else:
    #         self.code = ''.join([str(i) for j in self.board for i in j])
    #         return self.code
    
    def boardToCode(self, input_board=None): # turn a pre-existing board into a code
        if input_board:
            _code = ""
            for j in input_board:
                for i in j:
                    _code = _code + str(i)
            return _code
        else:
            self.code = ""
            for j in self.board:
                for i in j:
                    self.code = self.code + str(i)
            return self.code


    def findSpaces(self): # finds the first empty space in the board, which is represented by a 0
        for row in range(len(self.board)):  #go trough thr rows
            for col in range(len(self.board[0])):  #go trough the columns
                if self.board[row][col] == 0:  
                    return (row, col)   #if the function finds a 0 return the index

        return False   #if there are no empty spaces we return false


    def checkSpace(self, num, space): #checks to see if we can place number a specifc space in a row and col
    #num is the number we are trying to enter and space contains the index of the place we are checking
        if not self.board[space[0]][space[1]] == 0: # check to see if space is a number already
            return False

        for col in self.board[space[0]]: # check to see if number is already in row
            if col == num:
                return False

        for row in range(len(self.board)): # check to see if number is already in column
            if self.board[row][space[1]] == num:
                return False

        _internalBoxRow = space[0] // 3
        _internalBoxCol = space[1] // 3

        for i in range(3): # check to see if internal box already has number
            for j in range(3):
                if self.board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
                    return False
    
        return True        

    def solve(self):   #solve the board using recursion
        _spacesAvailable = self.findSpaces()

        if not _spacesAvailable:
            return True    #it did not find a free space so the board is solved
    
        else:
            row, col = _spacesAvailable  #get the column and row index from spacesavailable function
    
        for n in range(1,10):  #try the numbers from 1 to 9 to see if they work
            if self.checkSpace(n,(row,col)):  #check if the number works
                self.board[row][col] = n  #placee the n into free place

                if self.solve():
                    return self.board
            
                self.board[row][col] = 0


        return False

    def solveForCode(self): # solves a board and returns the code of the solved board
        return self.boardToCode(self.solve())

    def __generateCont(self): # uses recursion to finish generating a random board
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] == 0:
                        _num = random.randint(1, 9)

                        if self.checkSpace(_num, (row, col)):
                            self.board[row][col] = _num

                            if self.solve():
                                self.__generateCont()
                                return self.board

                            self.board[row][col] = 0

            return False

    def __generateRandomCompleteBoard(self): # generates a brand new completely random board full of numbers
        self.__resetBoard()  #we first clear out the board

        _l = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)       #this lets us fill the 3 diagonal 3x3 boxes with random numbers


        

            return self.__generateCont()

#we want to make sure that the board only has one solution like normal sudoku


    def __solveToFindNumberOfSolutions(self, row, col): # solves the board using recursion, is used in the findNumberOfSolutions method
            for n in range(1, 10):
                if self.checkSpace(n, (row, col)):
                    self.board[row][col] = n

                    if self.solve():
                        return self.board

                    self.board[row][col] = 0

            return False


    def __findSpacesToFindNumberOfSolutions(self, board, h): # finds the first empty space it comes across, is used within the findNumberOfSolutions method
        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == h:
                        return (row, col)

                    _k += 1 #we increment k to count how many empty spaces we have

        return False



    def findNumberOfSolutions(self): # finds the number of solutions to a board and returns the list of solutions
            _z = 0
            _list_of_solutions = []

            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] == 0:
                        _z += 1   #we increment z until it is equal to the empty spaces

            for i in range(1, _z+1):
                _board_copy = copy.deepcopy(self)  #we make a deep copy of the board so we can change it without changing the main board

                _row, _col = self.__findSpacesToFindNumberOfSolutions(_board_copy.board, i)
                _board_copy_solution = _board_copy.__solveToFindNumberOfSolutions(_row, _col)

                _list_of_solutions.append(self.boardToCode(input_board=_board_copy_solution))

            return list(set(_list_of_solutions))


#now we can make the board with the missing spaces as well as the solved board

    def generateQuestionBoard(self, fullBoard, difficulty): # generates a question board with a certain number of cells removed depending on the chosen difficulty
        self.board = copy.deepcopy(fullBoard)
        
        if difficulty == 0:
            _squares_to_remove = 36
        elif difficulty == 1:
            _squares_to_remove = 46
        elif difficulty == 2:
            _squares_to_remove = 52
        else:
            return    #the difficulty decides how many spaces to leave empty

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(0, 2)
            _rCol = random.randint(0, 2)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(3, 5)
            _rCol = random.randint(3, 5)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(6, 8)
            _rCol = random.randint(6, 8)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _squares_to_remove -= 12  #we decrement the squares we need to remove by 12 
        _counter = 0
        while _counter < _squares_to_remove:
            _row = random.randint(0, 8)
            _col = random.randint(0, 8)

            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0

                if len(self.findNumberOfSolutions()) != 1:
                    self.board[_row][_col] = n
                    continue

                _counter += 1

        return self.board, fullBoard

#now we need a function that will do all of this while only needing the difficulty

    def generateQuestionBoardCode(self, difficulty): # generates a new random board and its board code depending on the difficulty
        self.board, _solution_board = self.generateQuestionBoard(self.__generateRandomCompleteBoard(), difficulty)
        return self.boardToCode(), self.boardToCode(_solution_board)

if __name__ == '__main__':
	board = Board()

	question_board_code = board.generateQuestionBoardCode(0) # generates a puzzle depending on the number entered 0= easy ,1=mid ,2=hard
	#print(question_board_code[0])  #print the problem board code
    

#	code = '300105000060200000008090060050000800800007040071009035000900084704006000902048300'
#	solved_board_code = Board(code).solveForCode() # solves a hard level sudoku 
#print(solved_board_code)

solvedSud= Board(question_board_code[0]).solveForCode()  #solve the board we just got
#print(solvedSud)

def print_sudoku_layout(number_string):
    
   # Takes a string of 81 numbers and prints it in a Sudoku-like 9x9 grid layout.
    #Empty cells can be represented by '0' or '.'.
    
    if len(number_string) != 81:
        print("Error: The input string must contain exactly 81 numbers.")
        return

    grid = []
    for i in range(9):
        row = [char for char in number_string[i * 9 : (i + 1) * 9]]
        grid.append(row)

    for r_idx, row in enumerate(grid):
        if r_idx % 3 == 0 and r_idx != 0:
            print("-" * 25)  # Horizontal separator for 3x3 blocks

        for c_idx, num in enumerate(row):
            if c_idx % 3 == 0 and c_idx != 0:
                print("| ", end="")  # Vertical separator for 3x3 blocks
            
            # Replace '0' or '.' with a space for empty cells
            display_num = num if num != '0' and num != '.' else '0'
            print(f"{display_num} ", end="")
        print()
    print("\n")


print_sudoku_layout(question_board_code[0])

print_sudoku_layout(solvedSud)


print("code is done")
