import sys
sys.path.append('./gmbh')


import gmbh


def main():
    print("gmbh python client demo")

    service_options = gmbh.opts.service(name="pycli-tester")
    options = gmbh.opts.new(service=service_options)
    client = gmbh.client(options)
    client.start()


main()