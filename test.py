import time
from db_endpoints import ChatConnector


print(ChatConnector.getUserIdsConnectedAdminAndOnline(6))
print(ChatConnector.getAdminIdsConnectedUserAndOnline(1))

