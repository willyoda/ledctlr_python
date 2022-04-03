
import datetime  as DT

import time

#方法1，获取到系统的时间，显示到ms ,如2022-04-03 14:39:44.691249
# today =DT.date.today()
# td= DT.datetime(today.year,today.month,today.day)
# print(td.today())   #显示格式为 ：2022-04-03 14:39:44.691249
# print(td.now())     #显示格式为 ：2022-04-03 14:39:44.691249


print(time.localtime())
print(time.asctime())





#format 修改没成功
now = DT.datetime.now()
print('**** now=%s'%now)
dt= DT.datetime(now.year,now.month,now.day)
print('timestamp =%d'%dt.timestamp())
print('utc time %s'%(dt.utcnow()))

# dt.fromisoformat(DT.date.isoformat(''))
print('*** ',dt.today())   #显示格式为 ：2022-04-03 14:39:44.691249
# print(dt.now())     #显示格式为 ：2022-04-03 14:39:44.691249

td=DT.date.today()
print('td=%s'%td)
print(td.isoformat())



# tm=DT.time()
# print(tm.hour,tm.minute,tm.second,tm.microsecond)

