import random
import pickle #! --NEW--
from hero import Hero
class Mapmanager():
    def __init__(self):
        self.blocks = {}
        textures = [
            'block.png',
            'stone.png',
            'wood.png',
            'brick.png'
        ]
        model = 'block'
        self.createSamples(model, textures)
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.4, 0.35, 1),
            (0.2, 0.2, 0.95, 1),
            (0.4, 0.2, 0.35, 1),
            (0.4, 0.35, 0.2, 1)
        ]
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode('Land')

    def get_ground_height(self, x, y):
        if (x, y) in self.blocks:
            return max([block.getZ()+1 for block in self.blocks[(x, y)]])
        else:
            return 0

    def createSamples(self, model, textures):
        self.samples = list()
        for tname in textures:
            block = loader.loadModel(model)
            block.setTexture(loader.loadTexture(tname))
            self.samples.append(block)

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position, type=0):
        if type >= len(self.samples):
            type = 0
        block = self.samples[type].copyTo(self.land)
        block.setPos(position)
        if type == 0:
            color = self.getColor(int(position[2]))
            block.setColor(color)
        block.setTag("type", str(type))
        block.setTag("at", str(position))
        block.reparentTo(self.land)

        x, y, z = position
        if (x, y) not in self.blocks:
            self.blocks[(x, y)] = []
        self.blocks[(x, y)].append(block)

    def addCol(self, x, y, z):
        for z0 in range(z + 1):
            self.addBlock((x, y, z0))

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            firstline = True
            for l in file:
                if firstline:
                    maxY = int(l)
                    firstline = False
                else:
                    line = map(int, l.split())
                    x = 0
                    for z in line:
                        self.addCol(x, maxY - y, z)
                        x += 1
                    y += 1
        return x, maxY

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos, type):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new, type)

    def delBlock(self, pos):
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()

    def delBlockInFront(self, player_pos, look_direction):
        x, y, z = player_pos
        dx, dy, dz = look_direction
        target_pos = x + dx, y + dy, (z+1) + dz

        blocks = self.findBlocks(target_pos)
        for block in blocks:
            block.removeNode()

    def save_map(self):
        blocks = self.land.getChildren()
        with open("my_save.dat", "wb") as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)
                pickle.dump(int(block.getTag("type")), fout)

    def load_map(self):
        self.clear()
        with open("my_save.dat", "rb") as fin:
            length = pickle.load(fin)
            for _ in range(length):
                pos = pickle.load(fin)
                type = pickle.load(fin)
                self.addBlock(pos, type)
    





