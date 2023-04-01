from utils import find_note_frequency, find_nearest_note


def test_find_note_frequency():
    print("Testing utils.find_note_frequency...", end="")

    A4_frequency = 440.0

    # Case insensitive
    assert find_note_frequency("A4") == A4_frequency
    assert find_note_frequency("a4") == A4_frequency

    # Same octave as BASE_FREQUENCY
    assert find_note_frequency("A4") == A4_frequency
    assert find_note_frequency("C4") == 261.626
    assert find_note_frequency("B4") == 493.883

    # Higher octave than BASE_FREQUENCY
    assert find_note_frequency("A5") == 880.000
    assert find_note_frequency("C5") == 523.251
    assert find_note_frequency("B5") == 987.767

    # Lower octave than BASE_FREQUENCY
    assert find_note_frequency("A3") == 220.0
    assert find_note_frequency("C3") == 130.813
    assert find_note_frequency("B3") == 246.942

    # Guitar strings
    assert find_note_frequency("E2") == 82.407
    assert find_note_frequency("A2") == 110.000
    assert find_note_frequency("D3") == 146.832
    assert find_note_frequency("G3") == 195.998
    assert find_note_frequency("B3") == 246.942
    assert find_note_frequency("E4") == 329.628

    print("OK")


def test_find_nearest_note():
    print("Testing utils.find_nearest_note...", end="")

    less_than_half_step = 2 ** (0.49 / 12)
    more_than_half_step = 2 ** (0.51 / 12)

    # Same octave as BASE_FREQUENCY
    A4 = 440.0
    assert find_nearest_note(A4) == "A4"
    assert find_nearest_note(261.626) == "C4"
    assert find_nearest_note(493.883) == "B4"
    # Rounding
    assert find_nearest_note(A4 * less_than_half_step) == "A4"
    assert find_nearest_note(A4 * more_than_half_step) == "A#4"

    # Higher octave than BASE_FREQUENCY
    A5 = 880.0
    assert find_nearest_note(A5) == "A5"
    assert find_nearest_note(523.251) == "C5"
    assert find_nearest_note(987.767) == "B5"
    # Rounding
    assert find_nearest_note(A5 * less_than_half_step) == "A5"
    assert find_nearest_note(A5 * more_than_half_step) == "A#5"

    # Lower octave than BASE_FREQUENCY
    A3 = 220.0
    assert find_nearest_note(A3) == "A3"
    assert find_nearest_note(130.813) == "C3"
    assert find_nearest_note(246.942) == "B3"
    # Rounding
    assert find_nearest_note(A3 * less_than_half_step) == "A3"
    assert find_nearest_note(A3 * more_than_half_step) == "A#3"

    print("OK")
