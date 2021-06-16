from mne import pick_info, find_events
from mne.io import read_raw_curry, RawArray
import numpy as np

from convert2bids.common import Processor


class NeuroScanCurry7Processor(Processor):

    def _clean_raw(self, raw):
        raw = super()._clean_raw(raw)
        raw = self._remap_extra_channels(raw)
        raw = self._remap_stim_channel(raw)
        raw = self._fix_channel_locations(raw)
        return raw

    def _load_raw(self):
        raw = read_raw_curry(self.raw_path, preload=False)
        return raw

    def _find_events(self, raw):
        stim_data = raw.get_data(picks=['STIM'])
        stim_data[0, :] = np.round(stim_data[0, :] * 1e6).astype(int)
        stim_chan_id = raw.info['ch_names'].index('STIM')
        stim_raw = RawArray(stim_data, pick_info(raw.info,
                                                 sel=[stim_chan_id]))
        events = find_events(stim_raw, consecutive=False, shortest_event=0,
                             min_duration=2 / stim_raw.info['sfreq'])
        return events

    def _remap_extra_channels(self, raw):
        raw.set_channel_types({'hEOG': 'eog', 'vEOG': 'eog'})
        raw.set_channel_types({'ECG': 'ecg'})
        return raw

    def _remap_stim_channel(self, raw):
        raw.rename_channels({'Trigger': 'STIM'})
        raw.set_channel_types({'STIM': 'stim'})
        raw.info['chs'][raw.info['ch_names'].index('STIM')]['cal'] = 1e6
        return raw

    def _fix_channel_locations(self, raw):
        for ch in raw.info['chs']:
            ch['loc'][0] = -ch['loc'][0]
            ch['loc'][1] = -ch['loc'][1]
        return raw
