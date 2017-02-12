"""
Question:
Pick one IP from each region, find network latency from via the below code snippet
(ping 3 times), and finally sort regions by the average latency.
http://ec2-reachability.amazonaws.com/
Sample output:
1. us-west-1 [50.18.56.1] - Smallest average latency
2. xx-xxxx-x [xx.xx.xx.xx] - x
3. xx-xxxx-x [xx.xx.xx.xx] - x
...
15. xx-xxxx-x [xx.xx.xx.xx] - Largest average latency
"""
import subprocess
import re
import operator

hosts = { 
	"us-east-1": "23.23.255.255",
	"us-east-2": "52.14.64.0",
	"us-west-1": "50.18.56.1",
	"us-west-2": "35.160.63.253",
	"us-gov-west-1": "52.222.9.163",
	"ca-central-1": "52.60.50.0",
	"eu-west-1": "34.248.60.213",
	"eu-west-2": "52.56.34.0",
	"eu-central-1": "35.156.63.252",
	"ap-northeast-1": "13.112.63.251",
	"ap-northeast-2": "52.78.63.252",
	"ap-southeast-1": "46.51.216.14",
	"ap-southeast-2": "13.54.63.252",
	"ap-south-1": "35.154.63.252",
	"sa-east-1": "52.67.255.254",
      }

result = {}
regex = "Average = (\d+)ms"

# parse returned output from ping cmd
def parseOutput(output):
    output = output.decode('utf-8').strip().split('\r\n')[-1:]
    avgTimeText = output[0].strip().split(',')[2]
    avgTime = re.search(regex, avgTimeText)
    return int(avgTime.group(1))


# loop through all the hosts and ping them all
for key in hosts: 
    ping = subprocess.Popen(
        ["ping", "-n", "3", hosts[key]],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = ping.communicate()
    avg =  parseOutput(out)
    result[key] = avg

#sort the result in ascending order of average time
sorted_r = sorted(result.items(), key=operator.itemgetter(1))
i = 1
print("\n================== Output ==================\n")
for k, v in sorted_r:
   print(i,". ", k," [",hosts[k],"] - ",v)
   i += 1


