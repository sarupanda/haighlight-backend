# load video
# extract audio and save it
# downsample video and save resize
# execute each function sequentially

from luminosity_detection import extract_luminosity_data
from audio_lufs import extractLufsFromVideo
import matplotlib.pyplot as plt

if __name__ == '__main__':
    interval_seconds = 10
    video_filepath = 'test_low_res.mp4'
    luminosity = extract_luminosity_data(video_filepath, interval_seconds)
    plt.plot(luminosity)
    plt.ylabel('luminosity')
    plt.savefig('luminosity.png')
    plt.close()

    lufs = extractLufsFromVideo(video_filepath, interval_seconds)
    plt.plot(lufs)
    plt.ylabel('LUFS')
    plt.savefig('lufs.png')
    plt.close()
