import sys
import json

with open('newUserId.json') as f:
  data = json.load(f)

def my_list(userId, itemId):
    new_list = [3,5,6,34,345,334]
    return new_list, userId, itemId

myList, userId, itemId = my_list(data['userId'], data['itemId'])

resp = {
    "Name": "shalie",
    "Age": 23,
    "list": myList,
    "userId": userId,
    "itemId": itemId
}

print(json.dumps(resp))
sys.stdout.flush()
