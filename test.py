import requests

BASE = "http://127.0.0.1:5000/"

data = [{"user_id":"123456","reference_number":"1234","destination":"KZN","date":"2 Des","location":"LP","timeslot":"12:00"},
		{"user_id":"963258","reference_number":"7894","destination":"PTA","date":"24 March","location":"MPM","timeslot":"12:00"},
		{"user_id":"789456","reference_number":"9632","destination":"JHB","date":"5 April","location":"NW","timeslot":"12:00"},
		{"user_id":"112233","reference_number":"1597","destination":"CPT","date":"30 Jan","location":"FS","timeslot":"12:00"}]


for i in range(len(data)):
	response = requests.put(BASE + "package/" + str(i),data[i])
	print(response.json())

#response = requests.put(BASE + "package/" + str(5),{"user_id":"112233","reference_number":"1597","destination":"CPT","date":"30 Jan","location":"FS","timeslot":"12:00"})
#print(response)
#response = requests.get(BASE + "package/1")
#print(response.json())

#response = requests.patch(BASE + "package/0",{"reference_number": "7777"})

#response = requests.delete(BASE + "package/123456")
#print(response)

response = requests.get(BASE + "package/1")
print(response.json())

