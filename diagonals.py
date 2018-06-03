import itertools
import random
from numpy import base_repr


CARD_POOL = [val for val in list(range(1, 11)) for _ in (0, 1)]
COLUMN_FACTORS = {"A": 0,
                  "B": 1,
                  "C": 2,
                  "D": 3,
                  }
EMPTY_TILE = "[]"

def all_sublists_from_list(given_list, sublist_size):
    """Get all sublists of given length `sublist_size` from longer list
    `given_list`.

    Returns all the possible sublists in a list of lists.
    Raises IndexError if desired sublist size is bigger than given list
    size.
    """
    length_difference = len(given_list) - sublist_size
    # If the desired length is the same as the given list.
    if length_difference == 0:
        # No caluclations are needed, return the original list.
        return [given_list]
    # If the desired length is longer than the given length.
    elif length_difference < 0:
        # Impossible to find such sublists, raise IndexError.
        raise IndexError
    returnable = []
    # Iterate through all the spare space given by the difference.
    for i in range(length_difference+1):
        # Add a slice, starting from the currently iterating position,
        # the length of which will be the desired sublist size, to the
        # list which will be returned.
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

def encode_seed(played_cards):
    
    seed = [0 if x==10 else x for x in played_cards]
    seed = "".join(str(x) for x in seed)
    seed = base_repr(int(seed), 36)
    return seed

def decode_seed(seed):

    seed = int(seed.upper(), 36)
    seed = [int(x) for x in list(str(seed))]
    seed = [10 if x==0 else x for x in seed]
    return seed

def detect_faulty_seed(seed):
    try:
        decoded_seed = decode_seed(seed)
    except Exception as e:
        return "Decoding seed threw and error {}".format(e)
    if len(decoded_seed) != 16:
        return "Seed is wrong length, please make sure you copied it correctly."
    return False

def detect_pair_in_row(row):
    """Find if a sequence of repeating number next to eachother
    exists in 4-length int list `row`.

    Example:
    [2, 3, 3, 8] has a pair (positions 1 and 2).

    Return the amount of points gained from this row,
    10 if there's a pair, 0 if there isn't.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """

    for y, i in enumerate(row):  # Go through every item in the row.
        if y == 3:  # If we're already at the last item
            return 0  # return that nothing was found.
        # Check if the item we're iterating on and the item that follows are identical.
        if i == row[y+1]:
            return 10  # Return the amount of points gained from a row (10).

def detect_double_pair_in_row(row):
    """Find if a sequence of two repeating pairs or a sequence of
    two alternating number exists in 4-length int list `row`.

    Examples:
    [4, 4, 9, 9] includes two repeating pairs (1=2, 3=4).
    [3, 7, 3, 7] includes two alternating numbers (1=3, 2=4).

    Return the amount of points gained from this row,
    20 if there's a double pair, 0 if there isn't.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """

    if row[0] == row[1] and row[2] == row[3]:
        return 20
    elif row[0] == row[2] and row[1] == row[3]:
        return 20
    return 0
    # Big row of checks because I'm lazy to find a better method

def detect_short_streak_in_row(row):
    """Find if a sequence of three consecutive numbers exists
    in any position in 4-length int list `row`.
    A streak can progress in any direction, either ascending or
    descending when counting from the left.

    Example:
    [7, 3, 4, 5] includes a short streak (3<4<5).

    Return the amount of points gained from this row,
    30 if there's a short streak, 0 if there isn't.

    Special case: Unlike any other combination,
    single pair + short row is the only combination with combined
    points that can be gained. (10 + 30 = 40).
    This logic is handled by the master row handler.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """

    sublists = all_sublists_from_list(row, 3)
    for i in sublists:
        if detect_one_by_one_changing_list(i):
            return 30
    return 0

def detect_long_streak_in_row(row):
    """Find if a sequence of four consecutive numbers exists
    in any position in 4-length int list `row`.
    A streak can progress in any direction, either ascending or
    descending when counting from the left.

    Example:
    [9, 8, 7, 6] includes a long streak (9>8>7>6).

    Return the amount of points gained from this row,
    40 if there's a long streak, 0 if there isn't.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """

    if detect_one_by_one_changing_list(row):
        return 40
    return 0

def detect_jospel_in_row(row):
    """Find if a sequence of only the number 1 and 10 exist in 4-length int list `row`.
    These numbers can exist in any order, as long as only those two number are in it.
    In the code, documentation, and user interface of this program, this
    sequence is referred to as a "Jospel".

    Example:
    [1, 10, 1, 10] includes a Jospel.

    Return the amount of points gained from this row,
    50 if there's a Jospel, 0 if there isn't.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """
    if all(i == 10 or i == 1 for i in row):
        return 50
    return 0

def max_points_of_row(row):
    """Find the most amount of points you could earn from the 4-length int list `row`
    This function runs through all the combinations of Jospel on the row.

    A single row can only yield points for one pattern, the only exception is
    the combination of short streak + pair, where you can get both at once on
    one row and gain 30 + 10 = 40 points.

    Returns None if no pattern was found
    Returns a tuple (points, name), where points is the amount of points gained
    from that row and name is the name of that pattern.

    An invalid input list, which doesn't match the criteria of 4-length int list
    isn't handled and may cause unforseeable consequences.
    """
    all_found_points = []  # Prepare an empty list where the matching patters are added.
    # This list contains all the patterns of Jospel, in function form as defined above.
    # Note that we aren't actually running the functions, just storing it.
    operations = [detect_pair_in_row,         # 10 points
                  detect_double_pair_in_row,  # 20 points
                  detect_short_streak_in_row, # 30 points
                  detect_long_streak_in_row,  # 40 points
                  detect_jospel_in_row,       # 50 points
                  ]
    # As the pattern functions return the amount of points gained from said function, this
    # dict converts those points into a more readable representation of that pattern.
    names = {10: "pair",
             20: "double pair",
             30: "short streak",
             40: "long streak",
             50: "Jospel",
             }
    for func in operations:  # Goes through every pattern function
        all_found_points.append(func(row))  # Runs each one with the given row
    # Special case: in case of a pair (10) and a short streak (30), combine the points of the two
    if 10 in all_found_points and 30 in all_found_points:
        return (40, "pair + streak")
    else:
        best_value = max(all_found_points)
        if best_value == 0:  # No patterns were found
            return None
        # Return the max of the values and the name of it
        return (best_value, names[best_value])

def display_board(board):
    """Prints out the 16-length int list `board`, formatted neatly for readability
    Displays the row numbers and column letter, which the player can use to position
    their numbers.

    Gives no output, directly prints.

    An invalid input list, which doesn't match the criteria of 16-length int list
    isn't handled and may cause unforseeable consequences.
    """
    print(" X │ A  B  C  D ")  # Hard-coded column headers
    print("───┼────────────")
    for i in range(0, 16, 4):  # Iterate through every beginning of a row, as rows are 4 tiles wide
        # Formatting magic. It works.
        print(" {} │".format((i+4)//4), end=" ")
        for y in range(4):
            current_tile = str(board[i + y])
            print((" " if len(current_tile) == 1 else "") + current_tile, end=" ")
        print()

def display_board_with_bonuses(board, points):
    """Prints out the 16-length int list `board`, formatted neatly for readability
    Displays the row numbers and column letter, which the player can use to position
    their numbers. Also displays the amount of points recieved for each row and column,
    taking data from 8-length tuple list `points`, where the tuple structure is
    (points, name), where `points` is the amount of points gained from the row and `name`
    is the name of that pattern.

    Gives no output, directly prints.

    Invalid input lists, which don't match the aformentioned criteria aren't handled and
    may cause unforseeable consequences.
    """
    print(" X │ A  B  C  D  │")  # Hard-coded column headers
    print("───┼─────────────┤")
    # I'm sorry if you need to do anything with this part. This deals with formatting and is a mess,
    # it works and I don't reccommend you touch it.
    # here be dragons.
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
    # dragons are gone.

def location_to_index(loc):
    """Converts the column-row notation string `loc` given by the user when playing into a list
    index used for the board.

    An example of a possible input:
    B3 - refers to the second 2nd column B and 3rd row 3. Converted into 9 by the function.

    Returns the list index of that location.

    Handles no errors on it's own, must be handled outside this function.
    """
    if int(loc[1]) > 4: # If the player tries to enter a row beyond the 4th
        raise IndexError
    # Simple return statement, calculating the index. The row number is simply multiplied by 4
    # (and 4 is subtracted because of zero-indexing), and is added to the column number. The
    # column number is found using a const dict `COLUMN_FACTORS`.
    # Note: this small snippet causes lots of error for many reasons of invalid input. Must be
    # handled outside the function.
    return COLUMN_FACTORS[loc[0]] + (int(loc[1]) * 4 - 4)

# Here's the main game logic, inside of a while True loop, since I don't intend to use the
# functionality elsewhere.
while True:
    board = [EMPTY_TILE] * 16  # Fill the board with empty tiles.

    seed_choice = input("Enter the custom seed for this game, leave blank for none >>> ")
    if seed_choice == "":
        current_card_pool = list(CARD_POOL)  # Creates a static copy of the card pool const list.
        random.shuffle(current_card_pool)  # Shuffle the card deck for a fair game.
        # Pick only 16 cards from the pool, as we'll only need that many.
        current_card_pool = current_card_pool[:16]
        # Create a duplicate of this round's card pool, for scorekeeping later.
        played_cards = list(current_card_pool)
        seed = encode_seed(played_cards)
        print("Seed for this game: {}\n\n".format(seed))
    else:
        
        if detect_faulty_seed(seed_choice):
            print(detect_faulty_seed(seed_choice))
            continue
        current_card_pool = decode_seed(seed_choice)
        played_cards = list(current_card_pool)

    turns_taken = 0
    while current_card_pool:  # While there are still cards in the pool.
        if turns_taken == 16:
            print("Game has lasted too long, forcing end.")
            break
        # Pop the top card. As the list is shuffled this is random anyway.
        chosen_number = current_card_pool.pop()
        display_board(board)
        got_target = False  # bool denoting if a position for the number has been chosen.
        while not got_target:
            try:
                target = location_to_index(input(f"\n\nChoose a location for {chosen_number} >>> ").upper())
            # All the errors that can arise from location_to_index() when the input is invalid.
            except (IndexError, KeyError, ValueError):
                print("Invalid position, try again")
            else:
                if board[target] == EMPTY_TILE:
                    got_target = True  # Found a valid position, end while loop.
                else:  # If the chosen position isn't empty
                    print("Position filled, try again")
        board[target] = chosen_number  # Update the board with the number
        turns_taken += 1
        print("\n" * 20)  # Print some whitespace for better formatting.

    row_indices = [[0,  1,  2,  3],  #  0  1  2  3
                   [4,  5,  6,  7],  #  4  5  6  7
                   [8,  9,  10, 11], #  8  9 10 11
                   [12, 13, 14, 15], # 12 13 14 15
                   [0,  4,  8,  12],
                   [1,  5,  9,  13], # This list has all the rows and columns
                   [2,  6,  10, 14], # that the system should check for patterns.
                   [3,  7,  11, 15],
                   [0,  5,  10, 15],
                   [3,  6,  9,  12],
                   ]

    # This part of the code turns all rows and columns into lists, for dealing with later.
    total_rows = []
    for r in row_indices:
        current_row = []
        for i in r:
            current_row.append(int(board[i]))
        total_rows.append(current_row)

    # This part of the code finds the max points of every row and column into a seperate list.
    results = []
    for i in total_rows:
        results.append(max_points_of_row(i))

    # Removes all the rows that gave no points
    results_clean = [x[0] for x in results if x is not None]

    # Nice messages for the user
    print("\n\n\nG A M E   O V E R !\n\n")
    display_board_with_bonuses(board, results)
    print(f"\n\nYou earned {sum(results_clean)} points!")
    print("Cards given in this round: {}".format(", ".join([str(x) for x in reversed(played_cards)])))
    input("Enter to continue...")
####################################################################################################
######### The following code is still a work in progress, and doesn't even work. Don't try #########
##                                                                                                ##
##    all_permutations = itertools.permutations(played_cards)                                     ##
##    best_score = 0                                                                              ##
##    best_permutation = []                                                                       ##
##    print(all_permutations)                                                                     ##
##    for i in all_permutations:                                                                  ##
##        total_rows = []                                                                         ##
##        for r in row_indices:                                                                   ##
##            current_row = []                                                                    ##
##            for k in r:                                                                         ##
##                current_row.append(i[k])                                                        ##
##            total_rows.append(current_row)                                                      ##
##        results = []                                                                            ##
##        for j in total_rows:                                                                    ##
##            results.append(max_points_of_row(j))                                                ##
##        results_clean = [x[0] for x in results if x is not None]                                ##
##        current_points = sum(results_clean)                                                     ##
##        if current_points > best_score:                                                         ##
##            best_score = current_points                                                         ##
##            print("::::::::" + str(best_score))                                                 ##
##            best_permutation = i                                                                ##
##            display_board_with_bonuses(i, results)                                              ##
##    print(best_permutation)                                                                     ##
##    input("Enter to continue...")                                                               ##
##                                                                                                ##
####################################################################################################
####################################################################################################
