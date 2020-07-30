import time

s1 = set([i for i in range(100,300)])
s2 = set([i for i in range(200,400)])

int1 = 0
int2 = 0
for i in range(729):
	if i in s1:
		int1 += 2**i 
	if i in s2:
		int2 += 2**i

start = time.time()
for j in range(1000000):
	if int1 & int2:
		#print("int check passed")
		pass

end = time.time()

print("Int time: {}".format(end - start))


start = time.time()
for j in range(1000000):
	if not s1.isdisjoint(s2):
		#print("set check passed")
		pass

end = time.time()

print("Set time: {}".format(end - start))
