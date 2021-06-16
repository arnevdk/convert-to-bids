from abc import ABC, abstractmethod

import mne.io
import numpy as np
from mne import find_events, pick_info
import os
import re


class Processor(ABC):

    def __init__(self, raw_path, logfile_path=None):
        self.raw_path = raw_path
        self.logfile_path = logfile_path

    def clean(self):
        raw = self._load_raw()
        raw = self._clean_raw(raw)
        events = self._clean_events(raw)
        return raw, events

    @abstractmethod
    def _load_raw(self):
        pass

    def _clean_raw(self, raw):
        return raw

    def _clean_events(self, raw):
        events = self._find_events(raw)
        self._check_events(events)
        return events

    def _find_events(self, raw):
        stim_data = raw.get_data(picks=['STIM'])
        stim_data[0, :] = np.round(stim_data[0, :]).astype(int)
        stim_chan_id = raw.info['ch_names'].index('STIM')
        stim_raw = mne.io.RawArray(stim_data, pick_info(raw.info,
                                                        sel=[stim_chan_id]))
        events = find_events(stim_raw, consecutive=False, shortest_event=0,
                             min_duration=2 / stim_raw.info['sfreq'])
        return events

    def _check_events(self, events):
        if not os.path.isfile(self.logfile_path):
            return
        stim_events = events[events[:, -1] < 100, :]
        with open(self.logfile_path) as stim_log_file:
            stim_log = stim_log_file.read()
        log_regex = r'\[(?:\d|\-|\.)*\]\s+Marker\s+([\d]) .*'
        log_events = [int(s) for s in re.findall(log_regex, stim_log)]
        for i in range(len(log_events)):
            log_stim = log_events[i]
            data_stim = stim_events[i, -1]
            if log_stim != data_stim:
                raise ValueError(
                    f'Stimulus {i + 1} in log file ({log_stim}) does '
                    f'not match stimulus {i + 1} in raw file '
                    f'({data_stim})!')
