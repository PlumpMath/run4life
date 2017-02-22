from panda3d.core import Vec4, Vec2
from panda3d.core import DirectionalLight, PointLight #AmbientLight,

import logging
log=logging.getLogger(__name__)

class Terrain:

    COLOR_AMB_15=(0.15, 0.15, 0.15, 1)
    COLOR_AMB_30=(0.30, 0.30, 0.30, 1)
    COLOR_AMB_50=(0.50, 0.50, 0.50, 1)
    COLOR_AMB_75=(0.75, 0.75, 0.75, 1)
    COLOR_AMB_90=(0.90, 0.90, 0.90, 1)
    COLOR_SKY=(0.435, 1, 0.915, 1)
    COLOR_WHITE=(1, 1, 1, 1)

    def __init__(self, base):
        self.base=base
        log.info("initializing...")
        # model
        self.model=self.base.loader.loadModel("models/terrain.bam")
        self.model.reparentTo(self.base.render)
        # start position
        self.startPos=self.model.find("**/StartPosition").getPos()
        # sky
        #sky=self.model.find("**/Sky2")
        #skyMaterial=sky.findMaterial("Sky")
        #skyMaterial.setAmbient(Terrain.COLOR_SKY)
        #skyMaterial.setEmission(Terrain.COLOR_AMB_30)
        # lights
        #   ambient
        #alight=AmbientLight("alight")
        #alight.setColor(Vec4(Terrain.COLOR_AMB_50))
        #alightP=self.base.render.attachNewNode(alight)
        #   point
        plight=PointLight("plight")
        plight.setColor(Vec4(Terrain.COLOR_WHITE))
        self.plightP=self.base.render.attachNewNode(plight)
        self.plightP.setPos(14, -30, 17)
        #   directional
        #   sun
        sun=DirectionalLight("sun")
        sun.setColor(Vec4(Terrain.COLOR_WHITE))
        sun.setShadowCaster(True, 1024, 1024)
        sun.getLens().setFilmSize(Vec2(100, 100))
        sun.getLens().setNearFar(10, 200)
        sun.getLens().setFov(200)
        sun.showFrustum()
        sunP=self.base.render.attachNewNode(sun)
        sunP.setPos(0, -2, 20)
        sunP.setHpr(-60, -90, -30)
        #   sky
        sunSky=DirectionalLight("sunSky")
        sunSky.setColor(Vec4(Terrain.COLOR_WHITE))
        sunSkyP=self.base.render.attachNewNode(sunSky)
        sunSkyP.setPos(-14, 30, -17)
        sunSkyP.setHpr(-10, 60, -10)
        #
        #self.base.render.setLight(alightP)
        self.base.render.setLight(sunP)
        self.base.render.setLight(self.plightP)
        #sky.setLightOff()
        #sky.setLight(sunSkyP)
        #
        log.info("done initializing...")
