from panda3d.core import Vec2, Vec4
from panda3d.core import DirectionalLight, PointLight #AmbientLight,
from panda3d.core import CollisionNode, CollisionSphere, CollideMask, CollisionTube

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
        #sky=self.model.find("**/Sky")
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
        plightP=self.base.render.attachNewNode(plight)
        plightP.setPos(14, -30, 17)
        #   directional
        sun=DirectionalLight("sun")
        sun.setColor(Vec4(Terrain.COLOR_WHITE))
        #sun.setShadowCaster(True, 512, 512)
        sun.getLens().setFilmSize(Vec2(30, 30))
        sun.getLens().setNearFar(10, 100)
        sun.getLens().setFov(100)
        sun.showFrustum()
        sunP=self.base.render.attachNewNode(sun)
        sunP.setPos(14, -30, 17)
        sunP.setHpr(10, -60, 10)
        #
        #self.base.render.setLight(alightP)
        self.base.render.setLight(sunP)
        self.base.render.setLight(plightP)
        # collision objects
        self.createCollisionObjects()
        #
        log.info("done initializing...")
    
    def createCollisionObjects(self):
        log.info("creating collision objects...")
        objects=list()
        self.gatherCollidableObjects(self.model, objects)
        log.info("gathered %i objects for collision"%len(objects))
        for object in objects:
            name=object.getName()
            log.debug("- setting collision mesh to object %s..."%name)
            collSolid=None
            if name.startswith("Tree."):
                collSolid=CollisionTube(0, 0, 0, 0, 0, 1, 1)
            elif name.startswith("Rock."):
                collSolid=CollisionSphere(0, 0, 0.85, 1)
            collSphereN=CollisionNode("%s.CollNode"%name)
            collSphereN.addSolid(collSolid)
            collSphereN.setFromCollideMask(CollideMask.allOff())
            collSphereN.setIntoCollideMask(2)
            #collSphereNP=
            object.attachNewNode(collSphereN)
            #collSphereNP.show()

    def gatherCollidableObjects(self, parent, objectList):
        for child in parent.getChildren():
            name=child.getName()
            if name.startswith("Tree.") or name.startswith("Rock.Big."):
                objectList.append(child)
            self.gatherCollidableObjects(child, objectList)
