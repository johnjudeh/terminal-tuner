"""
The wave file format is a linear pulse-code modulation (LPCM) bitstream format.
It is also an application of the Resource Interchange File Format.

PCM is a method of digitally representing analog signals. It works by sampling the amplitude
of a continuous signal at specific time interval and quantizing it to the nearest digital
value available. Linear PCM is a specific method of PCM where the quantized values are linearly
uniform.
"""
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from typing import Union, Tuple

CHUNK = 1024
LOWEST_AUDIBLE_FREQUENCY = 20
HIGHEST_AUDIBLE_FREQUENCY = 20_000
SPEED_OF_SOUND_IN_AIR = 344 #m/s
STANDARD_FRAME_RATE = 44_100

# frames = frame_rate x time
# therefore time = frame_rate / frames
# velocity = frequency x wavelength
# frequency = wavelengths per second

def plot_graph(x: np.array, y: np.array) -> None:
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.scatter(x, y, s=15)
    plt.show()

def plot_frames(frames: bytes, channels: int = 2, sample_width = 2) -> None:
    x, y = [], []
    step = sample_width * channels
    for f in range(0, len(frames), step):
        value = int.from_bytes(frames[f:f+sample_width], byteorder="little", signed=True)
        x.append(f // step)
        y.append(value)
    plot_graph(x, y)

def read_wave_file(filename: str) -> Tuple[bytes, wave._wave_params]:
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
    return frames, wf.getparams()

def plot_wave_file(filename: str) -> None:
    frames, params = read_wave_file(filename)
    plot_frames(frames, channels=params.nchannels, sample_width=params.sampwidth)

def to_hexadecimal_bytes(num: np.float64) -> bytes:
    num = int(num)
    try:
        return num.to_bytes(2, byteorder="little", signed=True)
    except OverflowError:
        raise OverflowError(f"{num=}")

assert to_hexadecimal_bytes(32_767) == b"\xff\x7f"
assert to_hexadecimal_bytes(0.0) == b"\x00\x00"

def quantize(num: Union[float, np.ndarray], min_num: float, max_num: float, num_of_bytes: int = 2) -> int:
    max_quantized_num = 2 ** (num_of_bytes * 8 - 1) - 1
    num_range = max_num - min_num
    # Assumes numbers are centered around 0
    denom = num_range if min_num >= 0 else num_range / 2
    quantized = (num / denom) * max_quantized_num
    return quantized.round() if isinstance(quantized, np.ndarray) else round(quantized)

assert quantize(1.0, min_num=-1, max_num=1) == 32_767
# A little wrong but close enough (should be -32_768)
assert quantize(-1.0, min_num=-1, max_num=1) == -32_767

def create_sound_wave(frequency: int, frame_rate: int, channels: int = 1) -> bytes:
    if channels > 1:
        raise ValueError
    x = np.linspace(0, 2 * np.pi, frame_rate)
    y = np.sin(frequency * x)
    y = quantize(y, min_num=-1, max_num=1)
    y = y // 8
    print(y)
    frames = b"".join(map(to_hexadecimal_bytes, y))
    return frames

def make_sound(frequency: int) -> None:
    p = pyaudio.PyAudio()
    with wave.open("sample.wav", "rb") as wf:
        audio_stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=1,
            rate=wf.getframerate(),
            output=True
        )
        frames = create_sound_wave(frequency, wf.getframerate())
        audio_stream.write(frames)
        audio_stream.close()
        plot_frames(frames, channels=1)


def calculate_pitch(frames: bytes, frame_rate: int, channels: int = 1, sample_width: int = 2) -> int:
    # Mark each peak of the wave
    peaks = []
    step = sample_width * channels

    peak_start = None
    peak_end = None
    last_value = None
    is_rising = None

    def set_is_rising(current_value: int, last_value: int) -> bool:
        if current_value > last_value:
            return True
        elif current_value < last_value:
            return False

    for f in range(step, len(frames), step):
        current_value = int.from_bytes(frames[f:f+sample_width], byteorder="little", signed=True)

        if last_value is None:
            last_f = f - step
            last_value = int.from_bytes(frames[last_f:last_f+sample_width], byteorder="little", signed=True)

        if is_rising is None or is_rising is False:
            # When the values are falling, we want to change is_rising
            # before the next conditional block. When the values are
            # rising, we want to change it after the conditional block
            # so that we can record the peak end
            is_rising = set_is_rising(current_value, last_value) or is_rising

        if is_rising:
            if current_value > last_value:
                # We might be at a peak
                peak_start = f // step

            elif current_value < last_value:
                # Confirms we were at a peak
                peak_end = (f - step) // step
                peak_mid = round(peak_start + (peak_end - peak_start) / 2)
                peaks.append(peak_mid)

        # print(f // step, last_value, current_value, is_rising, peak_start, peak_end)

        if current_value != last_value:
            is_rising = set_is_rising(current_value, last_value)
            last_value = current_value

    print(peaks[-10:])

    if len(peaks) == 0:
        raise ValueError("Frames has no peaks to calculate pitch")

    # Calculate the distance between each peak in frames
    frames_wave_lengths = []
    for i, peak_mid in enumerate(peaks):
        if i == 0:
            continue
        frames_wave_length = peak_mid - peaks[i - 1]
        frames_wave_lengths.append(frames_wave_length)
    print(frames_wave_lengths[-10:])

    # Convert wavelength in frames to wavelength in seconds
    frequencies = []
    for frames_wave_length in frames_wave_lengths:
        seconds_wave_length = frames_wave_length / frame_rate
        frequency = 1 / seconds_wave_length
        frequencies.append(frequency)
    print(frequencies[-10:])
    print(Counter(list(map(lambda x: round(x, 2), frequencies))))

    # Average frequency
    avg_frequency = sum(frequencies) / len(frequencies)

    # Return
    return avg_frequency

if __name__ == "__main__":
    # make_sound(frequency=440)
    # frames = create_sound_wave(frequency=440, frame_rate=STANDARD_FRAME_RATE)
    # frequency = calculate_pitch(frames, STANDARD_FRAME_RATE)
    # print(f"Frequency (Hz): {frequency}")
    # assert round(frequency) == 440
    # plot_frames(frames, channels=1)

    frames, params = read_wave_file("examples/A.wav")
    # frames, params = read_wave_file("examples/82.407.wav")
    frequency = calculate_pitch(
        frames,
        frame_rate=params.framerate,
        channels=params.nchannels,
        sample_width=params.sampwidth
    )
    print(f"Frequency (Hz): {frequency}")

    plot_frames(frames, channels=params.nchannels, sample_width=params.sampwidth)
