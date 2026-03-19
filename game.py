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
from powerup import Powerup

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
        self.powerup_list = []

        self.y_offset = 0 # use this to draw multiple levels or stages

        self.score = 0

        self.scene = "start_screen" # sets the starting scene

        self.setup_map_sprites()

        pyxel.run(self.update, self.draw)

    def setup_map_sprites(self):
        '''Sets up Player and Coin Sprites based on the map'''

        for y in range(self.y_offset, self.y_offset + self.height//8):
            for x in range(self.width//8):

                tile = pyxel.tilemaps[0].pget(x, y)

                screen_y = (y - self.y_offset) * 8 # STAGE TWO LOGIC

                if tile == helpers.PLAYER_TILE:
                    self.player.set_pos(x * 8, screen_y) # STAGE TWO LOGIC

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

                    coin.set_pos(x * 8, screen_y) # STAGE TWO LOGIC         
                    self.coin_list.append(coin)
                
                    pyxel.tilemaps[0].pset(x, y, helpers.TRANSPARENT_TILE) 

                if tile == helpers.POWERUP_TILE:

                    powerup = Powerup(
                        img_bank = 0, 
                        editX = 16, 
                        editY = 0, 
                        width = 8, 
                        height = 8,
                        scale = 0.5)

                    powerup.set_pos(x * 8, screen_y)              
                    self.powerup_list.append(powerup)
                
                    pyxel.tilemaps[0].pset(x, y, helpers.TRANSPARENT_TILE) 

    def draw(self):
        '''Handles what is drawn on the screen'''

        pyxel.cls(0)    # clears screen

        if self.scene == "start_screen":
            self.draw_start_screen()

        elif self.scene == "play_game":
            self.draw_play()
    
        elif self.scene == "end_screen":
            self.draw_end_screen()

    def draw_map(self, mapX, mapY):
        """Handles how the map is drawn"""
        """mapX represents the x coordinate from the map editor"""
        """mapY represents the y coordinate from the map editor"""

        pyxel.bltm(
            x= 0, 
            y = 0, 
            tm = 0, 
            u = mapX*8, 
            v = mapY*8, 
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
    
        self.draw_map(0, self.y_offset) # STAGE TWO LOGIC

        self.player.draw()

        for coin in self.coin_list:
            coin.draw()

        for powerup in self.powerup_list:
            powerup.draw()
    
    def draw_end_screen(self):
        '''Handles what is drawn on the start screen'''

        pyxel.rect(0, 0, self.width, self.height, helpers.BLACK)

        pyxel.text(
            x = self.width//2 - 30, 
            y = self.height//3, 
            s = f"GAME OVER", 
            col = helpers.WHITE)  

    def change_stage(self): # STAGE TWO LOGIC
        self.player.set_pos(8,8)
        self.coin_list = []
        self.powerup_list = []
        self.setup_map_sprites()

    def update(self):
        '''Called every frame of the game'''
  
        self.player.movement(self.y_offset)

        for coin in self.coin_list:
            if self.player.collides_with(coin) and coin.active == True:
                coin.set_active(False)
                self.score += 1
                print(self.score)
        
        for powerup in self.powerup_list:
            if self.player.collides_with(powerup) and powerup.active == True:
                powerup.set_active(False)
                self.score += 3
                print(self.score)

        if self.score == 9 and self.y_offset == 0: # STAGE TWO LOGIC
            self.y_offset = 16
            self.change_stage()

        if self.score == 11:
            self.scene = "end_screen"
        

Game()




