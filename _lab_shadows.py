from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        #
        self.disableMouse()
        self.render.setShaderAuto()
        #
        gameplay=Gameplay(self)
        gameplay.start()

class Gameplay:
    
    def __init__(self, base):
        self.base=base
        
    def start(self):
        # meshes
        self.terrain=Terrain(self.base)
        self.player=Player(self.base)
        # camera
        #self.base.camera.setPos(1, -39, 1)
        self.base.camera.setPos(0, -5, 1)
    
    def stop(self):
        self.terrain=None

from panda3d.core import Vec2, Vec4
from panda3d.core import AmbientLight, DirectionalLight

class Terrain:

    def __init__(self, base):
        self.base=base
        # model
        self.model=self.base.loader.loadModel("models/terrain")
        self.model.reparentTo(self.base.render)
        # lights
        #   ambient
        alight=AmbientLight("alight")
        alight.setColor(Vec4(0.4, 0.4, 0.4, 1))
        alightP=self.base.render.attachNewNode(alight)
        self.base.render.setLight(alightP)
        #   directional
        sun=DirectionalLight("sun")
        sun.setColor(Vec4(1, 0.973, 0.491, 1))
        sun.setShadowCaster(True, 4096, 4096)
        sun.getLens().setFilmSize(Vec2(30, 30))
        sun.getLens().setNearFar(10, 100)
        sun.getLens().setFov(100)
        sunP=self.base.render.attachNewNode(sun)
        sunP.setHpr(10, -60, 10)
        self.base.render.setLight(sunP)

class Player:
    
        def __init__(self, base):
            self.base=base
            #
            self.model=self.base.loader.loadModel("models/player")
            self.model.reparentTo(self.base.render)
            #self.model.setPos(0, -31.1, 0.2)
            
if __name__=="__main__":
    g=Game()
    g.run()
