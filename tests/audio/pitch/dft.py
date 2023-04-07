from audio.pitch.dft import calculate_pitch


def test_calculate_pitch() -> None:
    print("Testing audio.pitch.calculate_pitch...", end="")
    calculate_pitch("examples/E.wav") == "E2"
    calculate_pitch("examples/A.wav") == "A2"
    calculate_pitch("examples/D.wav") == "D3"
    calculate_pitch("examples/G.wav") == "G3"
    calculate_pitch("examples/B.wav") == "B3"
    calculate_pitch("examples/e_high.wav") == "E4"
    print("OK")
