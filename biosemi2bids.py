#!/usr/bin/env python

import click
import os
import numpy as np
from mne_bids import BIDSPath, write_raw_bids
from convert2bids.biosemi import BioSemiBDFProcessor
from convert2bids.utils import _copy_sourcedata


@click.command()
@click.argument('raw_files', type=click.Path(exists=True), nargs=-1)
@click.argument('task', type=click.Path())
@click.argument('output_path', type=click.Path())
def biosemi2bids(raw_files, task, output_path):
    rawdata_path = os.path.join(output_path, 'rawdata')
    sourcedata_path = os.path.join(output_path, 'sourcedata')
    for i, raw_path in enumerate(raw_files):
        logfile_path = os.path.splitext(raw_path)[0] + '.txt'
        _copy_sourcedata(raw_path, logfile_path, sourcedata_path)
        processor = BioSemiBDFProcessor(raw_path, logfile_path)
        raw, events = processor.clean()
        # TODO support for sessions and runs
        subject_id = str(i+1).zfill(3)
        bids_path = BIDSPath(subject=subject_id, task=task, root=rawdata_path,
                             run=None, session=None)
        write_raw_bids(raw, bids_path, events_data=events,
                       event_id={str(e):e for e in np.unique(events[:,-1])},
                       overwrite=True)


if __name__ == '__main__':
    biosemi2bids()
