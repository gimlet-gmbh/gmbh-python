class runtime():
    def __init__(self,blocking=True,verbose=True):
        self.blocking = blocking
        self.verbose = verbose
    def set_blocking(self, v):
        self.bocking = v
    def set_verbose(self, v):
        self.verbose = v

class service():
    def __init__(self, name="", aliases=[], pg=["universal"]):
        self.name = name
        self.aliases = aliases
        self.peerGroups = pg
    def set_name(self,name):
        self.name = name
    def set_aliases(self, aliases):
        self.aliases = aliases
    def set_peerGroups(self, pg):
        self.peerGroups = pg

class standalone():
    def __init__(self, coreAddress="localhost:49500"):
        self.coreAddress = coreAddress
    def set_coreAddress(self, coreAddress):
        self.coreAddress = coreAddress

class new:
    def __init__(self,runtime=runtime(), service=service(), standalone=standalone()):
        self.runtime = runtime
        self.service = service
        self.standalone = standalone
    def set_runtime(self, runtime):
        self.runtime = runtime
    def set_service(self, service):
        self.service = service
    def set_standalone(self, standalone):
        self.standalone = standalone


