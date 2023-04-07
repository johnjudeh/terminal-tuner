from audio.utils import find_nearest_note
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
import numpy as np


def calculate_pitch(filename: str) -> str:
    frame_rate, audio_data = wavfile.read(filename)
    sample_size = len(audio_data)

    # Use a Discrete Fourier Transform to find the frequencies that
    # make up this audio data. Throwing away negative half.
    x_freq = fftfreq(sample_size, 1 / frame_rate)[: sample_size // 2]
    y_freq = fft(audio_data)[: sample_size // 2]
    y_freq = np.abs(y_freq)

    # Finding the top N frequencies in the DFT spectrum
    # TODO: Keep as np array, converted to list for speed
    n = 20
    top_frequency_indices = np.argpartition(y_freq, -n)[-n:]
    top_frequencies = list(
        zip(x_freq[top_frequency_indices], y_freq[top_frequency_indices])
    )
    top_frequencies.sort(reverse=True, key=lambda x: x[1])

    # Discarding any duplicate clustered frequencies keeping only the
    # strongest signals.
    min_diff = 2
    top_magnitude = top_frequencies[0][1]

    # Somewhat arbitrary looking at the data
    min_magnitude = top_magnitude / 5

    cleaned_top_frequencies = []

    for freq, magnitude in top_frequencies:
        if magnitude < min_magnitude:
            break
        if cleaned_top_frequencies:
            for tf in cleaned_top_frequencies:
                if abs(tf - freq) < min_diff:
                    break
            else:
                cleaned_top_frequencies.append(freq)
        else:
            cleaned_top_frequencies.append(freq)

    # Choose the lowest frequency. Since strings vibrate at frequencies
    # that can form standing waves, the base frequency will be the lowest
    # and all higher frequencies will be overtones.
    # TODO: this assumes there are no stray frequencies in the mix such as the
    # mains hum or other electrical noise. Change this to account for this
    cleaned_top_frequencies.sort()
    lowest_frequency = cleaned_top_frequencies[0]
    return find_nearest_note(lowest_frequency)


print(calculate_pitch("examples/E.wav"))
print(calculate_pitch("examples/A.wav"))
print(calculate_pitch("examples/D.wav"))
print(calculate_pitch("examples/G.wav"))
print(calculate_pitch("examples/B.wav"))
print(calculate_pitch("examples/e_high.wav"))
