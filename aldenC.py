import requests

class returnObj:
	def __init__(self, works, names, leaving):
		self.works = works
		self.names = names
		self.leaving = leaving

def makeRec(userID):
	iniFile = open("ini.txt", "r")
	rURL = iniFile.readline().rstrip()
	kNum = int(iniFile.readline().rstrip())

	# furl = "http://72.79.54.70:55622/acceptedID/" + userID + "/" + str(kiosk)
	try:
		r = requests.get(url = rURL, params = {"id":str(userID), "kiosk":str(kNum)})
		print("finished")
		rdata = r.json()
		print(rdata)
	except:
		print("Server Error")
		returnObj(False, "REE", False)

	return returnObj(True, rdata["name"], rdata['seniorPriv'])
	# isAccepted = rdata['accepted']

	# return returnObj(isAccepted, rdata['name'], rdata['leaving'])

if __name__ == '__main__':
	print(makeRec("19422"))

