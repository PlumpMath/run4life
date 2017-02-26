from direct.showbase.ShowBase import ShowBase
from gameplay import Gameplay
from panda3d.core import PStatClient

import logging
log=logging.getLogger(__name__)

class Game(ShowBase):
    
    def __init__(self):
        ShowBase.__init__(self)
        logging.basicConfig(level=logging.DEBUG)
        log.info("initializing...")
        #
        self.disableMouse()
        self.setFrameRateMeter(True)
        self.render.setShaderAuto()
        #
        gameplay=Gameplay(self)
        gameplay.start()
        #
        PStatClient.connect()
        #
        log.info("done initializing")
