def isValidToken(token):
    return isStaff(token) | isUser(token)


def isStaff(token):
    from main import stafftoken
    if token in stafftoken.values():
        return True
    return False


def serializeDatetime(arr):
    from datetime import datetime
    for i in range(len(arr)):
        for key in arr[i]:
            if type(arr[i][key]) == datetime:
                arr[i][key] = str(arr[i][key])
    return arr


def isUser(token):
    from main import usertoken
    if token in usertoken.values():
        return True
    return False


def getUID(token):
    from main import usertoken
    if isUser(token):
        for uid in usertoken:
            if usertoken[uid] == token:
                return uid
    return None


def getSID(token):
    from main import stafftoken
    if isStaff(token):
        for uid in stafftoken:
            if stafftoken[uid] == token:
                return uid
    return None
