from random import randint
from os import system
from platform import system as os_name
from time import sleep

static_game_board = """\
 ----- ----- -----
|     |     |     |
|  1  |  2  |  3  |
|     |     |     |
 ----- ----- -----
|     |     |     |
|  4  |  5  |  6  |
|     |     |     |
 ----- ----- -----
|     |     |     |
|  7  |  8  |  9  |
|     |     |     |
 ----- ----- ----- """

banner = """\
___________.__     ___________           ___________            
\__    ___/|__| ___\__    ___/____    ___\__    ___/___   ____  
  |    |   |  |/ ___\|    |  \__  \ _/ ___\|    | /  _ \_/ __ \ 
  |    |   |  \  \___|    |   / __ \\  \___ |    |(  <_> )  ___/ 
  |____|   |__|\___  >____|  (____  /\___  >____| \____/ \___  >
                    \/             \/     \/                  \/ """

# game board cells of each field
fields_data = {1: [20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 60, 61, 62, 63, 64],
               2: [26, 27, 28, 29, 30, 46, 47, 48, 49, 50, 66, 67, 68, 69, 70],
               3: [32, 33, 34, 35, 36, 52, 53, 54, 55, 56, 72, 73, 74, 75, 76],
               4: [99, 100, 101, 102, 103, 119, 120, 121, 122, 123, 139, 140, 141, 142, 143],
               5: [105, 106, 107, 108, 109, 125, 126, 127, 128, 129, 145, 146, 147, 148, 149],
               6: [111, 112, 113, 114, 115, 131, 132, 133, 134, 135, 151, 152, 153, 154, 155],
               7: [178, 179, 180, 181, 182, 198, 199, 200, 201, 202, 218, 219, 220, 221, 222],
               8: [184, 185, 186, 187, 188, 204, 205, 206, 207, 208, 224, 225, 226, 227, 228],
               9: [190, 191, 192, 193, 194, 210, 211, 212, 213, 214, 230, 231, 232, 233, 234]}

# possible winning situations
winning_positions = {1: [1, 2, 3],
                     2: [4, 5, 6],
                     3: [7, 8, 9],
                     4: [1, 4, 7],
                     5: [2, 5, 8],
                     6: [3, 6, 9],
                     7: [1, 5, 9],
                     8: [3, 5, 7]}

# data used for visual help where there is win
cross_fields_data = {1: [40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56],
                     2: [119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135],
                     3: [198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 210, 211, 212, 213, 214],
                     4: [22, 42, 62, 101, 121, 141, 180, 200, 220],
                     5: [28, 48, 68, 107, 127, 147, 186, 206, 226],
                     6: [34, 54, 74, 113, 133, 153, 192, 212, 232],
                     7: [21, 42, 63, 106, 127, 148, 191, 212, 233],
                     8: [35, 54, 73, 108, 127, 146, 181, 200, 219]}


def nickname_input(player_symbol):
    """
    Function to make nicknames feature
    better and more accurate

    :param player_symbol: symbol on game board, for example 'X'
    :return: nick
    """
    nick = ''

    while True:
        clear_screen()
        print('Enter nick for player with', player_symbol)
        nick = input('Enter nick: ') 
        clear_screen()
        if nick == '':
            print("Nickname can't be empty!")
            sleep(0.5)
            clear_screen()
            continue
        elif nick != '':
            clear_screen()
            break

    return nick 


def list_to_string(_list):
    """
    Convert any string converted
    to list back to string easily 

    :param _list: list to convert
    :return: beautiful string recovered from list
    """
    string = ''
    for char in _list:
        string += ''.join(char)

    return string


def choose_field(number, symbol):
    """
    Function to handle field selection

    :param number: field number
    :param symbol: by default 'X' or 'O'
    :return: void function
    """

    number = int(number)

    while True:
        try:
            while True:
                if number in chosen_fields_X or number in chosen_fields_O:
                    print("You can't choose already chosen field")
                    sleep(0.5)
                    clear_screen()
                    print(list_to_string(dynamic_game_board))
                    number = int(input('Select a field({}): '.format(symbol)))
                else:
                    break 
            for fields in fields_data[number]:
                dynamic_game_board[fields] = symbol
            if symbol == 'X':
                chosen_fields_X.append(number)
            elif symbol == 'O':
                chosen_fields_O.append(number)
        except ValueError:
            print('You have to enter a number')
            sleep(0.5)
            clear_screen()
            print(list_to_string(dynamic_game_board))
            number = int(input('Select a field({}): '.format(symbol)))
        except KeyError:
            print('You have to enter a number in range from 1 to 9')
            sleep(0.5)
            clear_screen()
            print(list_to_string(dynamic_game_board))
            number = int(input('Select a field({}): '.format(symbol)))
        else:
            break 
        
     
def cross_winning_fields(position_number):
    """
    Visual help for showing winning position
    on game board

    :param position_number: number of winning position
    :return: void function
    """
    if position_number in [1, 2, 3]:
        symbol = '-'
    elif position_number in [4, 5, 6]:
        symbol = '|'
    elif position_number == 7:
        symbol = "\\"
    else:
        symbol = '/'

    for data in cross_fields_data[position_number]:
        dynamic_game_board[data] = symbol


def check_win():
    """
    Checks if one of the sides already won
    or if there is tie

    :return: decision
    """
    decision = -2
    position = 0
    set_fields_x = set(chosen_fields_X)
    set_fields_o = set(chosen_fields_O)

    for i in range(1, 9):
        set_positions = set(winning_positions[i])
        position += 1
        if set_positions.intersection(set_fields_x) == set_positions:
            decision = -1
            break
        elif set_positions.intersection(set_fields_o) == set_positions:
            decision = 1
            break
        elif len(chosen_fields_X) + len(chosen_fields_O) == 9:
            decision = 0
            break 

    if decision == -1:
        clear_screen()
        cross_winning_fields(position)
        print(list_to_string(dynamic_game_board))
        print(nick1, 'won!!!')
    elif decision == 1:
        clear_screen()
        cross_winning_fields(position)
        print(list_to_string(dynamic_game_board))
        print(nick2, 'won!!!')
    elif decision == 0 and len(chosen_fields_X) + len(chosen_fields_O) == 9:
        clear_screen()
        print(list_to_string(dynamic_game_board))
        print('Tie!!!')
    
    if decision in [-1, 0, 1]:
        print('Want to play again?')
        play_again = input('Type (y/n): ') 
        if play_again == 'y':
            return 'y'
        elif play_again == 'n': 
            try:
                input("Press Enter to continue...") 
                exit(-1)
            except Exception: 
                exit(-1)
        

def computer_move():
    """
    Generates random computer move 

    :return: generated computer move 
    """
    while True :
        random_move = randint(1, 9)
        if random_move in chosen_fields_O or random_move in chosen_fields_X: 
            continue 
        else:
            break 
    
    return random_move


def clear_screen():
    """
    It just clears screen, u know...

    :return: void function
    """
    if os_name() == 'Windows':
        system('cls')
    elif os_name() == 'Linux':
        system('clear')
    elif os_name() == 'Darwin':
        system('clear')

while True:
    dynamic_game_board = list(static_game_board)
    chosen_fields_X = []
    chosen_fields_O = []

    while True:
        clear_screen()
        print(banner)
        print('Game mode (1): player vs player')
        print('Game mode (2): player vs computer')
        game_mode = input('Choose a game mode: ')
        if game_mode not in['1', '2']:
            print('You have to choose game mode (1) or (2)')
            sleep(0.5)
            continue
        else:
            break 

    nick1 = nickname_input('X')

    if game_mode == '1':
        while True: 
            nick2 = nickname_input('O')
            if nick2 == nick1: 
                print("Nicknames can't be the same!")
                sleep(0.5)
                clear_screen()
                continue 
            else:
                break 
    else: 
        nick2 = 'Computer'

    while True:
        clear_screen()
        print(list_to_string(dynamic_game_board))
        print(nick1, end=', ')
        field_number = input('please select a field(X): ')
        choose_field(field_number, 'X')
        if check_win() == 'y': 
            break 
        clear_screen()
        print(list_to_string(dynamic_game_board))
        if game_mode == '1':
            print(nick2, end=', ')
            field_number = input('please select a field(O): ')
            choose_field(field_number, 'O')
        elif game_mode == '2': 
            print("Now it's time for computer move")
            sleep(1)
            choose_field(computer_move(), 'O')
        if check_win() == 'y': 
            break 
