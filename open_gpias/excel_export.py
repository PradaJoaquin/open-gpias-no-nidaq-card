import xlsxwriter
import numpy as np
import os

def process_trial(data, samplerate):
    trigger_thresh = 0.2
    startle_thresh = 0.2

    trigger_idx = np.argmax(abs(data[3]) > trigger_thresh)
    startle_idx = np.argmax(abs(data[1][trigger_idx:]) > startle_thresh) + trigger_idx
    peak_idx = np.argmax(abs(data[1][trigger_idx:])) + trigger_idx

    trigger_t = float(trigger_idx) / samplerate
    startle_t = float(startle_idx) / samplerate
    peak_t = float(peak_idx) / samplerate

    print(f'Trigger: {trigger_t}s')

    startle_sec = startle_t - trigger_t
    peak_sec = peak_t - trigger_t

    peak_amp = abs(data[1][peak_idx])

    return [
        startle_sec,
        peak_sec,
        peak_amp
    ]


def export(data, filepath):
    """
    Export data to an Excel file.
    """

    if os.path.isdir(filepath):
        filepath = os.path.join(filepath, 'experiment.xlsx')

    rows = []
    for trial_data in data:
        row = process_trial(trial_data, 48000)
        rows.append(row)

    workbook = xlsxwriter.Workbook(filepath)
    worksheet = workbook.add_worksheet()

    header = [
        'Startle Beginning Time (s)',
        'Startle Peak Time (s)',
        'Peak Amplitude (0-1)',
    ]
    index = [f'Trial {i+1}' for i in range(len(rows))]
    worksheet.write_row(0, 1, header)
    worksheet.write_column(1, 0, index)

    for i,row in enumerate(rows):
        worksheet.write_row(i+1, 1, row)

    worksheet.write_row(len(rows)+2, 0, [
        'Average',
        f'=AVERAGE(B2:B{len(rows)+1})',
        f'=AVERAGE(C2:C{len(rows)+1})',
        f'=AVERAGE(D2:D{len(rows)+1})',
    ])

    workbook.close()

    if not os.path.isfile(filepath):
        raise RuntimeError(f'Could not create excel file')
