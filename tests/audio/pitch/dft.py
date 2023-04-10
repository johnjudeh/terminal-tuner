from audio.pitch.dft import calculate_pitch, _find_base_frequency


def test_calculate_pitch() -> None:
    print("Testing audio.pitch.calculate_pitch...", end="")
    calculate_pitch("examples/E.wav") == "E2"
    calculate_pitch("examples/A.wav") == "A2"
    calculate_pitch("examples/D.wav") == "D3"
    calculate_pitch("examples/G.wav") == "G3"
    calculate_pitch("examples/B.wav") == "B3"
    calculate_pitch("examples/e_high.wav") == "E4"
    print("OK")


def test_find_base_frequency() -> None:
    print("Testing audio.pitch._find_base_frequency...", end="")
    # Happy path
    assert _find_base_frequency([20.0]) == 20.0
    assert _find_base_frequency([20.0, 40.0, 60.0]) == 20.0
    # Sorting
    assert _find_base_frequency([40.0, 20.0, 60.0]) == 20.0
    # Edge case
    assert _find_base_frequency([20.0, 41.0, 61.0]) == 20.0
    assert _find_base_frequency([20.0, 39.0, 59.0]) == 20.0
    # Bad frequencies
    assert _find_base_frequency([18.0, 19.0, 20.0, 40.0, 60.0]) == 20.0
    assert _find_base_frequency([20.0, 44.0, 66.0]) == None
    print("OK")
