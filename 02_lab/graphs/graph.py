import matplotlib.pyplot as plt
from sage.all import srange, floor, ceil
import seaborn as sns
import pandas as pd
from timing import ts, t_succ
from sys import argv


def get_plot(ylabel, unit, unitbound, threadbound, filename, all_ts, ymax, cores=8):
    plt.clf()
    datalen = threadbound

    sns.set_style("darkgrid")
    plt.rc("axes", titlesize=18)
    plt.rc("axes", labelsize=14)
    plt.rc("xtick", labelsize=7)
    plt.rc("ytick", labelsize=8)
    plt.rc("legend", fontsize=12)
    plt.rc("font", size=13)

    sns.color_palette("bright")

    p = sns.lineplot(x="Threads", y=ylabel, hue="Type", marker=".", data=all_ts)
    p.set_xlabel("Threads, num", fontsize=14)
    p.set_ylabel(f"{ylabel}, {unit}", fontsize=14)

    l1 = p.lines[0]
    x1 = l1.get_xydata()[:, 0]
    y1 = l1.get_xydata()[:, 1]
    p.fill_between(x1, y1, color="blue", alpha=0.1)

    l2 = p.lines[1]
    x1 = l2.get_xydata()[:, 0]
    y1 = l2.get_xydata()[:, 1]
    p.fill_between(x1, y1, color="orange", alpha=0.04)

    p.margins(x=0, y=0)

    step = 2
    p.set_xticks(srange(0, datalen + 1, step))
    p.set_xticklabels([str(x) for x in srange(0, datalen + 1, step)])

    step = unitbound / 10
    p.set_yticks(srange(0, unitbound + step + 0.5, step))
    p.set_yticklabels(
        [str(floor(100 * x) / 100.0) for x in srange(0, unitbound + step + 0.5, step)]
    )

    m1 = srange(0, unitbound + step + 0.5, step)[-1]
    m2 = ymax
    m1, m2 = max(m1, m2), min(m1, m2)

    p.axvline(x=cores, ymin=0, ymax= m2 / m1, color="green", linestyle="-", label="cores")

    p.figure.savefig(filename)


threadbound = 16
cores = 8
ts = ts[:threadbound]
t_succ = ts[0][1]

ts = [[x[0], x[1] * 1000] for x in ts]

ts_ds = [[x[0], x[1], "Real"] for x in ts]
acc_ds = [[x[0], t_succ * 1000 / x[1], "Real"] for x in ts]
eff_ds = [[x[0], x[1] / x[0], "Real"] for x in acc_ds]

exp_ts = [[i, t_succ * 1000 / i, "Expected"] for i in range(1, cores + 1)] + [
    [i, t_succ * 1000 / cores, "Expected"] for i in range(cores + 1, threadbound + 1)
]
exp_acc = [[i, i, "Expected"] for i in range(1, cores + 1)] + [
    [i, cores, "Expected"] for i in range(cores + 1, threadbound + 1)
]
exp_eff = [[i, 1, "Expected"] for i in range(1, cores + 1)] + [
    [i, cores / i, "Expected"] for i in range(cores + 1, threadbound + 1)
]

columns = ["Threads", "AvgTime", "Type"]
got_ts_df = pd.DataFrame(ts_ds, columns=columns)
exp_ts_df = pd.DataFrame(exp_ts, columns=columns)
all_ts = pd.concat([got_ts_df, exp_ts_df])
unitbound = int(ceil(max([x[1] for x in ts])))
get_plot("AvgTime", "ms", unitbound, threadbound, argv[1], all_ts, max(ts_ds[0][1], exp_ts[0][1]))

columns = ["Threads", "Acceleration", "Type"]
got_acc_df = pd.DataFrame(acc_ds, columns=columns)
exp_acc_df = pd.DataFrame(exp_acc, columns=columns)
all_ts = pd.concat([got_acc_df, exp_acc_df])
unitbound = max(
    int(ceil(max([x[1] for x in acc_ds]))), int(ceil(max([x[1] for x in exp_acc])))
)
get_plot("Acceleration", "times", unitbound, threadbound, argv[2], all_ts, max(acc_ds[cores-1][1], exp_acc[cores-1][1]))

columns = ["Threads", "Efficiency", "Type"]
got_eff_df = pd.DataFrame(eff_ds, columns=columns)
exp_eff_df = pd.DataFrame(exp_eff, columns=columns)
all_ts = pd.concat([got_eff_df, exp_eff_df])
unitbound = int(ceil(max([x[1] for x in eff_ds])))
get_plot("Efficiency", "thread^-1", unitbound, threadbound, argv[3], all_ts, max(eff_ds[0][1], exp_eff[0][1]))
