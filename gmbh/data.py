class transport:
    def __init__(self, sender='',target='',method=''):
        self.sender = sender
        self.target = target
        self.method = method

    def proto(self):
        print()

    @staticmethod
    def fromProto(self, proto):
        print()
    

class payload:
    def __init__(self):
        self._data = {}

    def get(self,key):
        print()
    
    def getAsString(self,key):
        print()

    def append(self,key,value):
        print()

    def appendDataMap(self, inputData):
        print()
    
    def proto(self):
        print()

    @staticmethod
    def fromProto(self, proto):
        print()

class request:
    def __init__(self):
        self._payload = payload()
        self._transport = transport()

    def getPayload(self):
        print()

    def setPayload(self):
        print()

    def getTransport(self):
        print()

    def setTransport(self):
        print()

    def proto(self):
        print()

    @staticmethod
    def fromProto(self, proto):
        print()

class responder:
    def __init__(self):
        self._payload = None
        self._transport = None
        self._err = ""

    def setPayload(self, payload):
        print()
    
    def getPayload(self):
        print()

    @staticmethod
    def fromProto(self, proto):
        print()
