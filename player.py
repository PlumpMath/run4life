from panda3d.core import CollideMask, CollisionNode, CollisionRay, CollisionHandlerQueue
from direct.actor.Actor import Actor
import math

import logging
log=logging.getLogger(__name__)

class Player:

        STATE_IDLE="Idle"
        STATE_WALK="Walk"
        STATE_RUN="Walk"
        STATE_JUMP="Jump"
        STATE_FALL="Fall"
        
        JUMP_HEIGHT=2
        JUMP_A=-45
    
        TERRAIN_NONE=0
        TERRAIN_GROUND=1
        TERRAIN_WATER=2
        TERRAIN_AIR=3
    
        def __init__(self, base):
            self.base=base
            self.keyState={
                "WalkFw":False, 
                "WalkBw":False, 
                "Run":False, 
                "RotateL":False, 
                "RotateR":False, 
                "Jump":False
                }
            self.state=Player.STATE_IDLE
            self.walkDir=0
            self.rotationDir=0
            self.jumpV=0
            self.zOffset=None
            self.terrainZone=None
            self.terrainSurfZ=None
            # actor
            self.actor=Actor("models/player")
            self.actor.reparentTo(self.base.render)
            self.actor.setPos(0, -31.1, 0.2)
            # collision
            #   ray
            collRay=CollisionRay(0, 0, 1, 0, 0, -1)
            collRayN=CollisionNode("playerCollRay")
            collRayN.addSolid(collRay)
            collRayN.setFromCollideMask(1)
            collRayN.setIntoCollideMask(CollideMask.allOff())
            collRayNP=self.actor.attachNewNode(collRayN)
            collRayNP.show()
            self.collQRay=CollisionHandlerQueue()
            self.base.cTrav.addCollider(collRayNP, self.collQRay)
            # keys
            self.actor.accept("shift", self.setKeyState, ["Run", True])
            self.actor.accept("arrow_up", self.setKeyState, ["WalkFw", True])
            self.actor.accept("arrow_up-up", self.setKeyState, ["WalkFw", False])
            self.actor.accept("arrow_down", self.setKeyState, ["WalkBw", True])
            self.actor.accept("arrow_down-up", self.setKeyState, ["WalkBw", False])
            self.actor.accept("arrow_left", self.setKeyState, ["RotateL", True])
            self.actor.accept("arrow_left-up", self.setKeyState, ["RotateL", False])
            self.actor.accept("arrow_right", self.setKeyState, ["RotateR", True])
            self.actor.accept("arrow_right-up", self.setKeyState, ["RotateR", False])
            self.actor.accept("j", self.setKeyState, ["Jump", True])
            self.actor.accept("j-up", self.setKeyState, ["Jump", False])
            # task
            self.base.taskMgr.add(self.update, "playerUpdateTask")
        
        def setKeyState(self, key, state):
            log.debug("%s->%s"%(key, str(state)))
            self.keyState[key]=state
        
        def defineState(self):
            # keys states
            ks=self.keyState
            # from Idle -> Walk, Jump
            if self.state==Player.STATE_IDLE:
                # Walk
                if ks["WalkFw"] or ks["WalkBw"] or ks["RotateL"] or ks["RotateR"]:
                    if ks["Run"]:
                        self.state=Player.STATE_RUN
                    else:
                        self.state=Player.STATE_WALK
                    log.debug("new state: %s"%str(self.state))
                elif ks["Jump"]:
                    self.state=Player.STATE_JUMP
                    log.debug("new state: %s"%str(self.state))
            # from Walk -> Idle
            elif self.state==Player.STATE_WALK or self.state==Player.STATE_RUN:
                if ks["WalkFw"]:
                    self.walkDir=-1
                elif ks["WalkBw"]:
                    self.walkDir=1
                elif not ks["WalkFw"] and not ks["WalkBw"]:
                    self.walkDir=0
                if ks["RotateL"]:
                    self.rotationDir=1
                elif ks["RotateR"]:
                    self.rotationDir=-1
                elif not ks["RotateL"] and not ks["RotateR"]:
                    self.rotationDir=0
                if self.walkDir==0 and self.rotationDir==0:
                    self.state=Player.STATE_IDLE
                    log.debug("new state: %s"%str(self.state))
            # from Jump -> Fall
            elif self.state==Player.STATE_JUMP:
                self.state=Player.STATE_FALL
                log.debug("new state: %s"%str(self.state))
                # calculate initial jump "velocity"; for mass=1, jump height=JUMP_HEIGHT, a=JUMP_A; Ec=>Ep=mgh
                Ec=abs(1*Player.JUMP_A*Player.JUMP_HEIGHT)
                self.jumpV=math.sqrt(2*Ec/1)
                log.debug("jump Ec=%f V=%f"%(Ec, self.jumpV))
            # from Fall -> Idle
            elif self.state==Player.STATE_FALL:
                if self.zOffset<=0:
                    self.state=Player.STATE_IDLE
                    log.debug("new state: %s"%str(self.state))
                    self.jumpV=0
                    self.actor.setZ(self.terrainSurfZ)
        
        def processTerrainRelation(self): # -> [terrainZone, terrainSurfZ, zOffset]
            collEntries=self.collQRay.getEntries()
            if len(collEntries)==0:
                log.error("out of terrain, pos=%s"%str(self.actor.getPos()))
                if self.terrainZone!=Player.TERRAIN_NONE:
                    self.terrainZone=Player.TERRAIN_NONE
                    self.onTerrainZoneChanged(Player.TERRAIN_NONE)
                    return Player.TERRAIN_NONE, 0, 0
            maxZ=0
            for entry in collEntries:
                entryZ=entry.getSurfacePoint(self.base.render).getZ()
                if entryZ>maxZ: maxZ=entryZ
            terrainSurfZ=maxZ
            zOffset=self.actor.getZ()-self.terrainSurfZ
            entryName=entry.getIntoNodePath().getName()
            #log.debug("ray collision entry name: %s"%entryName)
            newZone=None
            if entryName=="Ground":
                newZone=Player.TERRAIN_GROUND
            elif entryName.startswith("Water"):
                newZone=Player.TERRAIN_WATER
            return newZone, terrainSurfZ, zOffset
        
        def onTerrainZoneChanged(self, zone):
            log.debug("terrain zone chaged to: %i"%self.terrainZone)
        
        def update(self, task):
            # clock
            dt=self.base.taskMgr.globalClock.getDt()
            # terrain relation
            newZone, self.terrainSurfZ, self.zOffset=self.processTerrainRelation()
            if newZone!=self.terrainZone:
                self.terrainZone=newZone
                self.onTerrainZoneChanged(self.terrainZone)
            if self.zOffset>0.5 and self.state!=Player.STATE_FALL:
                self.state=Player.STATE_FALL
                log.debug("new state: %s"%str(self.state))
            else:
                self.actor.setZ(self.terrainSurfZ)
            # state
            self.defineState()
            # walk
            if self.walkDir!=0:
                speed=0.6 if self.state==Player.STATE_RUN else 0.3
                self.actor.setY(self.actor, speed*self.walkDir*dt)
            if self.rotationDir!=0:
                self.actor.setH(self.actor.getH()+15*self.rotationDir)
            # jump
            if self.state==Player.STATE_FALL:
                dZ=self.jumpV*dt
                newZ=self.actor.getZ()+dZ
                if newZ<self.terrainSurfZ: newZ=self.terrainSurfZ
                self.actor.setZ(newZ)
                self.jumpV+=Player.JUMP_A*dt
                log.debug("jumping... h=%f, dZ=%f, v=%f, dt=%f"%(self.zOffset, dZ, self.jumpV, dt))
            return task.cont
