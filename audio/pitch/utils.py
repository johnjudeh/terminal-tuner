from math import log2
from audio.constants import (
    NOTES,
    BASE_FREQUENCY,
    BASE_OCTAVE,
    BASE_LETTER_INDEX,
)


def find_note_frequency(note: str) -> float:
    letter = note[:-1].upper()
    octave = int(note[-1:])
    letter_index = NOTES.index(letter)
    steps_away = (letter_index - BASE_LETTER_INDEX) + 12 * (octave - BASE_OCTAVE)
    frequency = BASE_FREQUENCY * (2 ** (steps_away / 12))
    return round(frequency, 3)


def _find_steps_away(current_freq: float, target_freq: float) -> float:
    return 12 * log2(current_freq / target_freq)


def find_steps_away(current_freq: float, target_freq: float) -> float:
    return ((current_freq - target_freq) / target_freq) * 100


def find_nearest_note(frequency: float) -> str:
    steps_away = round(_find_steps_away(frequency, BASE_FREQUENCY))
    letter_index = (BASE_LETTER_INDEX + steps_away) % 12
    letter = NOTES[letter_index]
    octaves_away = (BASE_LETTER_INDEX + steps_away) // 12
    octave = BASE_OCTAVE + octaves_away
    return f"{letter}{octave}"
