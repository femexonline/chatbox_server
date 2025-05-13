import time
from db_endpoints import ChatConnector, EndPoints


# print(ChatConnector.getUserIdsConnectedAdminAndOnline(6))
# print(ChatConnector.getAdminIdsConnectedUserAndOnline(1))



chatIds=[1,2,3]

chatData=EndPoints.getChatsByIdList(chatIds, False)

print(chatData)