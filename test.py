aa = [1,2,5,7,2]

try:
	for v in aa:
		if v == 5:
			raise Exception("!!!!!!!")
except:
	print("hhh")