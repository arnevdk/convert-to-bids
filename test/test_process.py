import unittest

from convert2bids.neuroscan import NeuroScanCurry7Processor

from convert2bids.biosemi import BioSemiProcessor


class TestProcess(unittest.TestCase):

    def test_biosemi(self):
        processor = BioSemiProcessor('data/test_32/subject_01.bdf',
                                     'data/test_32/subject_01.txt')
        raw, events = processor.clean()
        pass

    def test_neuroscan_curry_7(self):
        processor = NeuroScanCurry7Processor('data/test_128/subject_01.dat',
                                             'data/test_128/subject_01.txt')
        raw, events = processor.clean()
        pass
