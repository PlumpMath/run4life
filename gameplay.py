from panda3d.core import CollisionTraverser
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from terrain import Terrain
from player import Player
from zorrito import Zorrito
import random

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
        #
        self.placeZorritos()
        #
        self.terrain.plightP.reparentTo(self.player.actor)
        self.terrain.plightP.setPos(0, 3, 10)
        # camera
        self.cam.reparentTo(self.player.actor)
        self.cam.setPos(0, 4, 2)
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
        # zorritos
        for zorrito in self.terrain.zorritos:
            vec=self.player.actor.getPos()-zorrito.actor.getPos()
            zorrito.setDistanceToPlayer(vec.length())
        return task.cont

    def placeZorritos(self):
        self.zorritos=[]
        cantZorritos=int(len(self.terrain.zorritoStartPosList)/2)
        zorritosPosList=random.sample(self.terrain.zorritoStartPosList, cantZorritos)
        log.debug("placeZorritos:\n\t%(list)s"%{"list":str(self.terrain.zorritoStartPosList)})
        for zorritoPos in zorritosPosList:
            zorrito=Zorrito(self.base, self.player)
            zorrito.actor.setPos(zorritoPos)
            log.debug("zorrito pos is %s"%str(zorritoPos))
            self.zorritos.append(zorrito)
        
