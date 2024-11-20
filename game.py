from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        self.land.loadLand('land.txt')
        x=10
        y=10
        self.hero = Hero(((x//2), (y//2), 1), self.land)
        base.camLens.setFov(90)
        
game = Game()
game.run()