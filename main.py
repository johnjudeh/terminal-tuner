from collections import Counter
from graph import plot_frames
from audio.pitch import calculate_pitch
from audio.parsers import read_wave_file
from audio.generators import make_sound, create_sound_wave


if __name__ == "__main__":
    # make_sound(frequency=440)
    # frames = create_sound_wave(frequency=440, frame_rate=STANDARD_FRAME_RATE)
    # frequency = calculate_pitch(frames, STANDARD_FRAME_RATE)
    # print(f"Frequency (Hz): {frequency}")
    # assert round(frequency) == 440
    # plot_frames(frames, channels=1)

    frames, params = read_wave_file("examples/A.wav")
    # frames, params = read_wave_file("examples/82.407.wav")
    frequency = calculate_pitch(
        frames,
        frame_rate=params.framerate,
        channels=params.nchannels,
        sample_width=params.sampwidth,
    )
    print(f"Frequency (Hz): {frequency}")

    plot_frames(frames, channels=params.nchannels, sample_width=params.sampwidth)
