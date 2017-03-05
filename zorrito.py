from direct.actor.Actor import Actor
from panda3d.ai import *

import logging
log=logging.getLogger(__name__)

class Zorrito:
    
    def __init__(self, base):
        self.base=base
        #
        self.actor=Actor("models/zorrito")
        self.actor.reparentTo(self.base.render)
        self.actor.setScale(0.15)
        #
        self.setUpAI()
    
    def setUpAI(self):
        self.aiWorld=AIWorld(self.base.render)
        self.aiChar=AICharacter("aiZorrito", self.actor, 100, 0.05, 6)
        self.aiWorld.addAiChar(self.aiChar)
        self.aiBehaviors=self.aiChar.getAiBehaviors()
        
    def startAI(self, player):
        log.debug("initializing path finding...")
        self.aiBehaviors.initPathFind("navmesh.csv")
        log.debug("starting pathFindTo...")
        self.aiBehaviors.pathFindTo(player, "addPath")
        log.debug("adding ai task...")
        self.base.taskMgr.add(self.updateAI, "updateAI")
    
    def updateAI(self, task):
        self.aiWorld.update()
        return task.cont
        
