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

# used to manipulate static game board
dynamic_game_board = list(static_game_board)

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
cross_fields_data = {1: [40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53, 54, 55, 57],
                     2: [119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135],
                     3: [198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 210, 211, 212, 213, 214],
                     4: [22, 42, 62, 101, 121, 141, 180, 200, 220],
                     5: [28, 48, 68, 107, 127, 147, 186, 206, 226],
                     6: [34, 54, 74, 113, 133, 153, 192, 212, 232],
                     7: [21, 42, 63, 106, 127, 148, 191, 212, 233],
                     8: [35, 54, 73, 108, 127, 146, 181, 200, 219]}


choosen_fields_X = []
chosen_fields_O = []

nick1 = ''
nick2 = ''


def nickname_input(nick, player_symbol):
    """
    Function to make nicknames feature
    better and more accurate

    :param nick: player nickname
    :param player_symbol: symbol on game board, for example 'X'
    :return: nick
    """
    nick = ''
    i = 0

    while True:
        clear_screen()
        print('Enter nick for player with', player_symbol)
        nick = input('Enter nick: ') 
        clear_screen()
        if nick == '' and i != 0: 
            print("Nickname can't be empty")
            sleep(0.5)
            clear_screen()
            continue
        elif nick != '':
            clear_screen()
            break
        i += 1

    return nick + ','

def list_to_string(_list):
    """
    Convert any string converted
    to list back to string easily :)

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

    while type(number) != int or number not in range(1, 10):
        try:
            number = int(number)
            for fields in fields_data[number]:
                dynamic_game_board[fields] = symbol
            if symbol == 'X':
                choosen_fields_X.append(number)
            elif symbol == 'O':
                chosen_fields_O.append(number)
        except ValueError:
            print('You have to enter a number!')
            sleep(0.5)
            clear_screen()
            print(list_to_string(dynamic_game_board))
            number = input('Select a field({}): '.format(symbol))
        except KeyError:
            print('You have to enter a number in range from 1 to 9')
            sleep(0.5)
            clear_screen()
            print(list_to_string(dynamic_game_board))
            number = input('Select a field({}): '.format(symbol))


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

    :return:void function
    """
    decision = 0
    position = 0
    set_fields_x = set(choosen_fields_X)
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

    if decision == -1:
        clear_screen()
        cross_winning_fields(position)
        print(list_to_string(dynamic_game_board))
        print(nick1, 'won!!!')
        input('\nPress Enter to continue...')
        exit(-1)
    elif decision == 1:
        clear_screen()
        cross_winning_fields(position)
        print(list_to_string(dynamic_game_board))
        print(nick2, 'won!!!')
        input('\nPress Enter to continue...')
        exit(-1)
    elif decision == 0 and len(choosen_fields_X) + len(chosen_fields_O) == 9:
        clear_screen()
        print(list_to_string(dynamic_game_board))
        print('Tie!!!')
        input('\nPress Enter to continue...')
        exit(-1)


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

clear_screen()

nick1 = nickname_input(nick1, 'X')
nick2 = nickname_input(nick2, 'O')

while True:
    clear_screen()
    print(list_to_string(dynamic_game_board))
    print(nick1, end=' ')
    field_number = input('please select a field(X): ')
    choose_field(field_number, symbol='X')
    check_win()
    clear_screen()
    print(list_to_string(dynamic_game_board))
    print(nick2, end=' ')
    field_number = input('please select a field(O): ')
    choose_field(field_number, symbol='O')
    check_win()
    clear_screen()
