import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")

n_cpu = 8

dataset = []
with open("trace.txt", "r") as f:
    for _ in range(12):
        line = list(map(float, f.readline().split(";")))
        dataset.append(line)
        
for i in range(len(dataset)):
    line = dataset[i]
    line.sort()
    line = line[10:-10]
    dataset[i] = line

sns.set(rc={'figure.figsize':(12,8)})

data = []
for i, line in enumerate(dataset):
    data.append([i+1, (sum(line)/len(line))*1000, "Real"])
saved = data.copy()
data1 = data
data_df = pd.DataFrame(data, columns=["Threads", "AvgTime", "Type"])
for i in range(1, len(data1)): 
    if i > n_cpu:
        data1[i] = [data1[i][0], data1[0][1] / data1[n_cpu][0], "Perfect"]
    else:
        data1[i] = [data1[i][0], data1[0][1] / data1[i][0], "Perfect"]

data1[0][2] = "Perfect"
# pdf = pd.DataFrame(data1, columns=["Threads", "AvgTime"])
data1 = pd.DataFrame(data1, columns=["Threads", "AvgTime", "Type"])
all_data = pd.concat([data1, data_df])

p = sns.lineplot(x="Threads", y="AvgTime", hue="Type", marker="o", data=all_data)
p.set_xlabel("Threads, num", fontsize = 16)
p.set_ylabel("AvgTime, ms", fontsize = 16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]

p.fill_between(x1, y1, color="blue", alpha=0.1)
l2 = p.lines[1]

x2 = l2.get_xydata()[:, 0]
y2 = l2.get_xydata()[:, 1]

p.fill_between(x2, y2, color="orange", alpha=0.05)
p.margins(x=0, y=0)
_ = p.set_xticks(range(0, 13))
_ = p.set_xticklabels(str(i) for i in range(0, 13))
_ = p.set_yticks(range(0, 350, 25))
_ = p.set_yticklabels([str(i) for i in range(0, 350, 25)])
_ = p.axvline(x=4, ymax=0.225, color="red", alpha=0.8)

plt.savefig("target/avgtime.png")
plt.clf()


accceleration = [0] * 12
for i in range(0, len(accceleration)):
    accceleration[i] = [saved[i][0], saved[0][1]/saved[i][1]]

a_df = pd.DataFrame(accceleration, columns=["Threads", "Times Speed"])
p = sns.lineplot(x="Threads", y="Times Speed", marker="o", data=a_df, color='g')
p.set_xlabel("Threads, num", fontsize = 16)
p.set_ylabel("Times Speed, times", fontsize = 16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]

_ = p.fill_between(x1, y1, color="green", alpha=0.3)
_ = p.axvline(x=4, ymin=0.043 ,ymax=0.95, color="red", alpha=0.8)

plt.savefig("target/acceleration.png")
plt.clf()

per_thread = [0] * 12
for i in range(0, len(per_thread)):
    per_thread[i] = [accceleration[i][0], accceleration[i][1]/accceleration[i][0]]
thr_df = pd.DataFrame(per_thread, columns=["Threads", "EfficencyPerThread"])
p = sns.lineplot(x="Threads", y="EfficencyPerThread", marker="o", data=thr_df, color='b')
p.set_xlabel("Threads, num", fontsize = 16)
p.set_ylabel("EfficencyPerThread, times", fontsize = 16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]

_ = p.fill_between(x1, y1, color="cyan", alpha=0.1)
_ = p.axvline(x=4, ymin=0.043 ,ymax=0.62, color="red", alpha=0.8)

plt.savefig("target/efficiency.png")
