import seaborn as sns
import pandas as pd
import subprocess
import psutil
import matplotlib.pyplot as plt
import os


def get_n_cores():
    return psutil.cpu_count()


def run_target(n_threads, random_seed, n_times):
    cmd = f"target/main {n_threads} {random_seed} {n_times}"
    proc = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    if proc.returncode != 0:
        raise RuntimeError(f"Command {cmd} failed")

    raw = proc.stdout.decode().strip().split("\n")
    data = [float(entry.strip()) for entry in raw]
    return data


def benchmark(max_threads: int) -> pd.DataFrame:
    if "bench.pickle" in os.listdir("target"):
        return pd.read_pickle("target/bench.pickle")

    df = pd.DataFrame(columns=["n_threads", "result"])
    for n_threads in range(1, max_threads + 1):
        run_res = run_target(n_threads, 31337, 20)

        new_df = pd.DataFrame(
            {"n_threads": [n_threads] * len(run_res), "result": run_res}
        )
        df = pd.concat(
            [
                df,
                new_df,
            ]
        )

    df["n_threads"] = df["n_threads"].astype(int)
    df["result"] = df["result"].astype(float)
    df["result"] = df["result"].apply(lambda x: x * 1000)

    df.to_pickle("target/bench.pickle")

    return df


def create_perfect_data(one_thread_average: float, max_threads: int) -> pd.DataFrame:
    df = pd.DataFrame(columns=["n_threads", "result"])
    for n_threads in range(1, max_threads + 1):
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        "n_threads": [n_threads],
                        "result": [one_thread_average / n_threads],
                    }
                ),
            ]
        )
    df["n_threads"] = df["n_threads"].astype(int)
    df["result"] = df["result"].astype(float)
    return df


def render_threads(
    actual_data: pd.DataFrame,
    max_threads: int,
    one_thread_average: float,
):
    perfect_data = create_perfect_data(one_thread_average, max_threads)
    sns.set_theme(style="darkgrid")

    # create line plot with average data

    fig, ax = plt.subplots(figsize=(7, 7))

    sns.lineplot(data=perfect_data, x="n_threads", y="result", label="expected", ax=ax)
    plot = sns.lineplot(
        data=actual_data, x="n_threads", y="result", label="actual", ax=ax
    )

    # styling

    plot.margins(x=0, y=0)
    plot.set_xticks(range(0, max_threads))
    plot.set_yticks(range(0, int(one_thread_average) + 5))

    plot.set_xlabel("Threads, num", fontsize=16)
    plot.set_ylabel("AvgTime, ms", fontsize=16)

    plot.axvline(x=get_n_cores(), color="red", linestyle="--", label="cores")

    # save plot
    fig.savefig("target/threads.png")


def get_acceleration(data: pd.DataFrame):
    one_thread_average = data[data["n_threads"] == 1]["result"].mean()
    data["acceleration"] = one_thread_average / data["result"]
    return data


def get_expected_acceleration(max_threads: int):
    df = pd.DataFrame(columns=["n_threads", "acceleration"])
    for n_threads in range(1, max_threads + 1):
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    {
                        "n_threads": [n_threads],
                        "acceleration": [n_threads],
                    }
                ),
            ]
        )

    df["n_threads"] = df["n_threads"].astype(int)
    df["acceleration"] = df["acceleration"].astype(float)
    return df


def render_acceleration(actual_data: pd.DataFrame, max_threads: int):
    sns.set_theme(style="darkgrid")

    fig, ax = plt.subplots(figsize=(7, 7))

    data = get_acceleration(actual_data)
    expected = get_expected_acceleration(max_threads)
    sns.lineplot(
        data=expected, x="n_threads", y="acceleration", label="expected", ax=ax
    )
    plot = sns.lineplot(
        data=data, x="n_threads", y="acceleration", ax=ax, label="actual"
    )

    # styling
    plot.margins(x=0, y=0)
    plot.set_xticks(range(0, max_threads))
    plot.set_yticks(range(0, 5))

    plot.set_xlabel("Threads, num", fontsize=16)
    plot.set_ylabel("Acceleration, times", fontsize=16)

    # save plot
    fig.savefig("target/acceleration.png")


def render_efficiency(actual_data: pd.DataFrame, max_threads: int):
    sns.set_theme(style="darkgrid")

    fig, ax = plt.subplots(figsize=(7, 7))

    data["efficiency"] = data["acceleration"] / data["n_threads"]
    expected = get_expected_acceleration(max_threads)
    expected["efficiency"] = expected["acceleration"] / expected["n_threads"]
    sns.lineplot(data=expected, x="n_threads", y="efficiency", label="expected", ax=ax)
    plot = sns.lineplot(data=data, x="n_threads", y="efficiency", ax=ax, label="actual")

    # styling
    plot.margins(x=0, y=0)
    plot.set_xticks(range(0, max_threads))
    plot.set_yticks(range(0, 5))

    plot.set_xlabel("Threads, num", fontsize=16)
    plot.set_ylabel("Efficiency, times", fontsize=16)

    # save plot
    fig.savefig("target/efficiency.png")


if __name__ == "__main__":
    max_threads = 20
    data = benchmark(max_threads)
    one_thread_average = data[data["n_threads"] == 1]["result"].mean()

    render_threads(data, max_threads, one_thread_average)
    render_acceleration(data, max_threads)
    render_efficiency(data, max_threads)
