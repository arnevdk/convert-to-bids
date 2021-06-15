#!/usr/bin/env python
import math
import shutil
from os.path import exists
import pathlib
import click
from mne.io import read_raw_bdf
from mne_bids import BIDSPath, write_raw_bids
import os

from convert2bids.biosemi import clean_biosemi


@click.command()
@click.argument('raw_files', type=click.Path(exists=True), nargs=-1)
@click.argument('task', type=click.Path())
@click.argument('output_path', type=click.Path())
def biosemi2bids(raw_files, task, output_path):
    rawdata_path = os.path.join(output_path, 'rawdata')
    sourcedata_path = os.path.join(output_path, 'sourcedata')
    code_path = os.path.join(output_path, 'code')

    pathlib.Path(rawdata_path).mkdir(parents=True, exist_ok=True)
    pathlib.Path(sourcedata_path).mkdir(parents=True, exist_ok=True)

    for i, raw_path in enumerate(raw_files):
        # Copy original file to sourcedata
        source_raw_path = os.path.join(sourcedata_path,
                                       os.path.basename(raw_path))
        shutil.copy(raw_path, source_raw_path)
        # Copy original logfile to sourcedata if present
        logfile_path = os.path.splitext(raw_path)[0] + '.txt'
        if exists(logfile_path):
            source_logfile_path = os.path.join(sourcedata_path,
                                               os.path.basename(logfile_path))
            shutil.copy(logfile_path, source_logfile_path)

        # Clean raw data
        raw = read_raw_bdf(raw_path, preload=False)
        clean_biosemi(raw)
        # TODO find events
        # TODO check events
        # TODO generate PSD
        # TODO support for sessions and runs
        subject_id = str(i).zfill(3)
        bids_path = BIDSPath(subject=subject_id, task=task, root=rawdata_path,
                             run=None, session=None)
        write_raw_bids(raw, bids_path, events_data=None, event_id=None,
                       overwrite=True)


if __name__ == '__main__':
    biosemi2bids()
