import requests


BASE = "http://127.0.0.1:5000"

response = requests.put(BASE + "/video/1",{"likes":10,"name":"ahamd","views":10000})

# response2 = requests.post(BASE + "helloword")

print(response.json())
input()

# print(response2.json())

response =requests.get(BASE+"video/1")
print(response.json())
