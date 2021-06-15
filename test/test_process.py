import unittest

from convert2bids.process import process


class TestProcess(unittest.TestCase):

    def test_biosemi(self):
        process(['data/test_32/subject_02.bdf'], 'oddball',
                'data/test_32_bids', 'biosemi')

    def test_neuroscan_curry(self):
        process(['data/test_128/subject_02.dat'], 'oddball',
                'data/test_128_bids', 'neuroscan_curry')