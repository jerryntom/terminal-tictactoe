from random import randint
from os import system
from platform import system as osName
from time import sleep

staticGameBoard = """\
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
fieldsPositions = {1: [20, 21, 22, 23, 24, 40, 41, 42, 43, 44, 60, 61, 62, 63, 64],
               2: [26, 27, 28, 29, 30, 46, 47, 48, 49, 50, 66, 67, 68, 69, 70],
               3: [32, 33, 34, 35, 36, 52, 53, 54, 55, 56, 72, 73, 74, 75, 76],
               4: [99, 100, 101, 102, 103, 119, 120, 121, 122, 123, 139, 140, 141, 142, 143],
               5: [105, 106, 107, 108, 109, 125, 126, 127, 128, 129, 145, 146, 147, 148, 149],
               6: [111, 112, 113, 114, 115, 131, 132, 133, 134, 135, 151, 152, 153, 154, 155],
               7: [178, 179, 180, 181, 182, 198, 199, 200, 201, 202, 218, 219, 220, 221, 222],
               8: [184, 185, 186, 187, 188, 204, 205, 206, 207, 208, 224, 225, 226, 227, 228],
               9: [190, 191, 192, 193, 194, 210, 211, 212, 213, 214, 230, 231, 232, 233, 234]}

# possible winning fields
winningScenarios = {1: [1, 2, 3],
                     2: [4, 5, 6],
                     3: [7, 8, 9],
                     4: [1, 4, 7],
                     5: [2, 5, 8],
                     6: [3, 6, 9],
                     7: [1, 5, 9],
                     8: [3, 5, 7]}

# data used for visual effect when there is win
crossFieldWin = {1: [40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53, 54, 55, 56],
                     2: [119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135],
                     3: [198, 199, 200, 201, 202, 204, 205, 206, 207, 208, 210, 211, 212, 213, 214],
                     4: [22, 42, 62, 101, 121, 141, 180, 200, 220],
                     5: [28, 48, 68, 107, 127, 147, 186, 206, 226],
                     6: [34, 54, 74, 113, 133, 153, 192, 212, 232],
                     7: [21, 42, 63, 106, 127, 148, 191, 212, 233],
                     8: [35, 54, 73, 108, 127, 146, 181, 200, 219]}


def nicknameInput(playerSymbol):
    """
    Function to make nicknames feature
    better and more accurate

    :param player_symbol: symbol on game board, for example 'X'
    :return: nick
    """
    nick = ''

    while True:
        clearScreen()
        print('Enter nick for player with', playerSymbol)
        nick = input('Enter nick: ') 
        clearScreen()
        if nick == '':
            print("Nickname can't be empty!")
            sleep(0.5)
            clearScreen()
            continue
        elif nick != '':
            clearScreen()
            break

    return nick 


def listToString(listForm):
    """
    Restores game board to string form 

    :return str_data
    """

    strData = ''.join(listForm)
    return strData


def chosenFieldValidation(symbol, dynamicGameBoard, chosenFieldsX, chosenFieldsO, nick):
    """
    Validates chosen field to prevent occurrence of errors and crashing 

    Returns:
        fieldNumber (int): correct fieldNumber 
    """
    while 1:
        while 1:
            try:
                clearScreen()
                print(listToString(dynamicGameBoard))
                print(nick, end=', ')
                fieldNumber = int(input('please select a field({}): '.format(symbol)))

                if fieldNumber not in range(1, 10):
                    print("Can't choose field apart from range 1-9")
                    sleep(0.5)
                    break 
                elif fieldNumber in chosenFieldsX or fieldNumber in chosenFieldsO:
                    print("Can't choose already chosen field")
                    sleep(0.5)
                    break 
            except ValueError:
                print('You have to enter a number')
                sleep(0.5)
                break 
            except Exception as e:
                print('Error occured, wrong input')
                sleep(0.5)
                break 

            return fieldNumber


def chooseField(symbol, dynamicGameBoard, chosenFieldsX, chosenFieldsO, nick):
    """
    Function to handle field selection

    :param number: field number
    :param symbol: by default 'X' or 'O'
    :return: void function
    """
    
    if nick != "computer":
        fieldNumber = chosenFieldValidation(symbol, dynamicGameBoard, chosenFieldsX, chosenFieldsO, nick)
    else:
        print("Time for computer move")
        fieldNumber = computerMove(chosenFieldsX, chosenFieldsO)

    for fields in fieldsPositions[fieldNumber]:
        dynamicGameBoard[fields] = symbol
    if symbol == 'X':
        chosenFieldsX.append(fieldNumber)
    elif symbol == 'O':
        chosenFieldsO.append(fieldNumber)

     
def markWinningFields(positionNumber, dynamicGameBoard):
    """
    Visual help for showing winning position
    on game board

    :param position_number: number of winning position
    :return: void function
    """
    if positionNumber in [1, 2, 3]:
        symbol = '-'
    elif positionNumber in [4, 5, 6]:
        symbol = '|'
    elif positionNumber == 7:
        symbol = "\\"
    else:
        symbol = '/'

    for data in crossFieldWin[positionNumber]:
        dynamicGameBoard[data] = symbol


def checkWin(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2):
    """
    Checks if one of the sides already won
    or if there is tie

    :return: decision
    """
    decision = -2
    position = 0
    set_fields_x = set(chosenFieldsX)
    set_fields_o = set(chosenFieldsO)

    for i in range(1, 9):
        set_positions = set(winningScenarios[i])
        position += 1
        if set_positions.intersection(set_fields_x) == set_positions:
            decision = -1
            break
        elif set_positions.intersection(set_fields_o) == set_positions:
            decision = 1
            break
        elif len(chosenFieldsX) + len(chosenFieldsO) == 9:
            decision = 0
            break 

    if decision == -1:
        clearScreen()
        markWinningFields(position, dynamicGameBoard)
        print(listToString(dynamicGameBoard))
        print(nick1, 'won!!!')
    elif decision == 1:
        clearScreen()
        markWinningFields(position, dynamicGameBoard)
        print(listToString(dynamicGameBoard))
        print(nick2, 'won!!!')
    elif decision == 0 and len(chosenFieldsX) + len(chosenFieldsO) == 9:
        clearScreen()
        print(listToString(dynamicGameBoard))
        print('Tie!!!')
    
    if decision in [-1, 0, 1]:
        while 1:
            while 1:
                final_choice = input(("What's next? (p)lay again\\(m)enu\\(e)xit: "))

                if final_choice == 'p':
                    dynamicGameBoard = list(staticGameBoard)
                    chosenFieldsX = []
                    chosenFieldsO = []
                    gameplay(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2)
                elif final_choice == 'm': 
                    start()
                elif final_choice == 'e':
                    exit()
                else:
                    print("Wrong choice! Choose again!")
                    sleep(1)
                    clearScreen()
                    break 
            
        
def computerMove(chosenFieldsX, chosenFieldsO):
    """
    Generates random computer move 

    :return: generated computer move 
    """
    while True :
        random_move = randint(1, 9)
        if random_move in chosenFieldsX or random_move in chosenFieldsO: 
            continue 
        else:
            break 
    
    return random_move


def clearScreen():
    """
    It just clears screen, u know...

    :return: void function
    """
    if osName() == 'Windows':
        system('cls')
    elif osName() == 'Linux':
        system('clear')
    elif osName() == 'Darwin':
        system('clear')


def start():
    """
    Game beginning handler.

    - menu 
    - data input

    return: None 
    """
    dynamicGameBoard = list(staticGameBoard)
    chosenFieldsX = []
    chosenFieldsO = []

    while 1:
        clearScreen()
        print(banner)
        print('Game mode (1): player vs player')
        print('Game mode (2): player vs computer')
        gameMode = input('Choose a game mode: ')
        if gameMode not in['1', '2']:
            print('You have to choose game mode (1) or (2)')
            sleep(0.5)
            continue
        else:
            break 
    nick1 = nicknameInput('X')
    if gameMode == '1':
        while 1: 
            nick2 = nicknameInput('O')
            if nick2 == nick1: 
                print("Nicknames can't be the same!")
                sleep(0.5)
                clearScreen()
                continue 
            else:
                break 
    else: 
        nick2 = 'Computer'
    
    gameplay(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2)
    

def gameplay(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2):
    """
    Game logic helper, processes all actions.
    Transmits certain things to certain functions.
    
    return: None 
    """

    while 1:
        clearScreen()
        print(listToString(dynamicGameBoard))
        chooseField('X', dynamicGameBoard, chosenFieldsX, chosenFieldsO, nick1)
        checkWin(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2)
        clearScreen()
        print(listToString(dynamicGameBoard))
        if gameMode == '1':
            chooseField('O', dynamicGameBoard, chosenFieldsX, chosenFieldsO, nick2)
        elif gameMode == '2': 
            print("Now it's time for computer move")
            sleep(1)
            chooseField('O', dynamicGameBoard, chosenFieldsX, chosenFieldsO, "computer")
        checkWin(dynamicGameBoard, chosenFieldsX, chosenFieldsO, gameMode, nick1, nick2)


if __name__ == "__main__":
    start()
