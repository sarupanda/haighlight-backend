import moviepy.editor as mp
import soundfile as sf
import pyloudnorm as pyln
import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(level='INFO')
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
    meter = pyln.Meter(rate)
    lufs = []
    for chunk in data_chunks:
        loudness = meter.integrated_loudness(chunk)
        lufs.append(loudness)
    lufs = pd.DataFrame(lufs, columns=['lufs'], index=list(range(0, len(data_chunks) * interval_seconds, interval_seconds)))
    lufs = lufs.rolling(10).mean()
    return lufs

def extractLufsFromVideo(video_filepath, interval_seconds):
    audio_filepath = extractAudio(video_filepath)
    lufs = extractLufs(audio_filepath, interval_seconds)
    return lufs
