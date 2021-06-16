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
        raw.rename_channels({
            'EXG1': 'TP9',
            'EXG2': 'TP10'
        })
        raw.set_channel_types({
            'TP9': 'eeg',
            'TP10': 'eeg'
        })
        raw.rename_channels({
            'EXG3': 'EOG1',
            'EXG4': 'EOG2',
            'EXG5': 'EOG3',
            'EXG6': 'EOG4'
        })
        raw.set_channel_types({
            'EOG1': 'eog',
            'EOG2': 'eog',
            'EOG3': 'eog',
            'EOG4': 'eog',
        })
        raw.rename_channels({
            'EXG7': 'ECG1',
            'EXG8': 'ECG2',
        })
        raw.set_channel_types({
            'ECG1': 'ecg',
            'ECG2': 'ecg',
        })
        return raw

    def _remap_stim_channel(self, raw):
        raw.rename_channels({'Status': 'STIM'})
        raw.set_channel_types({'STIM': 'stim'})
        return raw
