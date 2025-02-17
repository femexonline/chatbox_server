import asyncio
import websockets


admins={}
users={}


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


async def handle_connection(websocket, path):
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
                print(users)
                print(admins)
                print(f"Received message: {message} {path}")
                await websocket.send(f"Server received: {message}")
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
