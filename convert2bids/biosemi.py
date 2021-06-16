from mne.io import read_raw_bdf

from convert2bids.common import Processor


class BioSemiBDFProcessor(Processor):

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
        raw.rename_channels({'EXG1': 'TP9', 'EXG2': 'TP10'})
        raw.set_channel_types({'TP9': 'eeg', 'TP10': 'eeg'})
        eog_channels = ['EXG3', 'EXG4', 'EXG5', 'EXG6']
        raw.set_channel_types({chan: 'eog' for chan in eog_channels})
        ecg_channels = ['EXG7', 'EXG8']
        raw.set_channel_types({chan: 'ecg' for chan in ecg_channels})
        return raw

    def _remap_stim_channel(self, raw):
        raw.rename_channels({'Status': 'STIM'})
        raw.set_channel_types({'STIM': 'stim'})
        return raw

