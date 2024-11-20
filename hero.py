key_turn_left = "q"
key_turn_right = "e"
key_turn_up = "wheel_up"
key_turn_down = "wheel_down"
key_forward = "w"
key_back = "s"
key_left = "a"
key_right = "d"
switch_camera = "c"
switch_mode = "x"

key_up = "shift"
key_down = "control"
key_jump = "space"

key_build = "mouse3"
key_destroy = "mouse1"

key_save = "f5"
key_load = "f6"

key_btype_0 = "1"
key_btype_1 = "2"
key_btype_2 = "3"
key_btype_3 = "4"

class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.btype = 0
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()
        self.grounded = True


        self.is_jumping = False
        self.jump_height = 2
        self.jump_speed = 0.5
        self.gravity = -0.1
        self.vertical_speed = 0

        taskMgr.add(self.update, "update")

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vertical_speed = self.jump_speed

    def update(self, task):
        x, y, z = self.hero.getPos()

        if self.is_jumping:
            z += self.vertical_speed
            self.vertical_speed += self.gravity

            if self.is_on_ground(z):
                z = self.get_ground_level(x, y)
                self.is_jumping = False
                self.vertical_speed = 0

        self.hero.setPos(x, y, z)
        return task.cont

    def is_on_ground(self, z):
        x, y = self.hero.getX(), self.hero.getY()
        ground_level = self.get_ground_level(x, y)
        return z <= ground_level

    def get_ground_level(self, x, y):
        z = self.land.get_ground_height(x, y)
        return z 

    def accept_events(self):
        base.accept(key_up, self.jump)

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,3)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
        
    def changeViev(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def turn_left(self):
        self.hero.setH((self.hero.getH()+5)%360)

    def turn_right(self):
        self.hero.setH((self.hero.getH()-5)%360)

    def turn_up(self):
        if self.hero.getP()>270 or self.hero.getP()<=90:
            self.hero.setP((self.hero.getP()-5)%360)

    def turn_down(self):
        if self.hero.getP()<90 or self.hero.getP()>=270:
            self.hero.setP((self.hero.getP()+5)%360)
        
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def check_dir(self, angle):
        if angle >= 0 and angle <=20:
            return (0,-1)
        elif angle <=65:
            return (1,-1)
        elif angle <=110:
            return (1,0)
        elif angle <=155:
            return (1,1)
        elif angle <=200:
            return (0,1)
        elif angle <=245:
            return (-1,1)
        elif angle <=290:
            return (-1,0)
        elif angle <=335:
            return (-1,-1)
        else:
            return (0,-1)

    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH()+180) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH()+270) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH()+90) % 360
        self.move_to(angle)

    def change_mode(self):
        if self.mode:
            self.mode = False
            if self.hero.getZ() >= 2:
                x, y = self.hero.getX(), self.hero.getY()
                ground_level = self.get_ground_level(x, y)
                while self.hero.getZ() > ground_level:
                    self.hero.setZ(self.hero.getZ() - 1)
        else:
            self.mode = True

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2]
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)
    def down(self):
        if self.mode and self.hero.getZ() > 2:
            self.hero.setZ(self.hero.getZ()-1)
            
    def build(self):
        angle = self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos, type = self.btype)
        else:
            self.land.buildBlock(pos, type = self.btype)

    def setBuild(self, type):
        self.btype = type
    
    def destroy(self):
        angle = self.hero.getH()%360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)

    def accept_events(self):
        base.accept(key_jump, self.jump)
        base.accept(switch_mode, self.change_mode)
        base.accept(key_up, self.up)
        base.accept(key_up + '-repeat', self.up)
        base.accept(key_down, self.down)
        base.accept(key_down + '-repeat', self.down)
        
        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)
        base.accept(key_turn_up, self.turn_up)
        base.accept(key_turn_up + '-repeat', self.turn_up)
        base.accept(key_turn_down, self.turn_down)
        base.accept(key_turn_down + '-repeat', self.turn_down)

        base.accept(key_forward, self.forward)
        base.accept(key_forward+'-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back+'-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left+'-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right+'-repeat', self.right)
        
        base.accept(switch_camera, self.changeViev)
        
        base.accept(key_save, self.land.save_map)
        base.accept(key_load, self.land.load_map)
        
        base.accept(key_build, self.build)
        base.accept(key_btype_0, self.setBuild, [0])
        base.accept(key_btype_1, self.setBuild, [1])
        base.accept(key_btype_2, self.setBuild, [2])
        base.accept(key_btype_3, self.setBuild, [3])

        base.accept(key_destroy, self.destroy)