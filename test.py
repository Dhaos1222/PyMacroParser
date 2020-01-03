
#coding=utf-8
tt = u"this is a data"
aa = tt.decode("unicode_escape")
# aa = tt.encode("unicode_escape")
# aa = unicode_escape(tt)
# aa = '\\x0c'
# aa = '0X4f3'
aa = [[97, (98,), 23], [97, (98,), 25]]
ret = []
for k in aa:
	ret.append(tuple(k))
	print(ret)
print(tuple(ret))

# aa = aa.decode("string_escape")
# print(aa)
# print(int(aa, 16))
# print(type(aa))

# print(ord(aa))