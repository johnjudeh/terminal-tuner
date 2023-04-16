import matplotlib.pyplot as plt
import numpy as np
from audio.parsers import read_wave_file


def plot_graph(
    x: np.array,
    y: np.array,
    xlim: tuple | None = None,
    ylim: tuple | None = None,
) -> None:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.scatter(x, y, s=15)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    plt.show()


def plot_frames(frames: bytes, channels: int = 2, sample_width=2) -> None:
    x, y = [], []
    step = sample_width * channels
    for f in range(0, len(frames), step):
        value = int.from_bytes(
            frames[f : f + sample_width], byteorder="little", signed=True
        )
        x.append(f // step)
        y.append(value)
    plot_graph(x, y)


def plot_wave_file(filename: str) -> None:
    frames, params = read_wave_file(filename)
    plot_frames(frames, channels=params.nchannels, sample_width=params.sampwidth)
