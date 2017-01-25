from panda3d.core import CollisionTraverser
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from terrain import Terrain
from player import Player

import logging
log=logging.getLogger(__name__)

def addLabel(base, text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.06,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))

class Gameplay:

    def __init__(self, base):
        self.base=base
        # hud
        self.label=addLabel(self.base, "?")
        
    def start(self):
        log.info("start...")
        # collisions
        self.base.cTrav=CollisionTraverser()
        self.base.cTrav.showCollisions(self.base.render)
        # meshes
        self.terrain=Terrain(self.base)
        self.player=Player(self.base)
        # camera
        self.base.camera.setPos(1, -39, 1)
        # task
        self.base.taskMgr.add(self.update, "gameplayUpdateTask")
        log.info("started.")
    
    def stop(self):
        log.info("stop...")
        self.base.taskMgr.remove("gameplayUpdateTask")
        self.terrain=None
        log.info("stoped.")

    def update(self, task):
        self.label.setText("Player state:{state:'%s',zoff:%s}. Terrain:{zone:'%s',surfz:%s}\njumpV=%s"%(self.player.state, str(self.player.zOffset), str(self.player.terrainZone), str(self.player.terrainSurfZ), str(self.player.jumpV)))
        return task.cont
