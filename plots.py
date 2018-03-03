from pylab import *
from datetime import datetime


# Generate plots of system time vs clock speed to visualize the clock synchronization
def get_time( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return float(s[start:end].strip())
        # return datetime.strptime(s[start:end].strip(), '%a, %d %b %Y %H:%M:%S %f')
    except ValueError:
        return ""

with open("log_0.log") as f0, open("log_1.log") as f1, open("log_2.log") as f2:	
    content0 = f0.readlines()
    content1 = f1.readlines()
    content2 = f2.readlines()
    contents = [content0,content1,content2]
    for content in contents:
    	data = [(get_time(line,"System Time","|"), int(line.split("Logical Clock")[1].strip())) for line in content] 
    	times = [packet[0] for packet in data]
    	clocks = [packet[1] for packet in data]
    	step(times,clocks)

grid(True)
xlabel('time (s)')
ylabel('Logical Clock Value')
title('Logical Clock Consistency, Scale Model / CS262, Mali and Kiran')
show()