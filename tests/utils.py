from utils import find_note_frequency


def test_find_note_frequency():
    print("Testing utils.find_note_frequency...", end="")
    assert find_note_frequency("E2") == 82.407
    assert find_note_frequency("A2") == 110.000
    assert find_note_frequency("D3") == 146.832
    assert find_note_frequency("G3") == 195.998
    assert find_note_frequency("B3") == 246.942
    assert find_note_frequency("E4") == 329.628
    print("OK")
