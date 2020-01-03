
#coding=utf-8
tt = u"this is a data"
aa = tt.decode("unicode_escape")
# aa = tt.encode("unicode_escape")
# aa = unicode_escape(tt)
# aa = '\\x0c'
# aa = '0X4f3'
aa = '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\//////////////////'
bb = '\\\\\\\\\\\\\\\\\\//////////////////'
ret = []
for k in aa:
	ret.append(tuple(k))
	print(tuple(k))
print(ret)

# aa = aa.decode("string_escape")
# print(aa)
# print(int(aa, 16))
# print(type(aa))

# print(ord(aa))