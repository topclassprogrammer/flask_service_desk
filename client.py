import requests

# r = requests.get("http://127.0.0.1:5000/user/1")
# # print(r.json())
# print(r.text)
# print(r.status_code)

r = requests.post("http://127.0.0.1:5000/user", json={"username": "Ivan1cH9", "password": "abcdef123"})
print(r.json())
# print(r.text)
print(r.status_code)


# r = requests.patch("http://127.0.0.1:5000/user/1", json={"username": "Ivan1cH5555"}, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDI4NDA4MiwianRpIjoiY2RjZDNlZDctZDJmOS00YzFiLWE5NzctZDU0YjMwZGE1M2U4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwMjg0MDgyLCJjc3JmIjoiZGYzN2NlYjYtYjk1Mi00YjI4LTljMjMtYTk1NjlhNmJlMDEzIn0.-Hn4YHHXHNapfjuzqlwby-KLF_rECjSckM0iCblMzOM"})
# print(r.json())
# print(r.status_code)

# r = requests.delete("http://127.0.0.1:5000/user/2", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDI4NDM5NSwianRpIjoiY2FiOWE1ZmItZDE2Yy00MTY1LTgyZmItOTk5ODgyMDdmM2Q5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNzYwMjg0Mzk1LCJjc3JmIjoiMjFmMTBhMmQtYjAxOS00NTcxLWEwZDMtYjBiYTAyZWVlNzViIn0.2DiUenlP9swr7kdkIPUVY-LXNR6vPgqE8hhNUns0-MY"})
# # print(r.json())
# print(r.status_code)

# r = requests.get("http://127.0.0.1:5000/ticket/222")
# print(r.json())
# print(r.status_code)
# # #
r = requests.post("http://127.0.0.1:5000/ticket", json={"topic": "order", "description": "some description", "status": "new", "user": 1}, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2MDcyMjkwNCwianRpIjoiZTFhN2QxMDEtYTE2Zi00M2U3LWFjNTctNDQ3ZGVmYmY2N2RmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzYwNzIyOTA0LCJjc3JmIjoiZTQ4MmY1NjMtMjUxYy00NWM3LTg0YTEtZDIwZTAyMzc3MzRhIn0.-DTdxu3QDegVoMzmvd1xItZ5gmkOV8i3f4OqDlTCCfI"})
print(r.json())
print(r.status_code)
