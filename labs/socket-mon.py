from collections import defaultdict
import csv
import psutil

connections = psutil.net_connections()
countPid = defaultdict(int)
socketList = defaultdict(list)

for conn in connections:
    if (conn[3] and conn[4] and  conn[3][0].find("::") == -1 and conn[4][0].find("::") == -1):
        laddr = conn[3][0] + "@" + str(conn[3][1])
        raddr = conn[4][0] + "@" + str(conn[4][1])
        status = conn[5]
        pid = conn[6]
        data = pid, laddr, raddr, status
        socketList[pid].append(data)
        countPid[pid] += 1

# sorted the countPid dictionary based on the number of connections in descending order
sorted_countPid = [pid for pid, counter in sorted(countPid.items(), key=lambda x: x[1], reverse=True)]

csvfile = open('socket-mon.csv', 'wb')
fieldNames = ["pid","laddr","raddr","status"]
writer = csv.writer(csvfile, quoting = csv.QUOTE_ALL)
writer.writerow(fieldNames)

for pid in sorted_countPid:
    for s in socketList[pid]:
        writer.writerow(s)

