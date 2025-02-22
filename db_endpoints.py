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


class EndPoints:

    @staticmethod
    def sendMsg(userID, chatID, msg, resId):
        return MessageConnector.sendDirectMsg(userID, chatID, msg, resId)
