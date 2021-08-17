import numpy as np
from mne import read_epochs_eeglab, create_info
from mne.io import RawArray

from convert2bids.common import Processor


class SEREEGAProcessor(Processor):

    def _load_raw(self):
        epochs = read_epochs_eeglab(self.raw_path)
        epochs_data = epochs.get_data()
        n_epochs, n_channels, n_samples = epochs_data.shape
        raw_data = epochs_data.transpose(1, 0, 2).reshape(
            (n_channels, n_epochs * n_samples))
        raw = RawArray(raw_data, epochs.info)
        stim_raw_data = np.zeros((1, n_epochs*n_samples))
        stim_raw_data[0, epochs.events[:,0]] = epochs.events[:,2]
        stim_raw_info = create_info(['STIM'], raw.info['sfreq'],
                                    ch_types='stim')
        stim_raw = RawArray(stim_raw_data, stim_raw_info)
        raw.add_channels([stim_raw])
        return raw

    def _clean_raw(self, raw):
        raw.set_montage('standard_1005')
        return raw
