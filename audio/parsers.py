import wave
from typing import Tuple
import numpy as np
from audio.constants import STANDARD_CHANNELS


def read_wave_file(filename: str) -> Tuple[bytes, wave._wave_params]:
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
    return frames, wf.getparams()


def numpy_array_from_frames(
    frames: bytes, channels: int = STANDARD_CHANNELS
) -> np.ndarray:
    np_array = np.frombuffer(frames, dtype=np.int16)
    if channels > 1:
        np_array = np_array.reshape(
            (len(frames) // (channels * 2), channels), order="F"
        )
    return np_array


def numpy_array_from_wave_file(filename: str) -> np.ndarray:
    frames, _ = read_wave_file(filename)
    return numpy_array_from_frames(frames)
