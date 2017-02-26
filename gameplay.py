from panda3d.core import CollisionTraverser
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from terrain import Terrain
from player import Player
from zorrito import Zorrito

import logging
log=logging.getLogger(__name__)

def addLabel(base, text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.05,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.29), shadow=(0, 0, 0, 1))

class Gameplay:

    MIN_CAM_PLAYER_DISTANCE=5
    MAX_CAM_PLAYER_DISTANCE=10

    def __init__(self, base):
        self.base=base
        # hud
        self.label=addLabel(self.base, "?")
        # camera
        self.cam=self.base.camera
        
    def start(self):
        log.info("start...")
        # collisions
        self.base.cTrav=CollisionTraverser()
        #self.base.cTrav.showCollisions(self.base.render)
        #self.base.messenger.toggleVerbose()
        # objects
        self.terrain=Terrain(self.base)
        self.player=Player(self.base)
        self.player.actor.setPos(self.terrain.startPos)
        self.zorrito=Zorrito(self.base)
        self.zorrito.actor.setPos(self.terrain.zorritoStartPos)
        #
        self.terrain.plightP.reparentTo(self.player.actor)
        self.terrain.plightP.setPos(0, 3, 10)
        # camera
        self.cam.reparentTo(self.player.actor)
        self.cam.setPos(0, 4, 1.5)
        self.cam.lookAt(self.player.camNode)
        # task
        #self.base.taskMgr.add(self.update, "gameplayUpdateTask")
        log.info("started.")
    
    def stop(self):
        log.info("stop...")
        self.base.taskMgr.remove("gameplayUpdateTask")
        self.player.destroy()
        self.terrain.destroy()
        log.info("stoped.")

    def update(self, task):
        #self.label.setText("Player state:{state:'%s',pos:%s,hpr=%s,zoff:%s}.\nTerrain:{zone:'%s',surfz:%s}\nzVelocity=%s\ncollObjs=%s\nkeyState=%s"%(self.player.state, str(self.player.actor.getPos()), str(self.player.actor.getHpr()), str(self.player.zOffset), str(self.player.terrainZone), str(self.player.terrainSurfZ), str(self.player.zVelocity), str(self.player.collidedObjects), str(self.player.keyState)))
        # camera
        camVec=self.cam.getPos()-self.player.actor.getPos()
        camVec.setZ(0)
        camDist=camVec.length()
        camVec.normalize()
        if camDist>Gameplay.MAX_CAM_PLAYER_DISTANCE:
            self.cam.setPos(self.cam.getPos()+camVec*(camDist-Gameplay.MAX_CAM_PLAYER_DISTANCE))
        if camDist<Gameplay.MIN_CAM_PLAYER_DISTANCE:
            self.cam.setPos(self.cam.getPos()-camVec*(Gameplay.MIN_CAM_PLAYER_DISTANCE-camDist))
        camVec.setZ(2)
        self.cam.lookAt(self.player.actor)
        return task.cont
