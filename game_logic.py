import random

AVERAGE_DIFFICULTY = 6  # 0 to 10, x of 10, average chance of effective autoplay move, at 10 only draw is possible

WINNING_INDEXES = ({0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # rows
                   {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, # columns
                   {0, 4, 8}, {2, 4, 6})  # diagonals


def winning_cells(player_taken):
    player_taken = set(player_taken)
    winning = set()
    for cellset in WINNING_INDEXES:
        if cellset.issubset(player_taken):
            winning.update(cellset)
    if winning:
        return winning


def is_draw(active_player_taken):
    active_player_taken = set(active_player_taken)
    return all([0 < len(active_player_taken & wi) < 3 for wi in WINNING_INDEXES])


def autoplay(free_cells, bot_taken, opponent_taken):
    global WINNING_INDEXES
    free_cells_set = set(free_cells)
    bot_taken = set(bot_taken)
    opponent_taken = set(opponent_taken)

    effective_autoplay = random.choices([True, False], weights=[AVERAGE_DIFFICULTY, 10 - AVERAGE_DIFFICULTY], k=1)[0]

    if effective_autoplay:
        for winning in WINNING_INDEXES:
            # WIN:
            if len(winning - bot_taken) == 1 and (winning - bot_taken).pop() in free_cells_set:
                return (winning - bot_taken).pop()
            # BLOCK:
            if len(winning - opponent_taken) == 1 and (winning - opponent_taken).pop() in free_cells_set:
                return (winning - opponent_taken).pop()
        # FORK:
        forks = ({0, 1, 3, 4}, {1, 2, 4, 5}, {3, 4, 6, 7}, {4, 5, 7, 8})
        for fork in forks:
            if len(fork - bot_taken) == 1 and (fork - bot_taken).pop() in free_cells_set:
                return (fork - bot_taken).pop()
            if len(fork - opponent_taken) == 1 and (fork - opponent_taken).pop() in free_cells_set:
                return (fork - opponent_taken).pop()
        # CENTER:
        if 4 in free_cells_set:
            return 4
        # OPPOSITE CORNER:
        for corner_pair in ({0, 8}, {2, 6}):
            if len(opponent_taken & corner_pair) == 1 and (corner_pair - (opponent_taken & corner_pair)).pop() \
                    in free_cells_set:
                return (corner_pair - (opponent_taken & corner_pair)).pop()
        # EMPTY CORNER
        corners = {0, 2, 6, 8}
        if corners & free_cells_set:
            return random.choice(tuple(corners & free_cells_set))
        # EMPTY SIDE
        sides_middles = {1, 3, 5, 7}
        if sides_middles & free_cells_set:
            return random.choice(tuple(sides_middles & free_cells_set))

    else:
        # RANDOM
        return random.choice(free_cells)
