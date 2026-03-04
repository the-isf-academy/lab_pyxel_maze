######################
# a few helpful commands
#   - pyxel edit assets.pyxres (run in Terminal)
#   - press `esc` to quit game 
#   - pyxel.frame_count - returns current frame number 
######################

import pyxel
import helpers
from player import Player
from coin import Coin

class Game:
    def __init__(self):
        self.width = 64*4
        self.height = 64*2

        pyxel.init(self.width, self.height) 

        pyxel.load("assets.pyxres")  # loads sprites and map
        
        self.player = Player(
            img_bank = 0, 
            editX = 24, 
            editY = 0, 
            width = 8, 
            height = 8,
            scale = 1)
        
        self.coin_list = []

        self.scene = "start_screen" # sets the starting scene

        self.setup_map_sprites()

        pyxel.run(self.update, self.draw)

    def setup_map_sprites(self):
        '''Sets up Player and Coin Sprites based on the map'''

        for y in range(pyxel.tilemaps[0].height):
            for x in range(pyxel.tilemaps[0].width):

                tile = pyxel.tilemaps[0].pget(x, y)

                if tile == helpers.PLAYER_TILE:
                    self.player.set_pos(x * 8, y * 8)   

                    for tileY in range(y, y + (self.player.height // 8)):
                        for tileX in range(x, x + (self.player.width // 8)):
                            pyxel.tilemaps[0].pset(tileX, tileY, helpers.TRANSPARENT_TILE)
 
                if tile == helpers.COIN_TILE:

                    coin = Coin(
                        img_bank = 0, 
                        editX = 32, 
                        editY = 0, 
                        width = 8, 
                        height = 8,
                        scale = 0.5)

                    coin.set_pos(x * 8, y * 8)              
                    self.coin_list.append(coin)
                
                    pyxel.tilemaps[0].pset(x, y, helpers.TRANSPARENT_TILE) 

    def draw(self):
        '''Handles what is drawn on the screen'''

        pyxel.cls(0)    # clears screen

        if self.scene == "start_screen":
            self.draw_start_screen()

        elif self.scene == "play_game":
            self.draw_play()

    def draw_map(self, mapX, mapY):
        """Handles how the map is drawn"""

        pyxel.bltm(
            x= mapX, 
            y = mapY, 
            tm = 0, 
            u = 0 , 
            v = 0, 
            w = self.width, 
            h = self.height, 
            colkey=helpers.COLKEY)
    
    def draw_start_screen(self):
        '''Handles what is drawn on the start screen'''

        pyxel.rect(0, 0, self.width, self.height, helpers.BLACK)


        pyxel.text(
            x = self.width//2 - 30, 
            y = self.height//3, 
            s = f"SIMPLE MAZE GAME", 
            col = helpers.WHITE)  
        
        pyxel.text(
            x = self.width//2 - 30,  
            y = self.height//2, 
            s = f"--press enter--", 
            col = helpers.WHITE)

        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = "play_game"

    def draw_play(self):
        '''Handles what is drawn when the game is being played'''

        # draw background color
        pyxel.rect(x=0, y=0, w=self.width, h=self.height, col=helpers.NAVY)
    
        self.draw_map(8, 0)

        self.player.draw()

        for coin in self.coin_list:
            coin.draw()

    def update(self):
        '''Called every frame of the game'''
  
        self.player.movement()

        for coin in self.coin_list:
            if self.player.collides_with(coin) and coin.active == True:
                coin.set_active(False)

Game()




