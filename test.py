import time

from direct import sendDirectMsg
from apis import sendApiMsg

start=int(time.time()*1000)
print(sendDirectMsg(2, 1, "love in air", ""))
end=int(time.time()*1000)
print(end-start)


