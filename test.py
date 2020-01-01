
#coding=utf-8
tt = u"this is a data"
aa = tt.decode("unicode_escape")
# aa = tt.encode("unicode_escape")
# aa = unicode_escape(tt)
aa = '\x0c'
print(type(aa))

print(ord(aa))