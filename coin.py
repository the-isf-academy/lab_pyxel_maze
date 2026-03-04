import pyxel
import helpers

class Coin:
    def __init__(self, img_bank, editX, editY, width, height, scale):
        self.img_bank = img_bank
        self.width = width
        self.height = height
        self.editX = editX
        self.editY = editY
        self.scale = scale

        self.posX = 0
        self.posY = 0

        self.active = True

    def set_pos(self, x, y):
        '''Set posX,posY position'''

        self.posX = x
        self.posY = y

    def draw(self):
        '''Draw Sprite at current location'''

        pyxel.blt(
            self.posX, 
            self.posY, 
            self.img_bank, 
            self.editX, 
            self.editY, 
            self.width, 
            self.height, 
            colkey=helpers.COLKEY,
            scale = self.scale)

    
    def set_active(self, bool):
        '''Set active'''

        self.active = bool
 




    


