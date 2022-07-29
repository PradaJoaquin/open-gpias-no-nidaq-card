import numpy as np

def process_recording(rec_data, playback_data):
    num_data_points = len(rec_data)
    data = np.zeros((6, num_data_points), dtype=np.float64)

    # channel ai0: x-Data
    # channel ai1: y-Data
    # channel ai2: z-Data
    # channel ai3: trigger pulse
    # channel ai4: pre-stimulus
    # channel ai5: startle-stimulus

    rec_data = np.stack(rec_data, axis=1)
    playback_data = np.stack(playback_data, axis=1)

    data[0] = data[1] = data[2] = rec_data[0]
    data[3] = data[5] = playback_data[0]
    data[4] = playback_data[1]

    return data
