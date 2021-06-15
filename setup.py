#!/usr/bin/env python

from distutils.core import setup

setup(name='convert2bids',
      version='0.0',
      description='Convert the biosensor data recorded with the lab equipment '
                  'to a clean and BIDS-compliant dataset',
      author='Arne Van Den Kerchove',
      author_email='arne@vandenkerchove.com',
      packages=[
          'click==8.0.1',
          'mne==0.23.0',
          'mne-bids==0.7',
          'numpy==1.20.3',
          'scipy==1.6.3',
      ],
      )
