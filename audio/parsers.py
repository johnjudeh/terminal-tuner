import wave
from typing import Tuple


def read_wave_file(filename: str) -> Tuple[bytes, wave._wave_params]:
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
    return frames, wf.getparams()
