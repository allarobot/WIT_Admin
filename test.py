from functools import reduce

if reduce(lambda x,y: x and y,[None, None, None, None, None, None, None, None]):
    print("True")

if reduce(lambda x,y: x and y,[None]):
    print("True")

import datetime
str_datetime = "17 JUL 17  10:54:56"
out = datetime.datetime.now().strftime("%y %b  %d %X")
print(out)
out2 = datetime.datetime.strptime(str_datetime,"%y %b %d  %X")
print(type(out2))
print(out2.year, out2.month, out2.day, out2.hour, out2.minute, out2.second)

