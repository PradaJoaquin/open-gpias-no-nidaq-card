import numpy as np
import soundcard as sc
import os
from scipy.io import wavfile
from datetime import datetime

def perform_soundcard_recording(duration_ms, recordingrate):
    rate = recordingrate  # sampling rate of measurement
    num_data_points = int(duration_ms * rate / 1000)

    default_mic = sc.default_microphone()
    recording_time = datetime.now()
    raw_data = default_mic.record(samplerate=rate, numframes=num_data_points, channels=1)

    out_dir = os.path.expanduser("~/Desktop/OpenGPIAS/")
    filepath = os.path.join(out_dir, f"recording_{recording_time.isoformat()}.wav")

    wavfile.write(filepath, rate, raw_data.astype(np.float32))

    return (recording_time, raw_data)

def process_recording(rec_data, recording_rate, playback_data, playback_rate):
    num_data_points = len(rec_data)

    pad_len = abs(len(rec_data) - len(playback_data))
    playback_data = np.pad(playback_data, ((0,pad_len), (0,0)), 'constant', constant_values=(0))

    # TODO: Optimize with numpy.recording_rate
    data = np.zeros((6, num_data_points), dtype=np.float64)

    # channel ai0: x-Data
    # channel ai1: y-Data
    # channel ai2: z-Data
    # channel ai3: trigger pulse
    # channel ai4: pre-stimulus
    # channel ai5: startle-stimulus
    
    for rec_idx, rec_sample in enumerate(rec_data):
        t = float(rec_idx) / recording_rate
        pb_idx = int(t * playback_rate)

        # TODO: Find better way to handle different samplerates
        pb_sample = playback_data[pb_idx]

        data[0][rec_idx] = data[1][rec_idx] = data[2][rec_idx] = float(rec_sample) # xyz data
        data[3][rec_idx] = data[5][rec_idx] = float(pb_sample[0]) # trigger pulse and startle-stimulus
        data[4][rec_idx] = float(pb_sample[1]) # pre-stimulus

    return data
