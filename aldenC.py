import requests
import gevent
from gevent import Timeout

class returnObj:
	def __init__(self, works, names, leaving, failed=False, withInfo=False):
		self.works = works
		self.names = names
		print(names)
                self.leaving = leaving
		self.failed=failed
		self.withInfo = withInfo

def request_server(): 
	return requests.get(url = rURL, params = {"id":str(userID), "kiosk":str(kNum)})


def makeRec(userID):
	global r
	iniFile = open("/home/pi/kiosk/client/ini.txt", "r")
	rURL = iniFile.readline().rstrip()
	kNum = int(iniFile.readline().rstrip())

	# furl = "http://72.79.54.70:55622/acceptedID/" + userID + "/" + str(kiosk)
	# timeout = Timeout(3)
	# timeout.start()
	# try:
	# 	gevent.start(request_server).join()
	# 	print("finished")
	# 	rdata = r.json()
	# 	print(rdata)
	# except: 
	# 	print("Server Error")
	# 	return returnObj(False, "REE", False, failed = True)
 #    finally:
 #        timeout.cancel()
 	r = Timeout.with_timeout(2, request_server, timeout_value=None)
 	rdata = None

 	if(r == None):
 		print("Server Error")
 		return returnObj(False, "REE", False, failed = True)
 	else: 
 		print("finished")
 		rdata = r.json()
 		print(rdata)

	if rdata['id'] == str(-1):
		return returnObj(rdata['seniorPriv'], rdata["name"], not rdata['in'])
	else:
		return returnObj(rdata['seniorPriv'], rdata["name"], not rdata['in'], withInfo=True)

if __name__ == '__main__':
	print(makeRec("19422"))

