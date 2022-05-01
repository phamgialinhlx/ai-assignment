
class State:
    def __init__(self):
        self.board = [
            ['*', '*', '*'],
            ['*', '*', '*'],
            ['*', '*', '*'],
        ]

    def print(self):
        for row in self.board:
            print(' '.join(row))


    def successor(self, action):
        ## return new state
        new_state = State()
        for i in range(3):
            for j in range(3):
                if i != action.row or j != action.col:
                    new_state.board[i][j] = self.board[i][j]
                else:
                    new_state.board[i][j] = action.player
        return new_state

    def get_player(self):
        countX = 0
        countO = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'X': countX += 1
                elif self.board[i][j] == 'O': countO += 1
        if countX == countO: return 'X'
        else: return 'O'

    def get_n_actions(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '*': count += 1
        return 9-count

    def get_successors_and_actions(self):
        ## return list of (action, next_state)
        player = self.get_player()
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '*':
                    action = Action(i, j, player)
                    yield action, self.successor(action)

    def is_terminal(self):
        for i in range(3): 
            if self.check_row(i, 'X') or self.check_row(i, 'O'): return True
        for j in range(3): 
            if self.check_col(j, 'X') or self.check_col(j, 'O'): return True
        if self.check_diag('X') or self.check_diag('O'): return True
        if self.check_other_diag('X') or self.check_other_diag('O'): return True
        if self.get_n_actions() == 9: return True
        return False

    def check_row(self, i, player):
        for j in range(3):
            if self.board[i][j] != player: return False
        return True

    def check_col(self, j, player):
        for i in range(3):
            if self.board[i][j] != player: return False
        return True

    def check_diag(self, player):
        for i in range(3):
            if self.board[i][i] != player: return False
        return True

    def check_other_diag(self, player):
        for i in range(3):
            if self.board[i][2-i] != player: return False
        return True

    def utility(self):
        if self.is_terminal():
            value = 0
            for i in range(3): 
                if self.check_row(i, 'X'): value = 1
                if self.check_row(i, 'O'): value =  -1
            for j in range(3): 
                if self.check_col(j, 'X'): value =  1
                if self.check_col(j, 'O'): value =  -1
            if self.check_diag('X'): value =  1
            if self.check_diag('O'): value =  -1
            if self.check_other_diag('X'): value = 1
            if self.check_other_diag('O'): value =  -1
            return value - self.get_n_actions()*0.1
        else: return None


def get_value(state):
    ## return value, best_action
    if state.is_terminal():
        return state.utility(), None

    player = state.get_player()
    if player == 'X': return get_max_value(state)
    else: return get_min_value(state)


def get_max_value(state):
    ## return value, best_action
    max_value = -100
    best_action = None
    for action, next_state in state.get_successors_and_actions():
        next_value, _ = get_value(next_state)
        if next_value > max_value:
            max_value = next_value
            best_action = action

    assert(best_action is not None)
    return max_value, best_action


def get_min_value(state):
    ## return value, best_action
    min_value = 100
    best_action = None
    for action, next_state in state.get_successors_and_actions():
        next_value, _ = get_value(next_state)
        if next_value < min_value:
            min_value = next_value
            best_action = action

    assert(best_action is not None)
    return min_value, best_action

class Action:
    def __init__(self, row, col, player):
        # player = X or O
        self.row = row
        self.col = col
        self.player = player

    def print(self):
        print('row: {}, col: {}, player: {}'.format(self.row, self.col, self.player))


if __name__ == '__main__':
    state = State()
    answer = input("Do you want to play first (y/n)?")
    if answer.lower() == 'y':
        human_player = 'X'
    else:
        human_player = 'O'
    current_player = 'X'
    count = 0
    while not state.is_terminal():
        state.print()
        if current_player == human_player:
            valid_actions = list(state.get_successors_and_actions())
            for i, (action, next_state) in enumerate(valid_actions):
                print(i, end=': ')
                action.print()
            answer = input(f"Your move: [ 0 - {len(valid_actions)-1} ]")
            action, next_state = valid_actions[int(answer)]
            state = next_state
        else:
            best_value, best_action = get_value(state)
            print(f"(value={best_value}) I play: ", end='')
            best_action.print()
            state = state.successor(best_action)

        count += 1
        current_player = state.get_player()
    
    print("Last state")
    state.print()