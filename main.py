from audio.pitch.dft import calculate_pitch
from audio.constants import (
    STANDARD_FRAME_RATE,
    STANDARD_SAMPLE_WIDTH,
    STANDARD_CHANNELS,
)
import sys
from pyaudio import PyAudio, get_format_from_width
from audio.parsers import numpy_array_from_frames
import numpy as np

KEYBOARD_INTERRUPT_EXIT_CODE = 130


def main() -> None:
    recording_time_s = 0.5
    number_of_frames = round(recording_time_s * STANDARD_FRAME_RATE)

    p = PyAudio()
    stream = p.open(
        rate=STANDARD_FRAME_RATE,
        channels=STANDARD_CHANNELS,
        format=get_format_from_width(STANDARD_SAMPLE_WIDTH),
        input=True,
    )

    try:
        while True:
            audio_data = numpy_array_from_frames(stream.read(number_of_frames))
            if np.array_equal(audio_data, np.zeros_like(audio_data)):
                print("No input data")
            else:
                note = calculate_pitch(audio_data)
                print(note if note else "No note found")

    except KeyboardInterrupt as exc:
        stream.close()
        p.terminate()
        raise exc


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(KEYBOARD_INTERRUPT_EXIT_CODE)
