from pump import Pump
import time


######################
# RESOURCE CATALOG
######################
RESOURCECAT_IP = "192.168.1.73"
RESOURCECAT_PORT = 8080

###############
# PUMP info
###############
resource_name = "pump1"
resources = ["out_pump"]
subnet = "1"
PIN = 26


################
# MAIN
################
if __name__ == '__main__':
	
	pump = Pump(resource_name, resources, subnet, PIN)

	if (pump.register(RESOURCECAT_IP, RESOURCECAT_PORT) == 1):
		print """\tUNABLE to register device to resource CATALOG
		(Check if the device is already registered with same name over the same IP address)"""

	pump.get_broker_info(RESOURCECAT_IP, RESOURCECAT_PORT)

	pump.run()

	while True:
		time.sleep(1)