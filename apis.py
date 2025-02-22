import requests

url = 'http://localhost/chat_box/chat_box/resources/backend/apis/socket/'


def sendApiMsg(userID, chatID, msg, resId):
    link=url+"send_msg.php"


    myobj = {
        'userID': userID,
        'chatID': chatID,
        'msg': msg,
        'resId': resId,
    }

    x = requests.post(link, data = myobj)
    res=x.json()

    # isErr, msg, err
    return res

