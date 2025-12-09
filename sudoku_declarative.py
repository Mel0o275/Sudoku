import random
from typing import List, Optional, Tuple

Grid = List[List[int]]


#ai solver
def solve(grid: Grid) -> List[Grid]:

    empty = find_empty(grid)
    if empty is None:
        return [grid]  

    row, col = empty

    solutions = []
    # for num in range(1, 10):
    #     if is_valid(grid, row, col, num):
    #         new_grid = update_grid(grid, row, col, num)
    #         solutions.extend(solve(new_grid))
    solutions = sum(
        [solve(update_grid(grid, row, col, num))
        for num in range(1, 10)
        if is_valid(grid, row, col, num)],
        []
    )
    return solutions
    
    
    
    

def is_valid(grid: Grid, row: int, col: int, num: int) -> bool:
    def check_row(r: List[int], idx: int = 0) -> bool:
        return False if idx >= 9 else (r[idx] == num or check_row(r, idx + 1))

    def check_col(c: int, idx: int = 0) -> bool:
        return False if idx >= 9 else (grid[idx][c] == num or check_col(c, idx + 1))

    def check_box(start_r: int, start_c: int, r_idx: int = 0, c_idx: int = 0) -> bool:
        if r_idx >= 3:
            return False
        if c_idx >= 3:
            return check_box(start_r, start_c, r_idx + 1, 0)
        return (grid[start_r + r_idx][start_c + c_idx] == num or
                check_box(start_r, start_c, r_idx, c_idx + 1))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    return not (check_row(grid[row]) or check_col(col) or check_box(start_row, start_col))


def find_empty_cells(grid: Grid, r: int = 0, c: int = 0, acc: List[Tuple[int,int]] = None) -> List[Tuple[int,int]]:
    acc = acc or []
    if r >= 9:
        return acc[::-1]
    if c >= 9:
        return find_empty_cells(grid, r + 1, 0, acc)
    new_acc = [(r, c)] + acc if grid[r][c] == 0 else acc
    return find_empty_cells(grid, r, c + 1, new_acc)


def solve_sudoku(grid: Grid, random_state: Optional[random.Random] = None) -> Optional[Grid]:
    empty_cells = find_empty_cells(grid)
    if not empty_cells:
        return grid

    row, col = empty_cells[0]
    nums = list(range(1, 10))
    shuffled_nums = random_state.sample(nums, len(nums)) if random_state else random.sample(nums, len(nums))

    def try_numbers(nums_list: List[int]) -> Optional[Grid]:
        if not nums_list:
            return None
        num = nums_list[0]
        if is_valid(grid, row, col, num):
            def copy_grid(r_idx: int = 0, new_grid: Grid = None) -> Grid:
                new_grid = new_grid or []
                if r_idx >= 9:
                    return new_grid[::-1] 
                new_row = grid[r_idx][:]
                if r_idx == row:
                    new_row = new_row[:col] + [num] + new_row[col+1:]
                return copy_grid(r_idx + 1, [new_row] + new_grid) 

            new_grid = copy_grid()
            solved = solve_sudoku(new_grid, random_state)
            if solved:
                return solved
        return try_numbers(nums_list[1:])

    return try_numbers(shuffled_nums)


def remove_cells(grid: Grid, cells: List[Tuple[int,int]]) -> Grid:
    if not cells:
        return grid

    r, c = cells[0]

    def create_new_grid(row_idx: int = 0, new_grid: Grid = None) -> Grid:
        new_grid = new_grid or []
        if row_idx >= 9:
            return new_grid[::-1]
        if row_idx == r:
            new_row = grid[row_idx][:c] + [0] + grid[row_idx][c+1:]
        else:
            new_row = grid[row_idx][:]
        return create_new_grid(row_idx + 1, [new_row] + new_grid)

    new_grid = create_new_grid()
    return remove_cells(new_grid, cells[1:])


def generate_sudoku_pair(removals: int = 40, seed: Optional[int] = None) -> Tuple[Grid, Grid]:
    random_state = random.Random(seed)

    def create_empty_grid(row: int = 0, grid: Grid = None) -> Grid:
        grid = grid or []
        if row >= 9:
            return grid
        return create_empty_grid(row + 1, grid + [[0] * 9])

    empty_grid = create_empty_grid()
    full_grid = solve_sudoku(empty_grid, random_state)

    if not full_grid:
        return None, None

    def all_cells(r: int = 0, c: int = 0, acc: List[Tuple[int,int]] = None) -> List[Tuple[int,int]]:
        acc = acc or []
        if r >= 9:
            return acc[::-1]
        if c >= 9:
            return all_cells(r + 1, 0, acc)
        new_acc = [(r, c)] + acc
        return all_cells(r, c + 1, new_acc)

    all_cell_coords = all_cells()
    shuffled_cells = random_state.sample(all_cell_coords, len(all_cell_coords))
    cells_to_remove = shuffled_cells[:removals]

    puzzle_grid = remove_cells(full_grid, cells_to_remove)
    return puzzle_grid, full_grid


if __name__ == "__main__":
    puzzle, solution = generate_sudoku_pair(40)

    if puzzle and solution:
        def print_row_recursive(row, c=0):
            if c == 9:
                print()
                return
            if c > 0 and c % 3 == 0:
                print("|", end=" ")
            print(str(row[c]) if row[c] != 0 else ".", end=" ")
            print_row_recursive(row, c + 1)

        def print_grid_recursive(grid, r=0):
            if r == 9:
                return
            if r > 0 and r % 3 == 0:
                print("-" * 21)
            print_row_recursive(grid[r])
            print_grid_recursive(grid, r + 1)

        print("RANDOM SUDOKU PUZZLE")
        print_grid_recursive(puzzle)

        print()
        print("SOLUTION")
        print_grid_recursive(solution)
    else:
        print("No solution exists.")