""" Generates music.wav: an original 8-bit (Game Boy style) chiptune used as
the game's background music.

Made by Shaurya Dogra and Ritak Raj Pandey.

Run once with `python make_music.py`. Only the Python standard library is used.
The sound is built the same way old handheld consoles made it: a square wave
lead, a quieter square wave arpeggio, a triangle wave bass and short bursts of
noise for the hi-hat.

"""
import math
import random
import struct
import wave

SAMPLE_RATE = 22050
BPM = 150
STEP = 60.0 / BPM / 2  # length of one eighth note in seconds

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# One chord per bar: (root note, chord tones as semitones above the root).
MAJOR = (0, 4, 7, 12)
MINOR = (0, 3, 7, 12)
CHORDS = [
    ('C3', MAJOR), ('G2', MAJOR), ('A2', MINOR), ('F2', MAJOR),
    ('C3', MAJOR), ('G2', MAJOR), ('F2', MAJOR), ('G2', MAJOR),
    ('A2', MINOR), ('F2', MAJOR), ('C3', MAJOR), ('G2', MAJOR),
    ('A2', MINOR), ('F2', MAJOR), ('G2', MAJOR), ('G2', MAJOR),
]

# Lead melody, 8 eighth notes per bar. '-' holds the previous note, '.' rests.
MELODY = """
E4 - G4 - C5 - B4 A4 | G4 - - D4 G4 - B4 - | A4 - C5 - E5 - D5 C5 | C5 - A4 - F4 - G4 A4
G4 - E4 - G4 C5 - E5 | D5 - B4 - G4 - A4 B4 | C5 - A4 - C5 - F5 E5 | D5 - - - B4 - D5 -
E5 - - C5 A4 - C5 E5 | F5 - E5 - D5 - C5 - | E5 - D5 C5 G4 - C5 - | D5 - - - G4 A4 B4 D5
E5 - A5 - G5 - E5 - | F5 - E5 - D5 - C5 A4 | B4 - D5 - G5 - F5 D5 | B4 - - - G4 - - -
"""


def midi(name):
    """ Convert a note name like 'C#4' to a MIDI note number. """
    return NOTE_NAMES.index(name[:-1]) + 12 * (int(name[-1]) + 1)


def frequency(note):
    """ Frequency in Hz of a MIDI note number (A4 = 69 = 440 Hz). """
    return 440.0 * 2 ** ((note - 69) / 12.0)


def square(phase, duty):
    return 1.0 if phase % 1.0 < duty else -1.0


def triangle(phase):
    return 4.0 * abs(phase % 1.0 - 0.5) - 1.0


def add_note(buf, start, length, freq, volume, wave_fn):
    """ Mix one note into `buf`, with a short attack and release to avoid
    clicks. `start` and `length` are in seconds.

    """
    first = int(start * SAMPLE_RATE)
    count = int(length * SAMPLE_RATE)
    fade = int(0.01 * SAMPLE_RATE)
    for i in range(count):
        if first + i >= len(buf):
            break
        env = min(1.0, i / float(fade), (count - i) / float(fade))
        env *= 1.0 - 0.3 * i / count  # slight decay over the note
        buf[first + i] += volume * env * wave_fn(i * freq / SAMPLE_RATE)


def parse_melody(text):
    """ Turn the MELODY text into (start step, length in steps, note) events. """
    steps = text.replace('|', ' ').split()
    events = []
    for i, token in enumerate(steps):
        if token == '-' and events:
            start, length, note = events[-1]
            events[-1] = (start, length + 1, note)
        elif token not in ('-', '.'):
            events.append((i, 1, midi(token)))
    return events, len(steps)


def main():
    events, total_steps = parse_melody(MELODY)
    buf = [0.0] * int(total_steps * STEP * SAMPLE_RATE)

    # Lead: 25% duty square wave.
    for start, length, note in events:
        add_note(buf, start * STEP, length * STEP, frequency(note), 0.22,
                 lambda p: square(p, 0.25))

    for bar, (root_name, tones) in enumerate(CHORDS):
        root = midi(root_name)
        bar_start = bar * 8 * STEP
        # Bass: triangle wave bouncing between the root and its octave.
        for i in range(8):
            note = root + (12 if i % 2 else 0)
            add_note(buf, bar_start + i * STEP, STEP, frequency(note), 0.30,
                     triangle)
        # Arpeggio: fast 16th notes cycling through the chord, two octaves up.
        for i in range(16):
            note = root + 24 + tones[i % len(tones)]
            add_note(buf, bar_start + i * STEP / 2, STEP / 2, frequency(note),
                     0.06, lambda p: square(p, 0.125))

    # Hi-hat: short noise bursts on every off-beat.
    rng = random.Random(1)
    for i in range(1, total_steps, 2):
        add_note(buf, i * STEP, 0.03, 1.0, 0.07,
                 lambda p: rng.uniform(-1.0, 1.0))

    # Write 16-bit mono PCM, clipped to the valid range.
    out = wave.open('music.wav', 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(SAMPLE_RATE)
    out.writeframes(b''.join(
        struct.pack('<h', int(max(-1.0, min(1.0, s)) * 26000)) for s in buf))
    out.close()
    print('Wrote music.wav (%.1f seconds)' % (len(buf) / float(SAMPLE_RATE)))


if __name__ == '__main__':
    main()
