import numpy as np
f = open("/Users/rohitbhoopalam/rohit/test_input5.txt", 'w')
total_time = 0
for i in range(1, 2500):
    r = np.random.choice(300)
    r1 = np.random.choice(500)
    total_time += r1
    f.write("<"+str(i)+","+str(r)+","+str(r1)+">\n")

f.close()
print total_time
