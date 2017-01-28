from panda3d.core import CollideMask, CollisionNode, CollisionRay, CollisionSphere, CollisionHandlerQueue
from direct.actor.Actor import Actor

import logging
log=logging.getLogger(__name__)

class Player:

        STATE_IDLE="Idle"
        STATE_WALK="Walk"
        STATE_RUN="Walk"
        STATE_JUMP="Jump"
        STATE_FALL="Fall"
        
        JUMP_ACCEL=63
        FALL_ACCEL=-9.81
    
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
            self.zVelocity=0
            self.zOffset=None
            self.terrainZone=Player.TERRAIN_NONE
            self.terrainSurfZ=None
            self.collidedObjects=list()
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
            #   sphere
            collSphere=CollisionSphere(0, 0, 0.5, 0.25)
            collSphereN=CollisionNode("playerCollSphere")
            collSphereN.addSolid(collSphere)
            collSphereN.setFromCollideMask(2)
            collSphereN.setIntoCollideMask(CollideMask.allOff())
            collSphereNP=self.actor.attachNewNode(collSphereN)
            collSphereNP.show()
            self.collQSphere=CollisionHandlerQueue()
            self.base.cTrav.addCollider(collSphereNP, self.collQSphere)
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
            if not self.keyState[key]==state:
                log.debug("setKeyState %s->%s"%(key, str(state)))
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
                if self.zVelocity>0:
                    self.state=Player.STATE_FALL
                    log.debug("new state: %s"%str(self.state))
            # from Fall -> Idle
            elif self.state==Player.STATE_FALL:
                if self.zOffset<=0:
                    self.state=Player.STATE_IDLE
                    log.debug("new state: %s"%str(self.state))
                    self.zVelocity=0
                    #self.actor.setZ(self.terrainSurfZ)
        
        def processState(self, dt):
            # walk
            if self.walkDir!=0:
                speed=0.6 if self.state==Player.STATE_RUN else 0.3
                self.actor.setY(self.actor, speed*self.walkDir*dt)
            if self.rotationDir!=0:
                self.actor.setH(self.actor.getH()+15*self.rotationDir)
            # jump
            if self.state==Player.STATE_JUMP:
                self.zVelocity=Player.JUMP_ACCEL*dt
                log.debug("jump start at v=%f"%self.zVelocity)
            # fall
            if self.state==Player.STATE_FALL:
                dZ=self.zVelocity*dt
                dV=Player.FALL_ACCEL*dt
                newZ=self.actor.getZ()+dZ
                log.debug("falling... dt=%(dt)f getZ=%(getZ)f v=%(v)f dZ=%(dZ)f newZ=%(newZ)f dV=%(dV)f zOffset=%(zOff)f"%{"dt":dt, "getZ":self.actor.getZ(), "v":self.zVelocity, "dZ":dZ, "newZ":newZ, "dV":dV, "zOff":self.zOffset})
                if newZ<self.terrainSurfZ: newZ=self.terrainSurfZ
                self.actor.setZ(newZ)
                self.zVelocity+=dV
        
        def processTerrainRelation(self): # -> [terrainZone, terrainSurfZ, zOffset]
            collEntries=self.collQRay.getEntries()
            newZone=None
            #
            if len(collEntries)==0:
                #log.error("out of terrain, pos=%s"%str(self.actor.getPos()))
                newZone=Player.TERRAIN_NONE
                if newZone!=self.terrainZone:
                    self.onTerrainZoneChanged(Player.TERRAIN_NONE)
                self.terrainZone=newZone
                return Player.TERRAIN_NONE, 0, 0
            #
            entries=list(collEntries)
            entries.sort(key=lambda x:x.getSurfacePoint(self.base.render).getZ())
            terrainSurfZ=entries[-1].getSurfacePoint(self.base.render).getZ()
            entryName=entries[-1].getIntoNodePath().getName()
            #
            zOffset=self.actor.getZ()-self.terrainSurfZ
            #log.debug("ray collision entry name: %s"%entryName)
            if entryName=="Ground":
                newZone=Player.TERRAIN_GROUND
            elif entryName.startswith("Water"):
                newZone=Player.TERRAIN_WATER
            return newZone, terrainSurfZ, zOffset
        
        def onTerrainZoneChanged(self, zone):
            log.debug("terrain zone chaged to: %i"%zone)
        
        def processObstaclesRelation(self):
            self.collidedObjects=list()
            collEntries=list(self.collQSphere.getEntries())
            if len(collEntries)==0:
                return
            for entry in collEntries:
                entryName=entry.getIntoNodePath().getName()
                relPos=self.actor.getPos()-entry.getIntoNodePath().getPos()
                relHpr=self.actor.getHpr()-entry.getIntoNodePath().getHpr()
                self.collidedObjects.append("%s [%s,%s]"%(entryName, str(relPos), str(relHpr)))
        
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
            elif self.zOffset<=0:
                self.actor.setZ(self.terrainSurfZ)
            # obstacles relation
            self.processObstaclesRelation()
            # state
            self.defineState()
            self.processState(dt)
            # move
            return task.cont
