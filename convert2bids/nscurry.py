def clean_neuroscan_curry(raw):
    _remap_extra_channels(raw)
    _remap_stim_channel(raw)
    _fix_channel_locations(raw)


def _remap_extra_channels(raw):
    raw.set_channel_types({'hEOG': 'eog', 'vEOG': 'eog'})
    raw.set_channel_types({'ECG': 'ecg'})




def _remap_stim_channel(raw):
    raw.rename_channels({'Trigger': 'STIM'})
    raw.set_channel_types({'STIM': 'stim'})
    raw.info['chs'][raw.info['ch_names'].index('STIM')]['cal'] = 1e6


def _fix_channel_locations(raw):
    for ch in raw.info['chs']:
        ch['loc'][0] = -ch['loc'][0]
        ch['loc'][1] = -ch['loc'][1]
