import mido
from music21 import *
import pretty_midi
import os
from pymongo import MongoClient
import traceback
import mido
import math

def get_midi_collection():
    client = MongoClient(connect=False)
    return client.jazz_midikar.midi

def transpose_tone_mido():
    midi = mido.MidiFile('./test.mid')
    for msg in midi:
        if msg.is_meta:
            print(msg)


def get_key_signature():
    root_dir = 'E:/jazz_midkar/raw'
    midi_collection = get_midi_collection()
    for midi in midi_collection.find({'KeySignature': {'$exists': False}}, no_cursor_timeout=True):
        original_path = os.path.join(root_dir + '/', midi['md5'] + '.mid')
        try:

            original_stream = converter.parse(original_path)

            estimate_key = original_stream.analyze('key')
            print(estimate_key)

            estimate_tone, estimate_mode = (estimate_key.tonic, estimate_key.mode)
            key_signature = {'Tone': str(estimate_tone), 'Mode': estimate_mode}
            print(key_signature)

            midi_collection.update_one({'_id': midi['_id']},
                                       {'$set': {'KeySignature': key_signature}})

            print('Progress: {:.2%}\n'.format(midi_collection.count({'KeySignature': {'$exists': True}}) / midi_collection.count()))

        except Exception:
            print(traceback.format_exc())


def get_key_signature_in_meta():
    root_dir = 'E:/free_midi_library/raw_midi'
    midi_collection = get_midi_collection()
    for midi in midi_collection.find({}, no_cursor_timeout=True):
        original_path = os.path.join(root_dir, midi['Genre'] + '/', midi['md5'] + '.mid')
        try:

            mido_object = mido.MidiFile(original_path)
            for i, track in enumerate(mido_object.tracks):
                for msg in track:
                    if msg.is_meta and msg.type == 'key_signature':
                        print(msg)
            print()

        except Exception:
            print(traceback.format_exc())


def transpose_to_c():
    root_dir = 'E:/jazz_midkar/raw'
    transpose_root_dir = 'E:/jazz_midkar/transposed'
    midi_collection = get_midi_collection()
    for midi in midi_collection.find({'Transposed': False}, no_cursor_timeout=True):
        original_path = os.path.join(root_dir + '/', midi['md5'] + '.mid')

        transposed_path = os.path.join(transpose_root_dir + '/', midi['md5'] + '.mid')
        try:

            c_major_key = key.Key('C', 'major')
            a_minor_key = key.Key('A', 'minor')

            estimate_tone, estimate_mode = midi['KeySignature']['Tone'], midi['KeySignature']['Mode']
            if estimate_mode == 'major':
                transposed_key = c_major_key

            else:
                transposed_key = a_minor_key

            semitones = interval.Interval(transposed_key.tonic, key.Key(estimate_tone, estimate_mode).tonic).semitones
            if semitones > 0:
                alt_semitones = abs(interval.Interval(transposed_key.tonic, key.Key(estimate_tone, estimate_mode).tonic).semitones) - 12
            else:
                alt_semitones = 12 - abs(interval.Interval(transposed_key.tonic, key.Key(estimate_tone, estimate_mode).tonic).semitones)

            if abs(semitones) <= 6:
                pass
            else:
                semitones = alt_semitones

            mid = pretty_midi.PrettyMIDI(original_path)
            for instr in mid.instruments:
                if not instr.is_drum:
                    for _note in instr.notes:
                        if _note.pitch + semitones in range(0, 128):
                            _note.pitch += semitones

            mid.write(transposed_path)
            # new_stream = converter.parse(transposed_path)
            # new_key = new_stream.analyze('key')
            midi_collection.update_one({'_id': midi['_id']}, {'$set': {'Transposed': True}})
            print('Progress: {:.2%}\n'.format(midi_collection.count({'Transposed': True}) / midi_collection.count()))

        except:
            print(traceback.format_exc())


if __name__ == '__main__':
    # get_midi_collection().delete_many({'Transposed': False})
    # get_key_signature()
    # get_midi_collection().update_many({}, {'$set': {'Transposed': False}})
    transpose_to_c()
