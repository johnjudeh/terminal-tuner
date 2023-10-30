from audio.pitch.utils import find_nearest_note, find_note_frequency, find_steps_away
from scipy.fft import rfft, fftfreq
import numpy as np
from math import ceil
from typing import Tuple
from audio.constants import STANDARD_FRAME_RATE
from graph import plot_graph


def _find_num_of_perfect_factorizations(frequencies: list[float], factor: float) -> int:
    MULTIPLE_THRESHOLD = 0.05
    factored_frequencies = [f / factor for f in frequencies]
    factored_frequencies_errors = [abs(f - round(f)) for f in factored_frequencies]
    count_of_perfect_factorizations = sum(
        1 if f <= MULTIPLE_THRESHOLD else 0 for f in factored_frequencies_errors
    )
    return count_of_perfect_factorizations


def _find_fundamental_frequency(frequencies: list[float]) -> float | None:
    """
    Given a list of frequencies, finds the base frequency and returns it. Because
    strings vibrate at frequencies that can form standing waves, the base frequency
    will be the lowest frequency where other major frequencies are multiples of it
    (overtones). This function finds the lowest frequency where the majority of the
    other frequencies are multiples of that (within a certain threshold)
    """
    ELECTRICAL_HUM = 50
    ELECTRICAL_HUM_THRESHOLD = 5
    majority_of_frequencies = ceil(len(frequencies) / 2)
    cleaned_frequencies = sorted(frequencies)

    while True:
        if len(cleaned_frequencies) < majority_of_frequencies:
            return None

        fundamental_freq_candidate = cleaned_frequencies[0]
        # Occasionally we have a missing note which is the true note being played.
        # Trying a ghost frequency before discarding a base_freq_candidate will help
        # us see this if that missing note is half the base_freq_candidate. E.g. G3
        ghost_freq = fundamental_freq_candidate / 2

        fundamental_freq_factorization_count = _find_num_of_perfect_factorizations(
            cleaned_frequencies, fundamental_freq_candidate
        )
        ghost_freq_factorization_count = _find_num_of_perfect_factorizations(
            cleaned_frequencies, ghost_freq
        )

        ghost_freq_passes = ghost_freq_factorization_count >= majority_of_frequencies
        fundamental_freq_passes = (
            fundamental_freq_factorization_count >= majority_of_frequencies
        )

        # This covers the rare case that the electrical hum is in fact a
        # factor of the overtones. This is rare but happens for D3.
        def is_electircal_hum(freq: float) -> bool:
            return abs(freq - ELECTRICAL_HUM) <= ELECTRICAL_HUM_THRESHOLD

        if (
            fundamental_freq_passes
            and not is_electircal_hum(fundamental_freq_candidate)
        ) or (ghost_freq_passes and not is_electircal_hum(ghost_freq)):
            if fundamental_freq_factorization_count >= ghost_freq_factorization_count:
                return fundamental_freq_candidate
            else:
                return ghost_freq
        else:
            cleaned_frequencies.remove(fundamental_freq_candidate)


def calculate_dft(
    audio_data: np.ndarray, frame_rate: int = STANDARD_FRAME_RATE
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Use a Discrete Fourier Transform to find the frequencies components of
    this audio data, throwing away negative half.
    """
    sample_size = len(audio_data)
    x_freq = fftfreq(sample_size, 1 / frame_rate)[: sample_size // 2]
    y_freq = rfft(audio_data)[: sample_size // 2]
    y_freq = np.abs(y_freq)
    return x_freq, y_freq


def plot_dft(audio_data: np.ndarray, frame_rate: int = STANDARD_FRAME_RATE) -> None:
    x_freq, y_freq = calculate_dft(audio_data, frame_rate)
    plot_graph(x_freq, y_freq, xlim=(0, 1000))


def calculate_note(
    audio_data: np.ndarray, frame_rate: int = STANDARD_FRAME_RATE
) -> Tuple[str, float]:
    """
    Given a wave file with a musical string being played, finds the pitch of the of
    the note it's tuned to. Uses the Discrete Fourier Transform (DFT) method to
    identify which sine and cosine waves make up the discrete repeating function
    passed to it. From there, it shows the frequencies of those componenets, from
    which we can calculate the base frequency which is the string being played.
    """
    x_freq, y_freq = calculate_dft(audio_data, frame_rate)

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
    min_diff = 10
    top_magnitude = top_frequencies[0][1]

    # Somewhat arbitrary looking at the data
    min_magnitude = top_magnitude / 8

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

    fundamental_frequency = _find_fundamental_frequency(cleaned_top_frequencies)
    nearest_note = (
        find_nearest_note(fundamental_frequency) if fundamental_frequency else None
    )
    steps_away = (
        find_steps_away(fundamental_frequency, find_note_frequency(nearest_note))
        if nearest_note
        else None
    )
    return nearest_note, steps_away
