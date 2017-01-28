from panda3d.core import Vec2, Vec4
from panda3d.core import AmbientLight, DirectionalLight

import logging
log=logging.getLogger(__name__)

class Terrain:

    def __init__(self, base):
        self.base=base
        # model
        self.model=self.base.loader.loadModel("models/terrain")
        self.model.reparentTo(self.base.render)
        # lights
        #   ambient
        alight=AmbientLight("alight")
        alight.setColor(Vec4(0.3, 0.3, 0.3, 1))
        alightP=self.base.render.attachNewNode(alight)
        self.base.render.setLight(alightP)
        #   directional
        sun=DirectionalLight("sun")
        sun.setColor(Vec4(1, 0.973, 0.691, 1))
        #sun.setShadowCaster(True, 4096, 4096)
        sun.getLens().setFilmSize(Vec2(30, 30))
        sun.getLens().setNearFar(10, 100)
        sun.getLens().setFov(100)
        sunP=self.base.render.attachNewNode(sun)
        sunP.setHpr(10, -60, 10)
        self.base.render.setLight(sunP)
