def clean_biosemi(raw):
    _remove_duplicate_channels(raw)
    _remap_extra_channels(raw)
    _remap_stim_channel(raw)
    raw.set_montage('standard_1020')


def _remove_duplicate_channels(raw):
    for chan in raw.ch_names:
        if chan.endswith('-1'):
            raw.drop_channels([chan])
        elif chan.endswith('-0'):
            raw.rename_channels({chan: chan[:-2]})


def _remap_extra_channels(raw):
    raw.rename_channels({'EXG1': 'TP9', 'EXG2': 'TP10'})
    raw.set_channel_types({'TP9': 'eeg', 'TP10': 'eeg'})
    eog_channels = ['EXG3', 'EXG4', 'EXG5', 'EXG6']
    raw.set_channel_types({chan: 'eog' for chan in eog_channels})
    ecg_channels = ['EXG7', 'EXG8']
    raw.set_channel_types({chan: 'ecg' for chan in ecg_channels})


def _remap_stim_channel(raw):
    raw.rename_channels({'Status': 'STIM'})
    raw.set_channel_types({'STIM': 'stim'})
