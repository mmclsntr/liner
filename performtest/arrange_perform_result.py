import sys
import re

argvs = sys.argv

if len(argvs) < 2:
    print("Please set result files")
    sys.exit(1) 

argvs.pop(0)
filename = argvs[0]

current_time = -1
usrcpu_tmp = 0.0
syscpu_tmp = 0.0
guestcpu_tmp = 0.0
totalcpu_tmp = 0.0
minflt_tmp = 0.0
majflt_tmp = 0.0
vsz_tmp = 0.0
rss_tmp = 0.0
totalmem_tmp = 0.0

def init():
    global current_time, usrcpu_tmp, syscpu_tmp, guestcpu_tmp, totalcpu_tmp, minflt_tmp, majflt_tmp, vsz_tmp, rss_tmp, totalmem_tmp
    
    current_time = -1
    usrcpu_tmp = 0.0
    syscpu_tmp = 0.0
    guestcpu_tmp = 0.0
    totalcpu_tmp = 0.0
    minflt_tmp = 0.0
    majflt_tmp = 0.0
    vsz_tmp = 0.0
    rss_tmp = 0.0
    totalmem_tmp = 0.0

def printLine():
    global current_time, usrcpu_tmp, syscpu_tmp, guestcpu_tmp, totalcpu_tmp, minflt_tmp, majflt_tmp, vsz_tmp, rss_tmp, totalmem_tmp
    
    print(str(current_time) + ',' + str(usrcpu_tmp) + ',' + str(syscpu_tmp) + ',' + str(guestcpu_tmp) + ',' + str(totalcpu_tmp) + ',,' + str(minflt_tmp) + ',' + str(majflt_tmp) + ',' + str(vsz_tmp) + ',' + str(rss_tmp) + ',' + str(totalmem_tmp))




# Read results from files
init()

f = open(filename,'r')

print("time[msc],usrcpu[%],syscpu[%],guestcpu[%],totalcpu[%],minflt/s,majfit/s,vsz,rss,totalmem[%]")

for line in f:
    line = line.replace('\n', '')
    m = re.match(r"^ [0-9]", line)
    if m == None: 
        continue
    columns = line.split()
    runtime = int(columns[0])
    uuid = int(columns[1])
    pid = int(columns[2])
    usrcpu = float(columns[3])
    syscpu = float(columns[4])
    guestcpu = float(columns[5])
    totalcpu = float(columns[6])
    numcpu = float(columns[7])
    minflt = float(columns[8])
    majflt = float(columns[9])
    vsz = float(columns[10])
    rss = float(columns[11])
    totalmem = float(columns[12])


    if current_time == -1:
        current_time = runtime 

    if current_time != runtime:
        printLine()
        init()
        current_time = runtime 

    usrcpu_tmp += usrcpu
    syscpu_tmp += syscpu
    guestcpu_tmp += guestcpu
    totalcpu_tmp += totalcpu
    minflt_tmp += minflt
    majflt_tmp += majflt
    vsz_tmp += vsz
    rss_tmp += rss
    totalmem_tmp += totalmem 

printLine()
