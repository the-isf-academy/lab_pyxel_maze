import pyxel
import helpers

class Player:
    def __init__(self, img_bank, editX, editY, width, height, scale):
        self.img_bank = img_bank
        self.width = width
        self.height = height
        self.editX = editX
        self.editY = editY
        self.scale = scale

        self.posX = 0
        self.posY = 0
        self.speed = 2
    
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

    def movement(self):
        original_x = self.posX
        original_y = self.posY


        if pyxel.btn(pyxel.KEY_LEFT):
            self.posX -= self.speed

        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.posX += self.speed

        elif pyxel.btn(pyxel.KEY_UP):
            self.posY -= self.speed

        elif pyxel.btn(pyxel.KEY_DOWN):
            self.posY += self.speed

        # prevent it from moving into wall tiles
        if self.is_colliding(self.posX, self.posY, helpers.WALL_TILE):
            self.set_pos(original_x,original_y)

    def is_colliding(self, x, y, tile):
        '''Checks if Player is colliding with a specific tile'''

        # Calculate the tile range based on the sprite's width and height
        x1 = pyxel.floor(x) // 8
        y1 = pyxel.floor(y) // 8
        x2 = pyxel.floor(x + self.width - 1) // 8
        y2 = pyxel.floor(y + self.height - 1) // 8

        # Check for collisions within the tile range
        for tileY in range(y1, y2 + 1):
            for tileX in range(x1, x2 + 1):
                if pyxel.tilemaps[0].pget(tileX, tileY) == tile:
                    return True

        return False
        

    def collides_with(self, other_sprite):
        '''Check is Player collides with another Sprite'''

        return (
            self.posX < other_sprite.posX + other_sprite.width and
            self.posX + self.width > other_sprite.posX and
            self.posY < other_sprite.posY + other_sprite.height and
            self.posY + self.height > other_sprite.posY
        )

       