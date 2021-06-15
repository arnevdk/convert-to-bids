#!/usr/bin/env python

import click
from convert2bids.process import process


@click.command()
@click.argument('raw_files', type=click.Path(exists=True), nargs=-1)
@click.argument('task', type=click.Path())
@click.argument('output_path', type=click.Path())
def nscurry2bids(raw_files, task, output_path):
    process(raw_files, task, output_path, 'neuroscan_curry')


if __name__ == '__main__':
    nscurry2bids()
