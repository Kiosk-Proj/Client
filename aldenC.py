import requests

class returnObj:
	def __init__(self, works, names, leaving):
		self.works = works
		self.names = names
		self.leaving = leaving

def makeRec(userID, kiosk):
	furl = "http://72.79.54.70:55622/acceptedID/" + userID + "/" + str(kiosk)
	r = requests.get(url = furl, params = {})
	rdata = r.json()
	print(rdata)
	isAccepted = rdata['accepted']
	return returnObj(isAccepted, rdata['name'], rdata['leaving'])

if __name__ == '__main__':
	makeRec("19422", 1)