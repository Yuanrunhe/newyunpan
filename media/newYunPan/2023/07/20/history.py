a = pd.Series([2,3,5,6])
a
a.index
a.index=["a","b","c","d"]
a
import numpy as np
a.index
a
a["a"]
a[1]
a[0]
a[1:3]
a.get()
a.get(index)
a.index
a[""e]
a["e"]
a.get(2)
a.get(7,"www")
a.name="索引列"
a
pd.DataFrame(np.range(20).reshape(4,5))
pd.DataFrame(np.arange(20).reshape(4,5))
a = pd.DataFrame(np.arange(20).reshape(4,5),index=["a","b","c","d"],columns=["one","two","three","font"])
a = pd.DataFrame(np.arange(20).reshape(4,5),index=["a","b","c","d","e"],columns=["one","two","three","font"])
a = pd.DataFrame(np.arange(20).reshape(4,5),index=["a","b","c","d"],columns=["one","two","three","font","fax"])
a
a["one"]
a.ix["a"]
import turtlr

## ---(Fri Aug 14 10:32:13 2020)---
a = [3,6,1,2,7,3,4]
a.sort()
a
names = ["小红","小黄","小林","小李","小明"]
a = ["小王","小吴","小李","小林","小院"]
count = 0
for i in range(len(a)):
    if names.count(a[i]):
        count+=1
print(count)
b = "abdjonkabba"
b.count("a")
"{:->20}".format(123)
import jieba
a = {"a":2,"b":6,"c":3,"d":23,"e":13,"f":7}
a
list(a)
list(dict.items())
list(a.items())
sort(key lambda x:x[1],reverse=False)
sort(key=lambda x:x[1],reverse=False)
a
ls=list(a.items())
ls
sort(key=lambda x:x[1],reverse=False)
ls.sort(key=lambda x:x[1],reverse=False)
ls
b=ls.sort(key=lambda x:x[1],reverse=False)
b
print(b)
a
ls=list(a.items())
ls
b=ls.sort(key=lambda x:x[1],reverse=False)
b
ls
b=ls.sort(key=lambda x:x[1],reverse=True)
b
typr(ls)
type(ls)
a = [('a', 2), ('c', 3), ('b', 6), ('f', 7), ('e', 13), ('d', 23)]
a.items()
a.sort()
a
a.sort(key=lambda x:x[1])
a
a = {"a":2,"b":6,"c":3,"d":23,"e":13,"f":7}
list(a)
list(a.items())
tt = list(a.items())
tt
tt.sort(key=lambda x:x[1])
a.value()
a.values()
tt
a = [('a', 2), ('c', 3), ('b', 6), ('f', 7), ('e', 13), ('d', 23)]
a = {"a":2,"b":6,"c":3,"d":23,"e":13,"f":7}
dd = list(a.items())
dd
dd.sort(key=lambda x:x[1],reverse=True)
dd
print("{最高得票者:}{票数为:}".format(dd[0][0],dd[0][1]))
print("{}{}".format(最高得票者:dd[0][0],票数为:dd[0][1]))
print("{}{}".format("最高得票者:"dd[0][0],"票数为:"dd[0][1]))
print("最高得票者:{}票数为:{}".format(dd[0][0],dd[0][1]))
a = "00000003210Runoob01230000000"
print str.strip('0')
print a.strip('0')
print(a.strip('0'))

## ---(Fri Aug  6 16:18:57 2021)---
runfile('C:/Users/User/.spyder-py3/temp.py', wdir='C:/Users/User/.spyder-py3')