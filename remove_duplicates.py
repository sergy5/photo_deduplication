#!/usr/bin/env python

import os
from argparse import ArgumentParser
from collections import defaultdict
import json
import logging
import shutil

from tqdm.auto import tqdm


def init_args():
    parser = ArgumentParser()
    parser.add_argument('similar_file_list', type=str)
    parser.add_argument('cache_md5', type=str)
    return parser


def read_cache_md5(f_cache_md5: str) -> dict:
    cache_md5 = dict()
    with open(f_cache_md5) as f_in:
        data = f_in.readlines()
        for line in tqdm(data):
            f, md5 = line.strip().split('\t')
            if os.path.dirname(f) not in cache_md5:
                cache_md5[os.path.dirname(f)] = defaultdict(str)
            cache_md5[os.path.dirname(f)][md5] = os.path.basename(f)

    return cache_md5


def main(args):

    logging.info('reading cache md5 file')
    cache_md5 = read_cache_md5(args.cache_md5)

    # 1. select bigger dir in pair
    with open(args.similar_file_list) as f_in:
        data = f_in.readlines()
        for line in tqdm(data):
            dir1, len_dir1, dir2, len_dir2, _, filelist_str =  line.strip().split('\t')

            if len_dir1 == len_dir2:
                logging.warning(f'equal dirs:\t{dir1}\t{dir2}')
            biggest_dir, smallest_dir = (dir1,dir2) if int(len_dir1) > int(len_dir2) else (dir2,dir1)
            # 2. check that files in smaller dir all exist (smaller dir, file_list, cache_md5)
            ok = True
            for md5 in json.loads(filelist_str.replace("'", '"')):
                if not os.path.isfile(os.path.join(smallest_dir, cache_md5[smallest_dir][md5])):
                    ok=False
                    break    
            if not ok:
                continue

            # 3. if 2 is True, than move to thrash on disk files in bigger dir (bigger dir, file_list, cache_md5)
        
            thrash_dir = 'Thrash_duplicates'
            for md5 in json.loads(filelist_str.replace("'", '"')):
                filename = os.path.join(biggest_dir, cache_md5[biggest_dir][md5])
                if thrash_dir == 'Thrash_duplicates':
                    drive, _ = os.path.splitdrive(filename)
                    thrash_dir = os.path.join(drive, thrash_dir)
                    if not os.path.isdir(thrash_dir):
                        os.mkdir(thrash_dir)
                
                if os.path.isfile(filename):
                    filename_thrash = os.path.join(thrash_dir, os.path.splitdrive(filename)[1].lstrip('/'))
            
                    logging.info(f'move {filename} to {filename_thrash}')
                    if not os.path.isdir(os.path.dirname(filename_thrash)):
                        os.makedirs(os.path.dirname(filename_thrash))
                    shutil.move(filename, filename_thrash)

    
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level='INFO')
    args = init_args().parse_args()
    main(args)
