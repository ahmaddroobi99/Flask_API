import requests


BASE = "http://127.0.0.1:5000"
data =[ {"likes":10,"name":"droobi","views":10000},
        {"likes":10,"name":"how to make rest API","views":10000} ,
        {"likes":12,"name":"ahmad","views":652}]

for i in range (len(data)):
    response = requests.put(BASE + "/video/" + str(i), data[i])
    print(response.json())

# response = requests.delete(BASE + "/video/0")
# print (response)
input()
response =requests.get(BASE+"/video/2")
print(response.json())

