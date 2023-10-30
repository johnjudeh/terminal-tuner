from audio.pitch.dft import plot_dft, calculate_note
from audio.parsers import numpy_array_from_wave_file, numpy_array_from_frames
import numpy as np
from audio.constants import STANDARD_FRAME_RATE

sample_size_s = 0.5


def _test_samples_of_file_are_note_accurate(
    filename: str,
    sample_size_s: float,
) -> None:
    audio_data = numpy_array_from_wave_file(filename)
    num_of_samples = len(audio_data) / (STANDARD_FRAME_RATE * sample_size_s)
    samples = np.array_split(audio_data, num_of_samples)
    for sample in samples:
        print(calculate_note(sample))
        plot_dft(sample)


_test_samples_of_file_are_note_accurate("examples/B_untrimmed.wav", sample_size_s)
