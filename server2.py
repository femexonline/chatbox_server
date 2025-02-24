import asyncio
import websockets
from websockets import WebSocketServerProtocol
import json

from db_endpoints import EndPoints


admins={}
users={}

class Pings:
    @staticmethod
    async def msgSent(resData, msgSendingID, senderId, isAdmin, sockeetId):
        send=[
            "msgsent",
            resData["msg"],
            msgSendingID,
            resData["isErr"],
            resData["err"],
        ]


        user_sockets={}
        if(isAdmin):
            user_sockets=admins
        else:
            user_sockets=users

        if(senderId in user_sockets):
            for socId in user_sockets[senderId]:
                webSoc:WebSocketServerProtocol=user_sockets[senderId][socId]
                if(not webSoc.closed):
                    await webSoc.send(json.dumps(send))
    
    @staticmethod
    async def notTheAdmin(chatID, senderId):
        send=[
            "nottheadmin",
            chatID,
        ]

        if(senderId in admins):
            for socId in admins[senderId]:
                webSoc:WebSocketServerProtocol=admins[senderId][socId]
                if(not webSoc.closed):
                    await webSoc.send(json.dumps(send))

    @staticmethod
    async def notTheAdmins(chatID, senderId):
        send=[
            "nottheadmins",
            chatID,
        ]

        for adminId in admins:
            if(senderId!=adminId):
                for socId in admins[adminId]:
                    webSoc:WebSocketServerProtocol=admins[adminId][socId]
                    if(not webSoc.closed):
                        await webSoc.send(json.dumps(send))


    @staticmethod
    async def newMsg(chatData, resData, senderId, isAdmin, sockeetId):
        if(resData["isErr"]):
            return
        
        newAdmin=None
        if(isAdmin):
            if(not chatData["admin_id"]):
                newAdmin=senderId
                None
        
        send=[
            "newmsg",
            resData["msg"],
            newAdmin
        ]

        # send to all admin if no admin
        if(not isAdmin):
            if(not chatData["admin_id"]):

                for adminId in admins:
                    for socId in admins[adminId]:
                        webSoc:WebSocketServerProtocol=admins[adminId][socId]
                        if(not webSoc.closed):
                            await webSoc.send(json.dumps(send))
            
                return



        user_sockets={}
        recieverId=0
        if(isAdmin):
            user_sockets=users
            recieverId=chatData["user_id"]
        else:
            user_sockets=admins
            recieverId=chatData["admin_id"]

        
        if(recieverId in user_sockets):
            for socId in user_sockets[recieverId]:
                webSoc:WebSocketServerProtocol=user_sockets[recieverId][socId]
                if(not webSoc.closed):
                    await webSoc.send(json.dumps(send))

        if(isAdmin):
            if(newAdmin):
                await Pings.notTheAdmins(chatData["id"], senderId)



class SocketMsgRecieve:
    @staticmethod
    async def recieve(message, userid, isAdmin, sockeetId):


        message=json.loads(message)
        msg_type=message[0]

        print("type", msg_type)
        print(message)
        print(type(message))

        if(msg_type=="sendmsg"):
            await SocketMsgRecieve._sendmsg(message, userid, isAdmin, sockeetId)


    @staticmethod
    async def _sendmsg(message:list, senderId, isAdmin, sockeetId):
        chatID=message[1]
        msgSendingID=message[2]
        msg=message[3]
        resId=message[4]


        chatData=EndPoints.getChatData(chatID)
        if(isAdmin):
            if(not chatData["admin_id"]):
                EndPoints.setChatAdmin(chatID, senderId)
            else:
                if(chatData["admin_id"] != senderId):
                    await Pings.notTheAdmin(chatID, senderId)
                    return


        resData=EndPoints.sendMsg(senderId, chatID, msg, resId)

        await Pings.msgSent(resData, msgSendingID, senderId, isAdmin, sockeetId)
        await Pings.newMsg(chatData, resData, senderId, isAdmin, sockeetId)






def processUser(userid, isAdmin, sockeetId, websocket):
    if(not isAdmin):
        if(userid not in users):
            users[userid]={}

        if(sockeetId not in users[userid]):
            users[userid][sockeetId]=websocket

    else:
        if(userid not in admins):
            admins[userid]={}

        if(sockeetId not in admins[userid]):
            admins[userid][sockeetId]=websocket
        
    print(userid, isAdmin, sockeetId)






async def handle_connection(websocket:WebSocketServerProtocol, path):
    print("A client connected!")

    data=path.split("/")
    userid=data[1]
    isAdmin=int(data[2])
    sockeetId=data[3]
    
    processUser(userid, isAdmin, sockeetId, websocket)


    try:
        while True:
            # Set a timeout for receiving messages
            message = await asyncio.wait_for(websocket.recv(), timeout=10)  # 10 seconds timeout
            if(message):
                print(sockeetId)
                await SocketMsgRecieve.recieve(message, userid, isAdmin, sockeetId)
                # await websocket.send(f"Server received: {message}")
    except asyncio.TimeoutError:
        print("Client timed out - no messages received for 10 seconds")
    except websockets.ConnectionClosed:
        print("A client disconnected")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def main():
    async with websockets.serve(handle_connection, "localhost", 8080):
        print("WebSocket server is running on ws://localhost:8080")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
