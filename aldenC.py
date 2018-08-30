import requests

class returnObj:
	def __init__(self, works, names, leaving, failed=False):
		self.works = works
		self.names = names
		self.leaving = leaving
		self.failed=failed

#<<<<<<< HEAD
#def makeRec(userID, kiosk)#
#	furl = "http://72.79.54.70:55622/acceptedID/" + userID + "/" + str(kiosk)
#	try:	
#		r = requests.get(url = furl, params = {})
#		rdata = r.json()
#		isAccepted = rdata['accepted']
#		return returnObj(isAccepted, rdata['name'], rdata['leaving'])
#	except:
#		return returnObj(False, "Server", False, failed=True)
#=======
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

	return returnObj(True, rdata["name"], not rdata['in'])
	# isAccepted = rdata['accepted']

	# return returnObj(isAccepted, rdata['name'], rdata['leaving'])
#>>>>>>> 02c60725d6d70d07122d51ad25aeced7d54ee965

if __name__ == '__main__':
	print(makeRec("19422"))

