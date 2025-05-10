#!/usr/bin/env python

import sys
import os
from argparse import ArgumentParser
import hashlib
from multiprocessing import Pool
from tqdm.auto import tqdm
from typing import Tuple, List
import logging


logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат даты и времени
)


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


def get_existing_cache(filename: str) -> List[Tuple[str, str]]:
    try:
        with open(filename) as f_in:
            cache_md5 = [s.strip().split('\t') for s in f_in.readlines()]
    except FileNotFoundError:
        cache_md5 = None
    
    return cache_md5
            

def get_files_not_in_cache(cache: List[Tuple[str, str]], files: List[str]) -> List[str]:
    cached_files = set([item[0] for item in cache])
    files = list(set(files) - cached_files)
    return files


def main(args):
    files_to_process = list()
    for root,_, files in os.walk(args.input_dir):
        for f in files:
            full_path = os.path.join(root, f)
            files_to_process.append(full_path)

    logging.info(f"files found: {len(files_to_process)}")
    cache_md5 = get_existing_cache(args.result_file)

    logging.info(f"cached_files: {len(cache_md5)}")
    files_to_process = get_files_not_in_cache(cache_md5, files_to_process)
    logging.info(f"new files for compute cache md5: {len(files_to_process)}")

    with Pool(args.num_threads) as pool:
        results = list(tqdm(pool.imap_unordered(calculate_md5, files_to_process, chunksize=10), 
                            total=len(files_to_process)))
        
    if results:
        cache_md5.extend(results)
        
        logging.info("Update cache MD5 file")
        with open(args.result_file, 'w') as f_out:
            f_out.writelines(list(map(lambda x: f'{x[0]}\t{x[1]}\n', cache_md5)))


if __name__ == '__main__':
    args = init_args().parse_args()
    main(args)
