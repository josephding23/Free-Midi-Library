import pretty_midi


def get_merged_5_tracks_from_pm(pm, save_path):
    new_pm = pretty_midi.PrettyMIDI()

    drums = pretty_midi.Instrument(0, is_drum=True, name='Drums')
    piano = pretty_midi.Instrument(0, name='Piano')
    guitar = pretty_midi.Instrument(24, name='Guitar')
    bass = pretty_midi.Instrument(32, name='Bass')
    strings = pretty_midi.Instrument(48, name='Strings')

    for instr in pm.instruments:
        if instr.is_drum:
            for note in instr.notes:
                drums.notes.append(note)
        elif instr.program//8 == 0:
            for note in instr.notes:
                piano.notes.append(note)
        elif instr.program//8 == 3:
            for note in instr.notes:
                guitar.notes.append(note)
        elif instr.program//8 == 4:
            for note in instr.notes:
                bass.notes.append(note)
        elif instr.program < 96 or 104 <= instr.program < 112:
            for note in instr.notes:
                strings.notes.append(note)

    for instr in [drums, piano, guitar, bass, strings]:
        new_pm.instruments.append(instr)
    new_pm.write(save_path)


def get_merged_1_track_from_pm(pm, save_path):
    new_pm = pretty_midi.PrettyMIDI()
    one_track = pretty_midi.Instrument(0, name='Piano')

    for instr in pm.instruments:
        if not instr.is_drum:
            for note in instr.notes:
                one_track.notes.append(note)

    new_pm.instruments.append(one_track)
    new_pm.write(save_path)


def run():
    test_path = '../../data/test.mid'
    pm = pretty_midi.PrettyMIDI(test_path)
    get_merged_5_tracks_from_pm(pm, '../../data/merged5.mid')
    get_merged_1_track_from_pm(pm, '../../data/merged1.mid')


if __name__ == '__main__':
    run()
