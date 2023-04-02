import pyaudio
import numpy as np
from typing import Union
from graph import plot_frames
from audio.constants import STANDARD_FRAME_RATE, STANDARD_SAMPLE_WIDTH


def _to_hexadecimal_bytes(num: np.float64) -> bytes:
    num = int(num)
    try:
        return num.to_bytes(2, byteorder="little", signed=True)
    except OverflowError:
        raise OverflowError(f"{num=}")


def _quantize(
    num: Union[float, np.ndarray], min_num: float, max_num: float, num_of_bytes: int = 2
) -> int:
    max_quantized_num = 2 ** (num_of_bytes * 8 - 1) - 1
    num_range = max_num - min_num
    # Assumes numbers are centered around 0
    denom = num_range if min_num >= 0 else num_range / 2
    quantized = (num / denom) * max_quantized_num
    return quantized.round() if isinstance(quantized, np.ndarray) else round(quantized)


def create_sound_wave(
    frequency: int, frame_rate: int = STANDARD_FRAME_RATE, channels: int = 1
) -> bytes:
    if channels > 1:
        raise ValueError
    x = np.linspace(0, 2 * np.pi, frame_rate)
    y = np.sin(frequency * x)
    y = _quantize(y, min_num=-1, max_num=1)
    y = y // 8
    print(y)
    frames = b"".join(map(_to_hexadecimal_bytes, y))
    return frames


def make_sound(frequency: int) -> None:
    p = pyaudio.PyAudio()
    audio_stream = p.open(
        format=p.get_format_from_width(STANDARD_SAMPLE_WIDTH),
        channels=1,
        rate=STANDARD_FRAME_RATE,
        output=True,
    )
    frames = create_sound_wave(frequency, STANDARD_FRAME_RATE)
    audio_stream.write(frames)
    audio_stream.close()
    plot_frames(frames, channels=1)
