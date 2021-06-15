import mne.io
import numpy as np
from mne import find_events, pick_info
import os
import re



def clean_events(raw):
    stim_data = raw.get_data(picks=['STIM'])
    print(np.max(stim_data))
    stim_data[0,:] = np.round(stim_data[0,:]).astype(int)
    stim_chan_id = raw.info['ch_names'].index('STIM')
    stim_raw = mne.io.RawArray(stim_data, pick_info(raw.info, sel=[stim_chan_id]))
    events = find_events(stim_raw, consecutive=False, shortest_event=0,
                         min_duration=2 / stim_raw.info['sfreq'])
    return events


def check_events(events, logfile):
    if not os.path.isfile(logfile):
        return
    stim_events = events[events[:, -1] < 100, :]
    with open(logfile) as stim_log_file:
        stim_log = stim_log_file.read()
    log_regex = r'\[(?:\d|\-|\.)*\]\s+Marker\s+([\d]) .*'
    log_events = [int(s) for s in re.findall(log_regex, stim_log)]
    for i in range(len(log_events)):
        log_stim = log_events[i]
        data_stim = stim_events[i, -1]
        if log_stim != data_stim:
            raise ValueError(f'Stimulus {i+1} in log file ({log_stim}) does '
                             f'not match stimulus {i+1} in raw file '
                             f'({data_stim})!')
