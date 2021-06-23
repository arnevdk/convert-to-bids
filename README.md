# Convert to BIDS

This repository contains scripts to and convert the biosensor data recorded with the lab equipment to a clean and
BIDS-compliant dataset for data sharing and processing.

BIDS is a standard format to store neuroimaging datasets. More information the BIDS specification can be found
at https://bids.neuroimaging.io/index.html .
A walktrough can be found at https://github.com/bids-standard/bids-starter-kit/wiki/Tutorials .

## Installation

Install with

```shell
pip install git+https://gitlab.kuleuven.be/compneuro/convert-to-bids.git # after setting an account password
# or
pip install git+ssh://git@gitlab.kuleuven.be:compneuro/convert-to-bids.git  # after adding an account ssh-key
```

## Usage

### Neuroscan Curry 7

Convert .dat files to BIDS dataset.

    nscurry2bids [OPTIONS] [RAW_FILES]... TASK OUTPUT_PATH

Clean the NeuroScan Curry 7 format `.dat` files specified in `RAW_FILES` and add them to a BIDS format dataset stored
in `OUTPUT_PATH`. The .dat files should be recorded by the lab equipment while performing experimental task `TASK`.
These files need to be accompanied in the same directory by their `.dat`,
`.dap` and `.rs3` files with metadata. These files is optionally accompanied in the same directory by a `.txt`
experiment log file with the same filename.

For example,

    nscurry2bids data/subject_01.bdf data/subject_02.bdf oddball oddball_32

converts the `.bdf` files in

    data
    ├── subject_01.ceo
    ├── subject_01.dap
    ├── subject_01.dat
    ├── subject_01.rs3
    ├── subject_01.txt
    ├── subject_02.ceo
    ├── subject_02.dap
    ├── subject_02.dat
    ├── subject_02.rs3
    └── subject_02.txt

cleans up the data's channel names and metadata, verifies the registration of all stimuli logged in
respectively `subject_01.txt` and `subject_02.txt`
and writes the data to `sub-001` and `sub-002` with tasks oddball to the BIDS dataset stored in `oddball_32`.

See `nscurry2bids --help` for more options.


### BioSemi

Convert `.bdf` files to BIDS dataset.

    biosemi2bids [OPTIONS] [RAW_FILES]... TASK OUTPUT_PATH

Clean the BioSemi `.bdf` files specified in `RAW_FILES` and add them to to a
`BIDS` format dataset stored in OUTPUT_PATH. The .bdf files should be recorded by the lab equipment while performing
experimental task `TASK`. These files are optionally accompanied in the same directory by a `.txt`
experiment log file with the same filename.

For example,

    biosemi2bids data/subject_01.bdf data/subject_02.bdf oddball oddball_32

converts the .bdf files in

    data
    ├── subject_01.bdf
    ├── subject_01.txt
    ├── subject_02.bdf
    └── subject_02.txt

cleans up the data's channel names and metadata, verifies the registration of all stimuli logged in
respectively `subject_01.txt` and `subject_02.txt`
and writes the data to `sub-subject01` and `sub-subject02` with task `oddball` to the BIDS dataset stored in `oddball_32`.

See `biosemi2bids --help` for more options.

### Log files

# TODO: document logfile format
see equipmentlib

## Steps to take after dataset generation

1. Complete the dataset by filling out the necessary files:  
    * dataset_description.json
    * README
    * CHANGES
    * LICENSE
    * participants.tsv
    * ...
1. event ids
1. Mark bad channels and epochs using
   the ```mne_bids inspect``` command, e.g.   
   ```shell
   mne_bids inspect --bids_root=data/test_32_bids/rawdata/ --subject_id=001 --l_freq=0.5 --h_freq=30
   ```
   For more information, see https://mne.tools/mne-bids/stable/auto_examples/mark_bad_channels.html

