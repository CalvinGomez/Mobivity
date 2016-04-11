import json
import re
from tabulate import tabulate

data = []
detailedData = []
detailedDataDrinks = []

def readData():
	global data
	data = tuple(open('data/sample-receipts.json', encoding="utf8"))

def numberCountCheck(s):
	ctr = 0
	flag = 0
	for i in range(0, len(s)):
		if s[i] == "#" and s[i+1].isdigit():
			ctr = i
			flag = 1
			break
	if flag==1:
		s = list(s)
		s.pop(ctr)
		s.pop(ctr)
		s = str(s)
	
	newS = 0
	for i in range(0,len(s)):
		if s[i].isdigit():
			news = int(s[i])
	return news

def computeQuantities():
	global detailedData, detailedDataDrinks
	for i in range(0,len(data)):
		dataJSON = json.loads(data[i])
		receipt = str(dataJSON['receipt'])
		patternSub = re.compile("\n(.*)(\d*)(.*)(6|12)\"(.*)Sub(.*)\r")
		matchSub = patternSub.findall(receipt)

		if len(matchSub)>0:
			inches = 0
			quantity = 0
			for j in range(0,len(matchSub)):
				inches = int(matchSub[j][3].strip())
				if containsNumbers(matchSub[j][0])==True:
					quantity = numberCountCheck(matchSub[j][0])
				else:
					quantity = 1
				detailedData.append([quantity, inches])

		patternSubKids = re.compile("Kids Meal(.*)\n(.*)Sub(.*)\r")
		matchSubKids = patternSubKids.findall(receipt)
		# print(matchSubKids)

		if len(matchSubKids)>0:
			inches = 0
			quantity = 1
			for j in range(0,len(matchSubKids)):
				detailedData.append([quantity, inches])
	
	# print(detailedData)
		pattern = re.compile("\n(.*)(\d\d)(.*)[oz|Oz](.*)Drink(.*)\r")
		match = pattern.findall(receipt)

	# print(match)
		if len(match)>0:
			quantity = 0
			for j in range(0,len(match)):
				if containsNumbers(match[j][0])==True:
					quantity = int(re.sub("\D", "", match[j][0]))
				else:
					quantity = 1
				detailedDataDrinks.append(quantity)

	# print(detailedData)

def displayResult():
	totalQuantity = 0.0
	totalInches	= 0.0
	totalQuantitySubs = sum(row[0] for row in detailedData)
	totalInches = sum(row[1] for row in detailedData)
	totalFeet = totalInches/12.0
	print("Sandwiches:")
	print(tabulate([[totalQuantitySubs, totalFeet]], headers=['Quantity', 'Feet']))

	totalQuantityDrinks = sum(detailedDataDrinks)
	print("\nDrinks:")
	print(tabulate([[totalQuantityDrinks]], headers=['Quantity']))

def containsNumbers(s):
	return any(character.isdigit() for character in s)

readData()
computeQuantities()
displayResult()