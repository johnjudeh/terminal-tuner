from audio.utils import find_nearest_note
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
import numpy as np
from math import ceil
from typing import Optional


def _find_base_frequency(frequencies: list[float]) -> Optional[float]:
    """
    Given a list of frequencies, finds the base frequency and returns it. Because
    strings vibrate at frequencies that can form standing waves, the base frequency
    will be the lowest frequency where other major frequencies are multiples of it
    (overtones). This function finds the lowest frequency where the majority of the
    other frequencies are multiples of that (within a certain threshold)
    """
    MULTIPLE_THRESHOLD = 0.05
    majority_of_frequencies = ceil(len(frequencies) / 2)
    cleaned_frequencies = sorted(frequencies)

    while True:
        if len(cleaned_frequencies) == 0:
            return None

        base_freq_candidate = cleaned_frequencies[0]

        factored_frequencies = [f / base_freq_candidate for f in cleaned_frequencies]
        factored_frequencies_errors = [abs(f - round(f)) for f in factored_frequencies]
        count_of_passing_frequencies = sum(
            1 if f <= MULTIPLE_THRESHOLD else 0 for f in factored_frequencies_errors
        )
        if count_of_passing_frequencies >= majority_of_frequencies:
            return base_freq_candidate
        else:
            cleaned_frequencies.remove(base_freq_candidate)


def calculate_pitch(filename: str) -> str:
    """
    Given a wave file with a musical string being played, finds the pitch of the of
    the note it's tuned to. Uses the Discrete Fourier Transform (DFT) method to
    identify which sine and cosine waves make up the discrete repeating function
    passed to it. From there, it shows the frequencies of those componenets, from
    which we can calculate the base frequency which is the string being played.
    """
    frame_rate, audio_data = wavfile.read(filename)
    sample_size = len(audio_data)

    # Use a Discrete Fourier Transform to find the frequencies components of
    # this audio data, throwing away negative half.
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

    base_frequency = _find_base_frequency(cleaned_top_frequencies)
    base_note = find_nearest_note(base_frequency) if base_frequency else None
    return base_note
