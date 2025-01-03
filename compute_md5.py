#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser
import hashlib
from multiprocessing import Pool
from tqdm.auto import tqdm


def calculate_md5(file_path):
    """Функция для вычисления MD5-хеша одного файла."""
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_path, file_hash.hexdigest()


def init_args():
    parser = ArgumentParser()
    parser.add_argument('--num_threads', type=int, default=10)
    parser.add_argument('input_dir', type=str)
    parser.add_argument('result_file', type=str)
    return parser


def main(args):
    files_to_process = list()
    for root,_, files in os.walk(args.input_dir):
        for f in files:
            full_path = os.path.join(root, f)
            files_to_process.append(full_path)

    with Pool(args.num_threads) as pool:
        results = list(tqdm(pool.imap_unordered(calculate_md5, files_to_process), 
                            total=len(files_to_process)))
        
    print('save md5 to file')
    with open(args.result_file, 'w') as f_out:
        f_out.writelines(list(map(lambda x: f'{x[0]}\t{x[1]}\n', results)))


if __name__ == '__main__':
    args = init_args().parse_args()
    main(args)
