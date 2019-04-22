import sys
sys.path.append('./gmbh')

import gmbh

def main():
    print("gmbh python client demo")
     
    # Creates a new service
    theservice = gmbh.opts.service(name="pycli-tester")
    options = gmbh.opts.new(service=theservice)

    # Creates a new client
    client = gmbh.newClient(options)
    client.start()
    


main()
