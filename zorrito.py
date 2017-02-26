from direct.actor.Actor import Actor

import logging
log=logging.getLogger(__name__)

class Zorrito:
    
    def __init__(self, base):
        self.base=base
        #
        self.actor=Actor("models/zorrito")
        self.actor.reparentTo(self.base.render)
        self.actor.setScale(0.15)
