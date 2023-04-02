from collections import Counter

# frames = frame_rate x time
# therefore time = frame_rate / frames
# velocity = frequency x wavelength
# frequency = wavelengths per second


def calculate_pitch(
    frames: bytes, frame_rate: int, channels: int = 1, sample_width: int = 2
) -> int:
    # Mark each peak of the wave
    peaks = []
    step = sample_width * channels

    peak_start = None
    peak_end = None
    last_value = None
    is_rising = None

    def set_is_rising(current_value: int, last_value: int) -> bool:
        if current_value > last_value:
            return True
        elif current_value < last_value:
            return False

    for f in range(step, len(frames), step):
        current_value = int.from_bytes(
            frames[f : f + sample_width], byteorder="little", signed=True
        )

        if last_value is None:
            last_f = f - step
            last_value = int.from_bytes(
                frames[last_f : last_f + sample_width], byteorder="little", signed=True
            )

        if is_rising is None or is_rising is False:
            # When the values are falling, we want to change is_rising
            # before the next conditional block. When the values are
            # rising, we want to change it after the conditional block
            # so that we can record the peak end
            is_rising = set_is_rising(current_value, last_value) or is_rising

        if is_rising:
            if current_value > last_value:
                # We might be at a peak
                peak_start = f // step

            elif current_value < last_value:
                # Confirms we were at a peak
                peak_end = (f - step) // step
                peak_mid = round(peak_start + (peak_end - peak_start) / 2)
                peaks.append(peak_mid)

        # print(f // step, last_value, current_value, is_rising, peak_start, peak_end)

        if current_value != last_value:
            is_rising = set_is_rising(current_value, last_value)
            last_value = current_value

    print(peaks[-10:])

    if len(peaks) == 0:
        raise ValueError("Frames has no peaks to calculate pitch")

    # Calculate the distance between each peak in frames
    frames_wave_lengths = []
    for i, peak_mid in enumerate(peaks):
        if i == 0:
            continue
        frames_wave_length = peak_mid - peaks[i - 1]
        frames_wave_lengths.append(frames_wave_length)
    print(frames_wave_lengths[-10:])

    # Convert wavelength in frames to wavelength in seconds
    frequencies = []
    for frames_wave_length in frames_wave_lengths:
        seconds_wave_length = frames_wave_length / frame_rate
        frequency = 1 / seconds_wave_length
        frequencies.append(frequency)
    print(frequencies[-10:])
    print(Counter(list(map(lambda x: round(x, 2), frequencies))))

    # Average frequency
    avg_frequency = sum(frequencies) / len(frequencies)

    # Return
    return avg_frequency
