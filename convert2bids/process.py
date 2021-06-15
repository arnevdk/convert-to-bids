import setuptools
from mne.io import read_raw_bdf, read_raw_curry
from mne_bids import BIDSPath, write_raw_bids
import os

import shutil
from os.path import exists
import pathlib
from convert2bids.biosemi import clean_biosemi
from convert2bids.common import clean_events, check_events
from convert2bids.nscurry import clean_neuroscan_curry


def process(raw_files, task, output_path, format):
    rawdata_path = os.path.join(output_path, 'rawdata')
    sourcedata_path = os.path.join(output_path, 'sourcedata')

    pathlib.Path(rawdata_path).mkdir(parents=True, exist_ok=True)

    for i, raw_path in enumerate(raw_files):
        logfile_path = os.path.splitext(raw_path)[0] + '.txt'
        # Copy original file to sourcedata
        _copy_sourcedata(raw_path, logfile_path, sourcedata_path)
        # Clean raw data
        if format == 'biosemi':
            raw = read_raw_bdf(raw_path, preload=False)
            clean_biosemi(raw)
        elif format == 'neuroscan_curry':
            raw = read_raw_curry(raw_path, preload=True)
            clean_neuroscan_curry(raw)
        else:
            raise NotImplementedError
        # Extract and verify events
        events = clean_events(raw)
        check_events(events, logfile_path)

        # TODO support for sessions and runs
        subject_id = str(i).zfill(3)
        bids_path = BIDSPath(subject=subject_id, task=task, root=rawdata_path,
                             run=None, session=None)
        write_raw_bids(raw, bids_path, events_data=None, event_id=None,
                       overwrite=True)


def _copy_sourcedata(raw_path, logfile_path, sourcedata_path):
    pathlib.Path(sourcedata_path).mkdir(parents=True, exist_ok=True)
    source_raw_path = os.path.join(sourcedata_path, os.path.basename(raw_path))
    shutil.copy(raw_path, source_raw_path)
    if exists(logfile_path):
        source_logfile_path = os.path.join(sourcedata_path,
                                           os.path.basename(logfile_path))
        shutil.copy(logfile_path, source_logfile_path)
