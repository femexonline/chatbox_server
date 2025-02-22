import asyncio
import websockets
from websockets import WebSocketServerProtocol
import json

from db_endpoints import EndPoints


admins={}
users={}

class Pings:
    @staticmethod
    async def msgSent(resData, msgSendingID, userid, isAdmin, sockeetId):
        send=[
            "msgsent",
            resData["msg"],
            msgSendingID,
            resData["isErr"],
            resData["err"],
        ]


        #     websocket.closed
        user_sockets={}
        if(isAdmin):
            user_sockets=admins
        else:
            user_sockets=users

        if(userid in user_sockets):
            for socId in user_sockets[userid]:
                webSoc:WebSocketServerProtocol=user_sockets[userid][socId]

                webSoc.send(json.dumps(send))

        




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

async def recieveMessage(message, userid, isAdmin, sockeetId):
    message=json.dumps(message)
    print(message)
    type=message[0]

    if(type=="sendmsg"):
        sendmsg(message, userid, isAdmin, sockeetId)


    def sendmsg(message:list, userid, isAdmin, sockeetId):
        userID=message[1]
        chatID=message[2]
        msgSendingID=message[3]
        msg=message[4]
        resId=message[5]

        resData=EndPoints.sendMsg(userID, chatID, msg, resId)

        Pings.msgSent(resData, msgSendingID, userid, isAdmin, sockeetId)






async def handle_connection(websocket:WebSocketServerProtocol, path):
    print("A client connected!")

    data=path.split("/")
    userid=data[1]
    isAdmin=int(data[2])
    sockeetId=data[3]
    
    processUser(userid, isAdmin, sockeetId, websocket)

    print(type(websocket))

    try:
        while True:
            # Set a timeout for receiving messages
            message = await asyncio.wait_for(websocket.recv(), timeout=10)  # 10 seconds timeout
            if(message):
                print(users)
                recieveMessage(message, userid, isAdmin, sockeetId)
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
