# import the library
from appJar import gui

ICON_PATH = "appJar/resources/icons/"
PROGRAM_TITLE = "Tic Tac Toe"
# init appJar
APP = gui(PROGRAM_TITLE, "800x600")
APP.addStatusbar(fields=1)
APP.setFont(18)
# GameState keeps track of an individual game
class GameState(object):
    current_player = 0
    tiles = []

    player_imgs = [
        "cancel.png",
        "shape-circle.png"
    ]

    player_symbols = [
        "X",
        "O"
    ]

    game_is_over = False

    def __init__(self):
        for i in range(0, 9):
            self.tiles.append("")
            col = i % 3
            row = i / 3
            APP.addIconButton(str(i), select_tile, "checkbox-empty", row, col)            

    @classmethod
    def get_current_player_symbol(self):
        return self.player_symbols[self.current_player]

    @classmethod
    def get_current_player_icon(self):
        return ICON_PATH + self.player_imgs[self.current_player]

    @classmethod
    def switch_player(self):
        self.current_player = not self.current_player

    @classmethod
    def reset(self):
        self.current_player = 0
        self.tiles = []
        self.game_is_over = False
        for i in range(0, 9):
            self.tiles.append("")
            col = i % 3
            row = i / 3
            APP.addIconButton(str(i), select_tile, "checkbox-empty", row, col)

    @classmethod
    def check_for_winner(self):
        win_conditions = [
            [ # left diag
                self.tiles[0],
                self.tiles[4],
                self.tiles[8]
            ],
            [ # right diag
                self.tiles[2],
                self.tiles[4],
                self.tiles[6]       
            ],
            [ # left col
                self.tiles[0],
                self.tiles[3],
                self.tiles[6]
            ],
            [ # center col
                self.tiles[1],
                self.tiles[4],
                self.tiles[7]
            ],
            [ # right col
                self.tiles[2],
                self.tiles[5],
                self.tiles[8]
            ],
            [ # top row
                self.tiles[0],
                self.tiles[1],
                self.tiles[2]
            ],
            [ # center row
                self.tiles[3],
                self.tiles[4],
                self.tiles[5]
            ],
            [ # bottom row
                self.tiles[6],
                self.tiles[7],
                self.tiles[8]
            ]
        ]

        for condition in win_conditions:
            first_tile = condition[0]
            second_tile = condition[1]
            third_tile = condition[2]  
            all_tiles_equal = first_tile == second_tile == third_tile
            no_blank_tiles = True
            for x in condition:
                if x.strip() == "":
                    no_blank_tiles = False

            if all_tiles_equal and no_blank_tiles:
                GAME_STATE.game_is_over = True
                APP.infoBox("msg", self.get_current_player_symbol() + "'s WIN!")
            
GAME_STATE = GameState

def new_game():
    APP.removeAllWidgets()
    APP.setStatusbar("Current Player: X's")
    GAME_STATE.reset()

def file_menu_handler(menu_item):
    file_handlers = {
        "New Game": new_game
    }

    file_handlers[menu_item]()

APP.addMenuList("File", ["New Game"], file_menu_handler)

def select_tile(button):
    if GAME_STATE.game_is_over:
        APP.warningBox("Game Over", "Game is over. Use File > New Game to start over")
        return

    i = int(button)
    tile_value = GAME_STATE.tiles[i]
    icon_img = GAME_STATE.get_current_player_icon()

    if tile_value == "":
        GAME_STATE.tiles[i] = GAME_STATE.get_current_player_symbol()
        GAME_STATE.check_for_winner()
        APP.setButtonImage(button, icon_img)  
        APP.setStatusbar("Current Player: " + GAME_STATE.get_current_player_symbol() + "'s")

        if GAME_STATE.game_is_over:
            APP.setStatusbar("Game over!")                    
        else:
            GAME_STATE.switch_player()       
    else:
        APP.warningBox("msg", "tile already selected!")  

# press handles main menu button events
def press(button):
    if button == "Cancel":
        APP.stop()
    else:
        new_game()

APP.addButtons(["New Game", "Cancel"], press)

# start the game!
APP.go()
