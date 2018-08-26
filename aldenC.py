import requests

class returnObj:
	def __init__(self, works, names, leaving, failed=False):
		self.works = works
		self.names = names
		self.leaving = leaving
		self.failed=failed

def makeRec(userID, kiosk):
	furl = "http://72.79.54.70:55622/acceptedID/" + userID + "/" + str(kiosk)
	try:	
		r = requests.get(url = furl, params = {})
		rdata = r.json()
		isAccepted = rdata['accepted']
		return returnObj(isAccepted, rdata['name'], rdata['leaving'])
	except:
		return returnObj(False, "Server", False, failed=True)

if __name__ == '__main__':
	makeRec("19422", 1)