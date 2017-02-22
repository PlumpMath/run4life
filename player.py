from panda3d.core import CollideMask, CollisionNode, CollisionRay, CollisionSphere, CollisionHandlerQueue, CollisionHandlerPusher
from panda3d.core import NodePath
from panda3d.core import KeyboardButton
from direct.actor.Actor import Actor

import logging
log=logging.getLogger(__name__)

class Player:

        STATE_IDLE="Idle"
        STATE_WALK="Walk"
        STATE_RUN="Run"
        STATE_JUMP="Jump"
        STATE_RUNJUMP="RunJump"
        STATE_FALL="Fall"
        STATE_DUCK="Duck"
        STATE_UN_DUCK="UnDuck"
        
        JUMP_ACCEL=3.5
        FALL_ACCEL=-9.81
    
        TERRAIN_NONE=0
        TERRAIN_GROUND=1
        TERRAIN_WATER=2
        TERRAIN_AIR=3
    
        DUCK_FRAME_COUNT=0
        DUCK_FRAME_MID=0
        
        SUNK_CUTOFF=-0.9
    
        def __init__(self, base):
            self.base=base
            self.keyState={
                "WalkFw":False, 
                "WalkBw":False, 
                "Run":False, 
                "RotateL":False, 
                "RotateR":False, 
                "Jump":False, 
                "Duck":False
                }
            self.isKeyDown=self.base.mouseWatcherNode.isButtonDown
            self.state=Player.STATE_IDLE
            self.walkDir=0
            self.rotationDir=0
            self.zVelocity=0
            self.zOffset=None
            self.jumpHeight=None
            self.terrainZone=Player.TERRAIN_NONE
            self.terrainSurfZ=None
            self.waterDepth=0
            self.collidedObjects=list()
            # actor
            anims={"idle":"models/player-idle","walk":"models/player-walk", "run":"models/player-run", "jump":"models/player-jump", "duck":"models/player-duck"}
            self.actor=Actor("models/player", anims)
            self.actor.reparentTo(self.base.render)
            self.actor.setH(200)
            log.debug("actor tight bounds is %s"%str(self.actor.getTightBounds()))
            # animation info
            Player.DUCK_FRAME_COUNT=self.actor.getNumFrames("duck")
            Player.DUCK_FRAME_MID=int(Player.DUCK_FRAME_COUNT/2)
            # camara point
            self.camNode=NodePath("camNode")
            self.camNode.reparentTo(self.actor)
            self.camNode.setPos(0, 0, 1)
            # collision
            #   ray
            collRay=CollisionRay(0, 0, 1.5, 0, 0, -1)
            collRayN=CollisionNode("playerCollRay")
            collRayN.addSolid(collRay)
            collRayN.setFromCollideMask(1)
            collRayN.setIntoCollideMask(CollideMask.allOff())
            collRayNP=self.actor.attachNewNode(collRayN)
            #collRayNP.show()
            self.collQRay=CollisionHandlerQueue()
            self.base.cTrav.addCollider(collRayNP, self.collQRay)
            #   sphere mask 2
            collSphere2=CollisionSphere(0, 0, 0.5, 0.25)
            collSphere2N=CollisionNode("playerCollSphere2")
            collSphere2N.addSolid(collSphere2)
            collSphere2N.setFromCollideMask(2)
            collSphere2N.setIntoCollideMask(CollideMask.allOff())
            self.collSphere2NP=self.actor.attachNewNode(collSphere2N)
            #self.collSphere2NP.show()
            self.collPSphere=CollisionHandlerPusher()
            self.collPSphere.addCollider(self.collSphere2NP, self.actor)
            self.base.cTrav.addCollider(self.collSphere2NP, self.collPSphere)
            #   sphere mask 3
            collSphere3=CollisionSphere(0, 0, 0.35, 0.4)
            collSphere3N=CollisionNode("playerCollSphere3")
            collSphere3N.addSolid(collSphere3)
            collSphere3N.setFromCollideMask(3)
            collSphere3N.setIntoCollideMask(CollideMask.allOff())
            #collSphere3NP=
            self.actor.attachNewNode(collSphere3N)
            #collSphere3NP.show()
            self.collQSphere=CollisionHandlerQueue()
            #self.base.cTrav.addCollider(collSphere3NP, self.collQSphere)
            # task
            self.base.taskMgr.add(self.update, "playerUpdateTask")
        
        def defineKeys(self):
            for k in self.keyState.keys():
                self.keyState[k]=False
            if self.isKeyDown(KeyboardButton.up()):
                self.keyState["WalkFw"]=True
            if self.isKeyDown(KeyboardButton.down()):
                self.keyState["WalkBw"]=True
            if self.isKeyDown(KeyboardButton.left()):
                self.keyState["RotateL"]=True
            if self.isKeyDown(KeyboardButton.right()):
                self.keyState["RotateR"]=True
            if self.isKeyDown(KeyboardButton.shift()):
                self.keyState["Run"]=True
            if self.isKeyDown(KeyboardButton.space()):
                self.keyState["Jump"]=True
            if self.isKeyDown(KeyboardButton.asciiKey("d")):
                self.keyState["Duck"]=True
        
        def defineState(self):
            #
            newState=self.state
            # keys states
            ks=self.keyState
            # state force
            if self.zOffset>0.2 and self.state!=Player.STATE_FALL:
                newState=Player.STATE_FALL
            # from Idle -> Walk, Jump
            if self.state==Player.STATE_IDLE:
                # Walk
                if ks["WalkFw"] or ks["WalkBw"] or ks["RotateL"] or ks["RotateR"]:
                    newState=Player.STATE_WALK
                elif ks["Jump"]:
                    newState=Player.STATE_JUMP
                elif ks["Duck"]:
                    newState=Player.STATE_DUCK
            # from Walk, Run -> Walk, Run, Idle; from Run -> Jump
            elif self.state==Player.STATE_WALK or self.state==Player.STATE_RUN:
                if ks["Run"] and self.state!=Player.STATE_RUN and self.terrainZone!=Player.TERRAIN_WATER:
                    newState=Player.STATE_RUN
                elif not ks["Run"] and self.state==Player.STATE_RUN:
                    newState=Player.STATE_WALK
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
                if ks["Jump"]:
                    newState=Player.STATE_RUNJUMP
                if self.walkDir==0 and self.rotationDir==0:
                    newState=Player.STATE_IDLE
            # from Jump -> Fall
            elif self.state==Player.STATE_JUMP or self.state==Player.STATE_RUNJUMP:
                if self.zVelocity>0:
                    newState=Player.STATE_FALL
            # from Fall -> Idle
            elif self.state==Player.STATE_FALL:
                if self.zOffset<=0:
                    newState=Player.STATE_IDLE
                    self.jumpHeight=None
                    self.zVelocity=0
                    self.walkDir=0
            # from Duck -> UnDuck
            elif self.state==Player.STATE_DUCK:
                if not ks["Duck"]:
                    newState=Player.STATE_UN_DUCK
            # from UnDuck -> Idle
            elif self.state==Player.STATE_UN_DUCK:
                if not self.actor.getCurrentAnim()=="duck":
                    newState=Player.STATE_IDLE
            return newState
        
        def processState(self, dt):
            # terrain sdjustment
            if self.zOffset<=0:
                self.actor.setZ(self.terrainSurfZ)
            # idle
            if self.state==Player.STATE_IDLE:
                self.collSphere2NP.setZ(0)
            # walk
            if self.walkDir!=0:
                if self.zVelocity==0:
                    speed=3.6 if self.state==Player.STATE_RUN else 2.4
                else:
                    speed=3.2
                if self.terrainZone==Player.TERRAIN_WATER:
                    speed*=0.5
                self.actor.setY(self.actor, speed*self.walkDir*dt)
            if self.rotationDir!=0:
                self.actor.setH(self.actor.getH()+3.5*self.rotationDir)
            # jump
            if self.state==Player.STATE_JUMP or self.state==Player.STATE_RUNJUMP:
                self.zVelocity=Player.JUMP_ACCEL
                log.debug("jump start at v=%f"%self.zVelocity)
                if self.state==Player.STATE_RUNJUMP:
                    self.walkDir=-1
            # fall
            if self.state==Player.STATE_FALL:
                dZ=self.zVelocity*dt
                dV=Player.FALL_ACCEL*dt
                curZ=self.actor.getZ()
                newZ=curZ+dZ
                if self.jumpHeight==None and newZ<curZ:
                    self.jumpHeight=self.zOffset
                    log.debug("jump height=%f"%self.jumpHeight)
                log.debug("falling... dt=%(dt)f getZ=%(getZ)f v=%(v)f dZ=%(dZ)f newZ=%(newZ)f dV=%(dV)f zOffset=%(zOff)f"%{"dt":dt, "getZ":self.actor.getZ(), "v":self.zVelocity, "dZ":dZ, "newZ":newZ, "dV":dV, "zOff":self.zOffset})
                if newZ<self.terrainSurfZ: newZ=self.terrainSurfZ
                self.actor.setZ(newZ)
                self.zVelocity+=dV
            # duck
            if self.state==Player.STATE_DUCK:
                if self.actor.getCurrentAnim()=="duck":
                    collSphrZ=(self.actor.getCurrentFrame("duck")/Player.DUCK_FRAME_MID)*0.25
                    self.collSphere2NP.setZ(-collSphrZ)
        
        def processTerrainRelation(self): # -> [terrainZone, terrainSurfZ, zOffset, waterDepth]
            collEntries=self.collQRay.getEntries()
            newZone=None
            #
            if len(collEntries)==0:
                #log.error("out of terrain, pos=%s"%str(self.actor.getPos()))
                newZone=Player.TERRAIN_NONE
                if newZone!=self.terrainZone:
                    self.onTerrainZoneChanged(Player.TERRAIN_NONE)
                self.terrainZone=newZone
                return Player.TERRAIN_NONE, 0, 0, 0
            #
            newZone=Player.TERRAIN_NONE
            gndZ, wtrZ=-1000, -1000
            waterDepth=0
            for entry in collEntries:
                eName=entry.getIntoNodePath().getName()
                eZ=entry.getSurfacePoint(self.base.render).getZ()
                if eName.startswith("Water"):
                    wtrZ=eZ
                    if wtrZ>gndZ:
                        newZone=Player.TERRAIN_WATER
                else:
                    if eZ>gndZ: gndZ=eZ
                    if gndZ>wtrZ:
                        newZone=Player.TERRAIN_GROUND
            if newZone==Player.TERRAIN_WATER:
                waterDepth=gndZ-wtrZ
                log.debug("water depth is %f"%waterDepth)
            zOffset=self.actor.getZ()-gndZ
            return newZone, gndZ, zOffset, waterDepth
#            ###
#            entries=list(collEntries)
#            entries.sort(key=lambda x:x.getSurfacePoint(self.base.render).getZ())
#            entryName=entries[-1].getIntoNodePath().getName()
#            #
#            groundEntries=[ge for ge in entries if not ge.getIntoNodePath().getName().startswith("Water")]
#            groundEntries.sort(key=lambda x:x.getSurfacePoint(self.base.render).getZ())
#            terrainSurfZ=groundEntries[-1].getSurfacePoint(self.base.render).getZ()
#            #
#            zOffset=self.actor.getZ()-self.terrainSurfZ
#            #log.debug("ray collision entry name: %s"%entryName)
#            if entryName=="Ground" or entryName.startswith("Rock"):
#                newZone=Player.TERRAIN_GROUND
#            elif entryName.startswith("Water"):
#                newZone=Player.TERRAIN_WATER
#            return newZone, gndZ, zOffset
        
        def onTerrainZoneChanged(self, zone):
            log.debug("terrain zone chaged to: %i"%zone)
        
        def onStateChanged(self, newState):
            curState=self.state
            log.debug("state change %s -> %s"%(str(curState), str(newState)))
            #self.actor.stop()
            if newState==Player.STATE_IDLE:
                self.actor.pose("idle", 0)
            elif newState==Player.STATE_WALK:
                self.actor.setPlayRate(4.0, "walk")
                self.actor.loop("walk")
            elif newState==Player.STATE_RUN:
                self.actor.loop("run")
            elif newState==Player.STATE_JUMP or newState==Player.STATE_RUNJUMP:
                self.actor.setPlayRate(1.4, "jump")
                self.actor.play("jump", fromFrame=20, toFrame=59)
            elif newState==Player.STATE_DUCK:
                self.actor.play("duck", fromFrame=0, toFrame=Player.DUCK_FRAME_MID)
            elif newState==Player.STATE_UN_DUCK:
                initFrame=Player.DUCK_FRAME_MID
                if self.actor.getCurrentAnim()=="duck":
                    initFrame=Player.DUCK_FRAME_COUNT-self.actor.getCurrentFrame("duck")
                self.actor.stop()
                self.actor.play("duck", fromFrame=initFrame, toFrame=Player.DUCK_FRAME_COUNT)
        
        def fillCollidedObjectsList(self):
            self.collidedObjects=list()
            collEntries=list(self.collPSphere.getEntries())
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
            # keys
            self.defineKeys()
            # terrain relation
            newZone, self.terrainSurfZ, self.zOffset, self.waterDepth=self.processTerrainRelation()
            if newZone!=self.terrainZone:
                self.terrainZone=newZone
                self.onTerrainZoneChanged(self.terrainZone)
            # obstacles relation
            #self.fillCollidedObjectsList()
            # state
            newState=self.defineState()
            if self.state!=newState:
                self.onStateChanged(newState)
                self.state=newState
            self.processState(dt)
            # move
            return task.cont
