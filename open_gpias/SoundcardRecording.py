import numpy as np
import soundcard as sc
import os
from scipy.io import wavfile
from datetime import datetime

def perform_soundcard_recording(duration_ms, recordingrate):
    rate = recordingrate  # sampling rate of measurement
    num_data_points = int(duration_ms * rate / 1000)

    data = np.zeros((6, num_data_points), dtype=np.float64)

    # channel ai0: x-Data
    # channel ai1: y-Data
    # channel ai2: z-Data
    # channel ai3: trigger pulse
    # channel ai4: pre-stimulus
    # channel ai5: startle-stimulus

    default_mic = sc.default_microphone()
    recording_time = datetime.now()
    raw_data = default_mic.record(samplerate=rate, numframes=num_data_points)

    out_dir = os.path.expanduser("~/Desktop/OpenGPIAS/")
    filepath = os.path.join(out_dir, f"recording_{recording_time.isoformat()}.wav")

    wavfile.write(filepath, rate, raw_data.astype(np.float32))

    for idx, sample in enumerate(raw_data):
        sample = sample[0]
        time = float(idx) / rate
        data[0][idx] = data[1][idx] = data[2][idx] = float(sample) # xyz data
        data[3][idx] = 0 # trigger pulse
        data[4][idx] = 0 # pre-stimulus
        data[5][idx] = 0 # startle-stimulus

    return (recording_time, data)
