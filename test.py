
#coding=utf-8
tt = u"this is a data"
# aa = tt.encode("unicode_escape")
# aa = unicode_escape(tt)
# aa = '\\x0c'
# aa = '0X4f3'
aa = "\v\'\"\f \"\n\r\t\b\a\\"
aa = '\x0b\'"\x0c"\n\r\t\x08\x07\\'
aa = '\x0b\'"\x0c "\n\r\t\x08\x07\\'
aa = aa.decode("string_escape")
ret = []
print(aa)
for k in aa:
	ret.append(tuple(k))
	print(tuple(k))
print(ret)

# aa = aa.decode("string_escape")
# print(aa)
# print(int(aa, 16))
# print(type(aa))

# print(ord(aa))