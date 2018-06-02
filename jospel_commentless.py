import itertools
import random


CARD_POOL = [val for val in list(range(1, 11)) for _ in (0, 1)]
COLUMN_FACTORS = {"A": 0,
                  "B": 1,
                  "C": 2,
                  "D": 3,
                  }
EMPTY_TILE = "[]"

def all_sublists_from_list(given_list, sublist_size):
    length_difference = len(given_list) - sublist_size
    if length_difference == 0:
        return [given_list]
    elif length_difference < 0:
        raise IndexError
    returnable = []
    for i in range(length_difference+1):
        returnable.append(given_list[i:i+sublist_size])
    return returnable

def detect_one_by_one_changing_list(given_list):
    direction = 0
    for y, i in enumerate(given_list):
        if y == 0:
            continue
        if direction == 0:
            if given_list[y-1] == i + 1:
                direction = 1
            elif given_list[y-1] == i - 1:
                direction = -1
            else:
                return False
        else:
            if given_list[y-1] != i + direction:
                return False
    return True

def detect_pair_in_row(row):
    for y, i in enumerate(row):
        if y == 3:
            return 0
        if i == row[y+1]:
            return 10

def detect_double_pair_in_row(row):
    if row[0] == row[1] and row[2] == row[3]:
        return 20
    elif row[0] == row[2] and row[1] == row[3]:
        return 20
    return 0

def detect_short_streak_in_row(row):
    sublists = all_sublists_from_list(row, 3)
    for i in sublists:
        if detect_one_by_one_changing_list(i):
            return 30
    return 0

def detect_long_streak_in_row(row):
    if detect_one_by_one_changing_list(row):
        return 40
    return 0

def detect_jospel_in_row(row):
    if all(i == 10 or i == 1 for i in row):
        return 50
    return 0

def max_points_of_row(row):
    all_found_points = []
    operations = [detect_pair_in_row,
                  detect_double_pair_in_row,
                  detect_short_streak_in_row,
                  detect_long_streak_in_row,
                  detect_jospel_in_row,
                  ]
    names = {10: "pair",
             20: "double pair",
             30: "short streak",
             40: "long streak",
             50: "Jospel",
             }
    for func in operations:
        all_found_points.append(func(row))
    if 10 in all_found_points and 30 in all_found_points:
        return (40, "pair + streak")
    else:
        best_value = max(all_found_points)
        if best_value == 0:
            return None
        return (best_value, names[best_value])

def display_board(board):
    print(" X │ A  B  C  D ")
    print("───┼────────────")
    for i in range(0, 16, 4):
        print(" {} │".format((i+4)//4), end=" ")
        for y in range(4):
            current_tile = str(board[i + y])
            print((" " if len(current_tile) == 1 else "") + current_tile, end=" ")
        print()

def display_board_with_bonuses(board, points):
    print(" X │ A  B  C  D  │")
    print("───┼─────────────┤")
    for i in range(0, 16, 4):
        row_number = i//4
        row_points = points[row_number]
        print(" {} │".format(row_number + 1), end=" ")
        for y in range(4):
            current_tile = str(board[i + y])
            print((" " if len(current_tile) == 1 else "") + current_tile, end=" ")
        if row_points is not None:
            print("│ ← {} ({})".format(row_points[1], row_points[0]))
        else:
            print("│")
    print("───┴─────────────┘")
    for j in range(4):
        row_points = points[4 + j]
        space_amount = 6 + 3 * j
        if row_points is not None:
            print("{}↑ {} ({})".format(space_amount * " ", row_points[1], row_points[0]))

def location_to_index(loc):
    if int(loc[1]) > 4:
        raise IndexError
    return COLUMN_FACTORS[loc[0]] + (int(loc[1]) * 4 - 4)

while True:
    current_card_pool = list(CARD_POOL)
    random.shuffle(current_card_pool)
    current_card_pool = current_card_pool[:16]
    board = [EMPTY_TILE] * 16
    played_cards = list(current_card_pool)
    while current_card_pool:
        chosen_number = current_card_pool.pop()
        print("\n" * 20)
        display_board(board)
        got_target = False
        while not got_target:
            try:
                target = location_to_index(input(f"\n\nChoose a location for {chosen_number} >>> ").upper())
            except (IndexError, KeyError, ValueError):
                print("Invalid position, try again")
            else:
                if board[target] == EMPTY_TILE:
                    got_target = True
                else:
                    print("Position filled, try again")
        board[target] = chosen_number
    row_indices = [[0,  1,  2,  3],
                   [4,  5,  6,  7],
                   [8,  9,  10, 11],
                   [12, 13, 14, 15],
                   [0,  4,  8,  12],
                   [1,  5,  9,  13],
                   [2,  6,  10, 14],
                   [3,  7,  11, 15],
                   ]
    total_rows = []
    for r in row_indices:
        current_row = []
        for i in r:
            current_row.append(board[i])
        total_rows.append(current_row)
    results = []
    for i in total_rows:
        results.append(max_points_of_row(i))
    results_clean = [x[0] for x in results if x is not None]
    print("\n\n\nG A M E   O V E R !\n\n")
    display_board_with_bonuses(board, results)
    print(f"\n\nYou earned {sum(results_clean)} points!")
    print("Cards given in this round: {}".format(", ".join([str(x) for x in played_cards])))
    input("Any key to continue...")
