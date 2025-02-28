import mysql.connector
import time
import os
from dotenv import load_dotenv

load_dotenv()

def env(name):
    return os.getenv(name)






mydb = mysql.connector.connect(
    host=env("HOST"),
    user=env("DB_UNAME"),
    password=env("DB_PASS"),
    database=env("DB_NAME"),
)




class MessageConnector:

    @staticmethod
    def _getMsgById(id):
        mycursor = mydb.cursor(dictionary=True)

        mycursor.execute("SELECT * FROM messages WHERE id='"+str(id)+"'")

        myresult = mycursor.fetchone()

        return myresult

    @staticmethod
    def _addMessage(chatID, userID, msg):
        mycursor = mydb.cursor()

        read_status="sent"
        time_sent=int(time.time())

        sql="""INSERT INTO messages (chat_id, sender_id, msg, time_sent, read_status) VALUES 
            (%s, %s, %s, %s, %s)
        """
        val = (chatID, userID, msg, time_sent, read_status)
        mycursor.execute(sql, val)

        mydb.commit()

        return mycursor.lastrowid

        print(mycursor.rowcount, "record inserted.")

    @staticmethod
    def sendDirectMsg(userID, chatID, msg, resId):

        res={
            "isErr":False,
            "msg":[],
            "err":"",
        }

        msgId=MessageConnector._addMessage(chatID, userID, msg)
        if(not msgId):
            res["isErr"]=True
            res["err"]="Some error occured"

        if(not res["isErr"]):
            msg=MessageConnector._getMsgById(msgId)

            if(not msg):
                res["isErr"]=True
                res["err"]="Some error occured"
                

        if(not res["isErr"]):
            res["msg"]=msg


        return res

class ChatConnector:
    @staticmethod
    def getChatByid(id):
        mycursor = mydb.cursor(dictionary=True)

        mycursor.execute("SELECT * FROM chats WHERE id='"+str(id)+"'")

        myresult = mycursor.fetchone()

        return myresult

    @staticmethod
    def setChatAdmin(id, admin_id):
        mycursor = mydb.cursor()

        sql = "UPDATE chats SET admin_id = '"+str(admin_id)+"' WHERE id = '"+str(id)+"'"

        mycursor.execute(sql)

        mydb.commit()

    @staticmethod
    def getUserIdsConnectedAdminAndOnline(adminId):
        mycursor = mydb.cursor(dictionary=True)

        sql="SELECT c.user_id FROM chats AS c "
        sql+="LEFT JOIN users AS u ON c.user_id=u.id "
        sql+="WHERE u.last_seen='online' AND c.admin_id='"+str(adminId)+"'"

        mycursor.execute(sql)

        myresult = mycursor.fetchall()
        data=[]
        for d in myresult:
            data.append(d["user_id"])

        return data

    @staticmethod
    def getAdminIdsConnectedUserAndOnline(userId):
        mycursor = mydb.cursor(dictionary=True)

        sql="SELECT c.admin_id FROM chats AS c "
        sql+="LEFT JOIN users AS u ON c.admin_id=u.id "
        sql+="WHERE u.last_seen='online' AND c.user_id='"+str(userId)+"'"

        mycursor.execute(sql)

        myresult = mycursor.fetchall()
        data=[]
        for d in myresult:
            data.append(d["admin_id"])

        return data


class UserConnector:
    @staticmethod
    def setUserOnline(userId):
        mycursor = mydb.cursor()

        sql = "UPDATE users SET last_seen = 'online' WHERE id = '"+str(userId)+"'"

        mycursor.execute(sql)

        mydb.commit()

        return "online"

    @staticmethod
    def setUserOffline(userId):
        mycursor = mydb.cursor()
        time_on=int(time.time())

        sql = "UPDATE users SET last_seen = '"+str(time_on)+"' WHERE id = '"+str(userId)+"'"

        mycursor.execute(sql)

        mydb.commit()

        return time_on


class EndPoints:

    @staticmethod
    def sendMsg(userID, chatID, msg, resId):
        return MessageConnector.sendDirectMsg(userID, chatID, msg, resId)

    @staticmethod
    def getChatData(id):
        return ChatConnector.getChatByid(id)
    
    @staticmethod
    def setChatAdmin(id, admin_id):
        return ChatConnector.setChatAdmin(id, admin_id)
    
    @staticmethod
    def setUseOnlineStatus(userId, isOnline):
        if(isOnline):
            return UserConnector.setUserOnline(userId)
        else:
            return UserConnector.setUserOffline(userId)

    @staticmethod
    def getAllUserToPing(userID, isAdmin):
        if(isAdmin):
            return ChatConnector.getUserIdsConnectedAdminAndOnline(userID)
        else:
            return ChatConnector.getAdminIdsConnectedUserAndOnline(userID)