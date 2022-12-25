CORE_LIMIT = 16
OLD_CUT = 5
NEW_CUT = 5

# import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")

old_arr, cur_arr = [], []

with open("old_trace_n.txt", "r") as fd:
    for _ in range(CORE_LIMIT):
        line = list(map(float, fd.readline().split(";")))
        line = sorted(line)[OLD_CUT:-OLD_CUT]
        avg_value = sum(line) / len(line)
        old_arr.append(avg_value)

with open("trace_n.txt", "r") as fd:
    for i in range(CORE_LIMIT):
        line = list(map(float, fd.readline().split(";")))
        line = sorted(line)[NEW_CUT:-NEW_CUT]
        avg_value = sum(line) / len(line)
        cur_arr.append(avg_value)

# Create DataFrames
old_predf = [[index + 1, avg_time, "OpenMP"] for index, avg_time in enumerate(old_arr)]
cur_predf = [[index + 1, avg_time, "MPI"] for index, avg_time in enumerate(cur_arr)]
old_df = pd.DataFrame(old_predf, columns=["Threads", "Time", "Type"])
cur_df = pd.DataFrame(cur_predf, columns=["Threads", "Time", "Type"])

all_df = pd.concat([old_df, cur_df], ignore_index=True)
# all_df = all_df.astype({"Threads": "int", "Time": "float", "Type": "string"})

# import IPython; IPython.embed()

# Time(Thread) graph
p = sns.lineplot(x="Threads", y="Time", hue="Type", marker="o", data=all_df)
p.set_xlabel("Threads, num", fontsize=16)
p.set_ylabel("Time, sec", fontsize=16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]
_ = p.fill_between(x1, y1, color="blue", alpha=0.3)
p.margins(x=0, y=0)
_ = p.set_xticks(range(0, CORE_LIMIT + 3))
_ = p.set_xticklabels([str(i) for i in range(CORE_LIMIT + 3)])
_ = p.set_yticks([val * 0.02 for val in range(19)])

plt.savefig("speed.png", dpi=300)
plt.clf()

acceleration = [0] * CORE_LIMIT
for i in range(0, CORE_LIMIT):
    acceleration[i] = [i + 1, (cur_arr[0] / cur_arr[i])]


a_df = pd.DataFrame(acceleration, columns=["Threads", "TimesSpeed"])
p = sns.lineplot(x="Threads", y="TimesSpeed", marker="o", data=a_df, color="g")
p.set_xlabel("Threads, num", fontsize=16)
p.set_ylabel("TimesSpeed, times", fontsize=16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]

_ = p.fill_between(x1, y1, color="green", alpha=0.3)
_ = p.axvline(x=8, ymin=0.04, ymax=0.8, color="red", alpha=0.4)

plt.savefig("acceleration.png", dpi=300)
plt.clf()

# Efficiency graph

per_thread = [0] * CORE_LIMIT
for i in range(0, len(per_thread)):
    per_thread[i] = [acceleration[i][0], acceleration[i][1] / acceleration[i][0]]
thr_df = pd.DataFrame(per_thread, columns=["Threads", "EfficencyPerThread"])
p = sns.lineplot(
    x="Threads", y="EfficencyPerThread", marker="o", data=thr_df, color="b"
)
p.set_xlabel("Threads, num", fontsize=16)
p.set_ylabel("EfficencyPerThread, times", fontsize=16)
l1 = p.lines[0]

x1 = l1.get_xydata()[:, 0]
y1 = l1.get_xydata()[:, 1]

_ = p.fill_between(x1, y1, color="cyan", alpha=0.1)
_ = p.axvline(x=6, ymin=0.04, ymax=0.33, color="red", alpha=0.4)

plt.savefig("efficiency.png", dpi=300)
