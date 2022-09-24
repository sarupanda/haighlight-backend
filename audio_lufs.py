import moviepy.editor as mp
import soundfile as sf
import pyloudnorm as pyln
import os
import logging
import numpy as np

logging.basicConfig(level='DEBUG')
log = logging.getLogger(__name__)

def extractAudio(filepath):
    log.debug('extracting audio')
    filename = ''.join(filepath.split('.')[:-1])
    audio_filepath = f'{filename}.wav'
    if os.path.exists(audio_filepath):
        log.info(f'{audio_filepath} already exists, skipping extracting audio')
        return audio_filepath
    my_clip = mp.VideoFileClip(filepath)
    my_clip.audio.write_audiofile(audio_filepath)
    return audio_filepath

def extractLufs(audio_filepath, interval_seconds):
    log.debug('extracting lufs')
    log.debug('reading soundfile')
    data, rate = sf.read(audio_filepath)
    data_chunks = np.array_split(data, len(data) // (rate * interval_seconds))
    lufs = []
    for chunk in data_chunks:
        meter = pyln.Meter(rate)
        loudness = meter.integrated_loudness(chunk)
        lufs.append(loudness)
    return lufs

if __name__ == '__main__':
    audio_filepath = extractAudio('no_mercy.mp4')
    interval_seconds = 5
    lufs = extractLufs(audio_filepath, interval_seconds)
    print(len(lufs))
