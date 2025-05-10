#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser
from tqdm.auto import tqdm
from typing import Tuple, List
import logging


logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат даты и времени
)



def init_args():
    parser = ArgumentParser()
    parser.add_argument('cache_file', type=str)
    return parser


def get_existing_cache(filename: str) -> List[Tuple[str, str]]:
    try:
        with open(filename) as f_in:
            cache_md5 = [s.strip().split('\t') for s in f_in.readlines()]
    except FileNotFoundError:
        cache_md5 = None
    
    return cache_md5

def main(args):
    cache_md5 = get_existing_cache(args.cache_file)
    old_len = len(cache_md5)
    cache_md5 = list(filter(lambda x: os.path.isfile(x[0]), cache_md5))
                
    if old_len != len(cache_md5):
        logging.info("Update cache MD5 file")
        with open(args.cache_file, 'w') as f_out:
            f_out.writelines(list(map(lambda x: f'{x[0]}\t{x[1]}\n', cache_md5)))
    else:
        logging.info("cache not changed")


if __name__ == '__main__':
    args = init_args().parse_args()
    main(args)
