from panda3d.core import CollideMask, CollisionNode, CollisionRay, CollisionHandlerQueue
from direct.actor.Actor import Actor
from panda3d.ai import *
import random

import logging
log=logging.getLogger(__name__)

class Zorrito:
    
    STATE_IDLE="Idle"
    STATE_WANDER="Wander"
    STATE_PURSUIT="Pursuit"
    
    PURSUIT_DISTANCE=8
    
    def __init__(self, base, player):
        self.base=base
        self.player=player
        # actor
        self.actor=Actor("models/zorrito")
        self.actor.reparentTo(self.base.render)
        self.actor.setScale(0.15)
        # collision
        #   ray
        collRay=CollisionRay(0, 0, 1.5, 0, 0, -1)
        collRayN=CollisionNode("playerCollRay")
        collRayN.addSolid(collRay)
        collRayN.setFromCollideMask(1)
        collRayN.setIntoCollideMask(CollideMask.allOff())
        #collRayNP=self.actor.attachNewNode(collRayN)
        self.collQRay=CollisionHandlerQueue()
        #self.base.cTrav.addCollider(collRayNP, self.collQRay)
        # ai
        self.aiWorld=AIWorld(self.base.render)
        self.aiChar=AICharacter("aiZorrito", self.actor, 150, 0.05, 6)
        self.aiWorld.addAiChar(self.aiChar)
        self.aiBehaviors=self.aiChar.getAiBehaviors()
        self.aiBehaviors.initPathFind("models/navmesh.csv")
        # state
        self.distanceToPlayer=1000
        self.zOffset=0
        self.terrainSurfZ=0
        self.state=Zorrito.STATE_IDLE
        self.currentStateTimeout=4+6*random.random()
        # uptade task
        self.base.taskMgr.add(self.update, "zorritoUpdateTask")
    
    def processTerrainRelation(self): # -> [terrainSurfZ, zOffset]
        collEntries=self.collQRay.getEntries()
        #
        if len(collEntries)==0:
            #log.error("out of terrain, pos=%s"%str(self.actor.getPos()))
            return 0, 0
        #
        gndZ=-1000
        for entry in collEntries:
            eName=entry.getIntoNodePath().getName()
            eZ=entry.getSurfacePoint(self.base.render).getZ()
            if eName.startswith("Ground"):
                if eZ>gndZ:
                    gndZ=eZ
        zOffset=self.actor.getZ()-gndZ
        return gndZ, zOffset
    
    def defineState(self):
        #
        newState=self.state
        # from Idle,Wander -> Idle,Wander,Pursuit
        if self.state==Zorrito.STATE_IDLE or self.state==Zorrito.STATE_WANDER:
            if self.distanceToPlayer<=Zorrito.PURSUIT_DISTANCE:
                newState=Zorrito.STATE_PURSUIT
                self.currentStateTimeout=0
            else:
                if self.currentStateTimeout==0:
                    newState, self.currentStateTimeout=self.newRandomState((Zorrito.STATE_IDLE, Zorrito.STATE_WANDER))
        elif self.state==Zorrito.STATE_PURSUIT:
            if self.aiBehaviors.behaviorStatus("pathfollow")=="done" or  self.distanceToPlayer>Zorrito.PURSUIT_DISTANCE:
                newState=Zorrito.STATE_IDLE
        return newState

    def processState(self, dt):
        # terrain sdjustment
        if self.zOffset!=0:
            self.actor.setZ(self.terrainSurfZ)

    def onStateChanged(self, newState):
        curState=self.state
        self.aiBehaviors.removeAi("all")
        if newState==Zorrito.STATE_WANDER:
            self.aiBehaviors.wander(5, 0, 10, 1)
        elif newState==Zorrito.STATE_PURSUIT:
            status=self.aiBehaviors.behaviorStatus("pathfollow")
            if status!="done" and status!="active":
                self.aiBehaviors.pathFindTo(self.player.actor)
        log.debug("state change %s -> %s"%(str(curState), str(newState)))
        
    def newRandomState(self, states): # -> (new state, timeout)
        newState=random.choice(states)
        timeout=4+6*random.random()
        return (newState, timeout)

    def update(self, task):
        # clock
        dt=self.base.taskMgr.globalClock.getDt()
        if self.currentStateTimeout>0:
            self.currentStateTimeout-=dt
        elif self.currentStateTimeout<0:
            self.currentStateTimeout=0
        # update vars
         # terrain relation
        self.terrainSurfZ, self.zOffset=self.processTerrainRelation()
         # distance to player
        diffVec=self.player.actor.getPos()-self.actor.getPos()
        diffVec.setZ(0)
        self.distanceToPlayer=diffVec.length()
        # state
        newState=self.defineState()
        if self.state!=newState:
            self.onStateChanged(newState)
            self.state=newState
        self.processState(dt)
        # ai
        self.aiWorld.update()
        return task.cont
            
