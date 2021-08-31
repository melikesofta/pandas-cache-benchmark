import matplotlib.pyplot as plt
import numpy as np


def plot():
    labels = ['redis-pyarrow', 'pickle', 'csv', 'hdf']
    small_writes = [0.011252880096435547, 0.0009887218475341797,
                    0.060813188552856445, 0.17034006118774414]
    small_reads = [0.0033261775970458984, 0.0005431175231933594,
                   0.013083934783935547, 0.006501913070678711]
    big_writes = [0.7082719802856445, 0.40320301055908203,
                  56.73444390296936, 0.16461515426635742]
    big_reads = [1.0988080501556396, 0.3689420223236084,
                 6.29616117477417, 0.990962028503418]

    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - 3 * width / 4, small_writes,
                    width / 2, label='Writes (small data)')
    rects2 = ax.bar(x - width / 4, small_reads,
                    width / 2, label='Reads (small data)')
    rects3 = ax.bar(x + width / 4, big_writes,
                    width / 2, label='Writes (big data)')
    rects4 = ax.bar(x + 3 * width / 4, big_reads,
                    width / 2, label='Reads (big data)')

    ax.set_ylabel('Duration (s)')
    ax.set_title('Benchmarks for caching pandas DFs')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    plot()
