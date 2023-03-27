BASE_FREQUENCY = 440
BASE_LETTER = "A"
BASE_OCTAVE = 4

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
BASE_LETTER_INDEX = NOTES.index(BASE_LETTER)


def find_note_frequency(note: str) -> float:
    letter = note[:-1]
    octave = int(note[-1:])
    letter_index = NOTES.index(letter)
    steps_away = (letter_index - BASE_LETTER_INDEX) + 12 * (octave - BASE_OCTAVE)
    frequency = BASE_FREQUENCY * (2 ** (steps_away / 12))
    return round(frequency, 3)
