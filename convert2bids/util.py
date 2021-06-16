import os
import pathlib
import shutil


def _copy_sourcedata(raw_path, logfile_path, sourcedata_path):
    pathlib.Path(sourcedata_path).mkdir(parents=True, exist_ok=True)
    source_raw_path = os.path.join(sourcedata_path, os.path.basename(raw_path))
    shutil.copy(raw_path, source_raw_path)
    if os.path.exists(logfile_path):
        source_logfile_path = os.path.join(sourcedata_path,
                                           os.path.basename(logfile_path))
        shutil.copy(logfile_path, source_logfile_path)
