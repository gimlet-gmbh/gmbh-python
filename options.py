
# Options contain the runtime configurable parameters
# type(runtime) = RuntimeOptions
# type(standalone) = StandaloneOptions
# type(service) = ServiceOptions
class options:
    def __init__(self, runtime, standalone, service):

        # runtime are options that affect runtime behavior
        self.runtime = runtime

        # standalone options are those intended for use without the service launcher or remotes
        self.standalone = standalone

        # service options are those that are used for identifying the service with core
        self.service = service

# RuntimeOptions - user configurable
class RuntimeOptions:
    def __init__(self, blocking, verbose):

        # Should the client block the main threaad until shutdown signal is received
        self.Blocking = blocking

        # Should the client run in verbose mode. In Verbose mode, debug information regarding
        # the gmbh client will be printed to stdout
        self.Verbose = verbose

# StandaloneOptions - user configurable, for use only without the service launcher or remotes
class StandaloneOptions:
    def __init__(self, coreaddress):

        # The address back to core
        # NOTE: This will be overriden depending on environment
        self.CoreAddress = coreaddress

# ServiceOptions - user configurable, a name must be set, this is how other services will contact this one.
class ServiceOptions:
    def __init__(self, name, aliases, peergroups):

        # Name - the unique name of the service as registered to core
        self.Name = name

        # Aliases - like the name, must be unique across all services; act as shortcut names
        self.Aliases = aliases

        # The group_id defines services that are allowed to connect directly with each other
        # and bypass the core for faster communications.
        #
        # The id assignment is arbitrary as long as each intended one has the same id.
        # NOTE: Any services where the group_id is undefined will be able to talk to eachother freely.
        self.PeerGroups = peergroups

defaultOptions = options(
    runtime = RuntimeOptions(
        blocking = False, 
        verbose = False
    ),
    standalone = "StandaloneOptions()",
    service = ServiceOptions(
        name = "",
        aliases = slice(0),
        peergroups = ["universal"]
    )
)

# SetRuntime options of the client
def SetRuntime(runtimeoptions):
    def func(options):
        options.runtime.Blocking = runtimeoptions.Blocking
        options.runtime.Verbose = runtimeoptions.Verbose
    return func

# SetStandalone options of the client
def SetStandalone(standaloneoptions):
    def func(options):
        options.standalone.CoreAddress = standaloneoptions.CoreAddress
    return func

# SetService options of the client
def SetService(serviceoptions):
    def func(options):
        options.service.Name = serviceoptions.Name
        options.service.Aliases = serviceoptions.Aliases
        if len(serviceoptions) != 0:
            options.service.PeerGroups = serviceoptions.PeerGroups
    return func
