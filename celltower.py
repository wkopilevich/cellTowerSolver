import requests

neighborOffsets = list((dy,dx) for dy in range(-1,2) for dx in range(-1,2) if abs(dy) != abs(dx))
minWordLength = 4
maxWordLength = 8

# generate all possible polys from a given start cell
def gen_polys(curr_poly, curr_state):
    ret = ()
    if len(curr_poly) >= minWordLength and len(curr_poly) <= maxWordLength:
        ret = ((curr_poly),)
    if len(curr_poly) < 8:
        for curr_cell in curr_poly:
            for (dy,dx) in neighborOffsets:
                pot_cell = (curr_cell[0]+dy, curr_cell[1]+dx)
                if 0 <= pot_cell[0] < grid_height and 0 <= pot_cell[1] < grid_width and pot_cell not in curr_poly and pot_cell not in curr_state:
                    ret += gen_polys(tuple(sorted(curr_poly + ((pot_cell),))), curr_state)
    return ret

# recursively match remaining grid cells to polys and words
def solve(curr_cell, curr_state):
    if len(curr_state) >= grid_height*grid_width:
        print('solved')
        return True
    
    # filter words based on current start cell
    filtered_words = [w for w in words if w.startswith(GRID[curr_cell[0]][curr_cell[1]].lower())]

    # generate all valid forms starting from start_cell
    forms = sorted(set(gen_polys((curr_cell, ), curr_state)))

    for currForm in forms:
        resWord = ''
        for currCell in currForm:
            resWord += GRID[currCell[0]][currCell[1]]

        if resWord.lower() in filtered_words:
            # find next start cell
            nextStartCell = (0,0)
            for y in range(grid_height):
                if nextStartCell == (0,0):
                    for x in range(grid_width):
                        if (y,x) not in curr_state and (y,x) not in currForm:
                            nextStartCell = (y,x)
                            break

            if solve(nextStartCell,curr_state + currForm):
                print('Form:', currForm, 'word:', resWord)   
                return True


words = requests.get("https://www.andrewt.net/puzzles/cell-tower/assets/words.json").json()

GRID = '''
REVECRE
RSSPOUD
MOERLUC
LOTADTE
ETHCRAS
TELTINM
RSIISEO
GRKIGRN
OUENOIN
NDRIFUG
LSANGNS
NDINGDS
'''.strip().splitlines()


grid_width = len(GRID[0])
grid_height = len(GRID)

solve((0,0),())