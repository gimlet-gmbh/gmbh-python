class registration:
    def __init__(self, id, mode, address, corePath, fingerprint):
        self.id = id
        self. mode = mode
        self.address = address
        self.corePath = corePath
        self.fingerprint = fingerprint

class Client:
    def __init__(self, registration, options, rpcConnection, registeredFunc, timeDuration, address, state, parentID, whoIs, msgCounter, mu, errors, warnings, env, closed):
        self.registration = registration
        self.options = options
        self.rpcConnection = rpcConnection
        self. registeredFunc = registeredFunc
        self.timeDuration = timeDuration
        self.address = address
        self.state = state
        self.parentID = parentID
        self.whoIs = whoIs
        self.msgCounter = msgCounter
        self.mu = mu
        self.errors = errors
        self.warnings = warnings
        self.env = env
        self.closed = closed
    
    # NewClient should be called only once. It returns the object in which parameters, and
    # handler functions can be attached to gmbh Client.
    def NewClient(self, *opts):
        
    # Start()
    # Shutdown(src)
    # resolveAddress(target)
    # disconnect()
    # failed
    # makeUnregisterRequest()
    # getReg()
    


if __name__ == '__main__':
    cli = Client("reg", "options", "rpc", "register", 10, "addy", "state", 1, "whois", 0, "mu", "errors", "warnings", "env", "closed")
    cli.NewClient("option1", "option2", "option3")

    
