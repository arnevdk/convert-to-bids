from mne import set_bipolar_reference
from mne.io import read_raw_bdf

from convert2bids.common import Processor


class BioSemiProcessor(Processor):

    def _clean_raw(self, raw):
        raw = super()._clean_raw(raw)
        raw = self._remove_duplicate_channels(raw)
        raw = self._remap_extra_channels(raw)
        raw = self._remap_stim_channel(raw)
        raw.set_montage('standard_1020')
        return raw

    def _load_raw(self):
        raw = read_raw_bdf(self.raw_path, preload=False)
        return raw

    def _remove_duplicate_channels(self, raw):
        for chan in raw.ch_names:
            if chan.endswith('-1'):
                raw.drop_channels([chan])
            elif chan.endswith('-0'):
                raw.rename_channels({chan: chan[:-2]})
        return raw

    def _remap_extra_channels(self, raw):
        """
        raw.rename_channels({
            'EXG1': 'TP9',
            'EXG2': 'TP10'
        })
        raw.load_data()
        set_bipolar_reference(raw, 'EXG3', 'EXG4', ch_name='hEOG',
                              drop_refs=True, copy=False)
        set_bipolar_reference(raw, 'EXG5', 'EXG6', ch_name='vEOG',
                              drop_refs=True, copy=False)
        set_bipolar_reference(raw, 'EXG7', 'EXG8', ch_name='ECG',
                              drop_refs=True, copy=False)
        raw.set_channel_types({
            'TP9': 'eeg',
            'TP10': 'eeg',
            'hEOG': 'eog',
            'vEOG': 'eog',
            'ECG': 'ecg',
        })
        """
        raw.rename_channels({
            'EXG1': 'TP9',
            'EXG2': 'TP10',
            'EXG3': 'hEOGl',
            'EXG4': 'hEOGr',
            'EXG5': 'vEOGu',
            'EXG6': 'vEOGd',
            'EXG7': 'ECGl',
            'EXG8': 'ECGr',
        })
        raw.set_channel_types({
            'TP9': 'eeg',
            'TP10': 'eeg',
            'hEOGl': 'eog',
            'hEOGr': 'eog',
            'vEOGl': 'eog',
            'vEOGr': 'eog',
            'ECGl': 'ecg',
            'ECGr': 'ecg',
        })
        return raw

    def _remap_stim_channel(self, raw):
        raw.rename_channels({'Status': 'STIM'})
        raw.set_channel_types({'STIM': 'stim'})
        return raw
