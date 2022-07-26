import numpy as np

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

        data[0][rec_idx] = data[1][rec_idx] = data[2][rec_idx] = float(rec_sample[0]) # xyz data
        data[3][rec_idx] = data[5][rec_idx] = float(pb_sample[0]) # trigger pulse and startle-stimulus
        data[4][rec_idx] = float(pb_sample[1]) # pre-stimulus

    return data
