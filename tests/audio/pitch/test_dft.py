from audio.pitch.dft import calculate_note, _find_fundamental_frequency
from audio.parsers import numpy_array_from_wave_file
from audio.constants import STANDARD_FRAME_RATE
import numpy as np


def _test_samples_of_file_are_note_accurate(
    filename: str,
    expected_note: str,
    sample_size_s: float,
) -> None:
    audio_data = numpy_array_from_wave_file(filename)
    num_of_samples = len(audio_data) / (STANDARD_FRAME_RATE * sample_size_s)
    samples = np.array_split(audio_data, num_of_samples)
    for s, sample in enumerate(samples):
        note, _ = calculate_note(sample)
        assert (
            note == expected_note
        ), f"{expected_note} not found in {filename} sample {s}/{len(samples)}"


def test_calculate_note() -> None:
    print("Testing audio.pitch.calculate_note...", end="")
    notes_to_test = [
        ("examples/E.wav", "E2"),
        ("examples/A.wav", "A2"),
        ("examples/D.wav", "D3"),
        ("examples/G.wav", "G3"),
        ("examples/B.wav", "B3"),
        ("examples/e_high.wav", "E4"),
    ]
    for filename, expected_note in notes_to_test:
        note, _ = calculate_note(numpy_array_from_wave_file(filename))
        assert note == expected_note, f"{expected_note} not found in {filename}"
        _test_samples_of_file_are_note_accurate(filename, expected_note, 1)
    print("OK")


def test_find_base_frequency() -> None:
    print("Testing audio.pitch._find_base_frequency...", end="")
    # Happy path
    assert _find_fundamental_frequency([20.0]) == 20.0
    assert _find_fundamental_frequency([20.0, 40.0, 60.0]) == 20.0
    # Sorting
    assert _find_fundamental_frequency([40.0, 20.0, 60.0]) == 20.0
    # Edge case
    assert _find_fundamental_frequency([20.0, 41.0, 61.0]) == 20.0
    assert _find_fundamental_frequency([20.0, 39.0, 59.0]) == 20.0
    # Bad frequencies
    assert _find_fundamental_frequency([18.0, 19.0, 20.0, 40.0, 60.0]) == 20.0
    assert _find_fundamental_frequency([20.0, 44.0, 68.0]) == None
    # Ghost frequencies
    assert _find_fundamental_frequency([40.0, 60.0]) == 20.0
    print("OK")
