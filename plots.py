import pylab as pt
from datetime import datetime
from trials import *


# Generate plots of system time vs clock speed to visualize the clock synchronization
def get_time( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return float(s[start:end].strip())
        # return datetime.strptime(s[start:end].strip(), '%a, %d %b %Y %H:%M:%S %f')
    except ValueError:
        return ""

# Parse log files and generate plots; plots are .png and titled based on speed and operation configurations
def plot_clocks(trial,speeds,probs):
    speeds = [str(i) for i in speeds]
    probs = [str(i) for i in probs]
    with open("trial%d/log_0.log"%trial) as f0, open("trial%d/log_1.log"%trial) as f1, open("trial%d/log_2.log"%trial) as f2:
        pt.figure(1, figsize=(6, 6))
        content0 = f0.readlines()
        content1 = f1.readlines()
        content2 = f2.readlines()
        contents = [content0,content1,content2]
        for i, content in enumerate(contents):
            data = [(get_time(line,"System Time","|"), int(line.split("Logical Clock")[1].strip())) for line in content]
            times = [packet[0] for packet in data]
            clocks = [packet[1] for packet in data]
            pt.step(times,clocks, label="Speed (%s)" % (speeds[i]))
        pt.grid(True)
        pt.xlabel('time (s)')
        pt.ylabel('Logical Clock Value')
        pt.title('Clock Comparison, Speeds (%s), Probabilities (%s)' % (",".join(speeds), ",".join(probs)))
        pt.legend(loc=2)
        pt.savefig('speeds%s_probs%s.png' % ("_".join(speeds), "_".join(probs)))

trial = 0
for speeds in all_speeds:
    for probs in all_probs:
        pt.clf()
        plot_clocks(trial,speeds,probs)
        trial += 1
