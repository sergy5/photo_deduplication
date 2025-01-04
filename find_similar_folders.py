#!/usr/bin/env python

import os
from argparse import ArgumentParser
from collections import defaultdict

from tqdm.auto import tqdm


def init_args():
    parser = ArgumentParser()
    parser.add_argument('md5_list', type=str)
    parser.add_argument('result_file', type=str)
    return parser


def main(args):
    dir_lists = defaultdict(list) # dict with sets

    # 1. build dir_sets with files
    with open(args.md5_list) as f_in:
        for s in tqdm(f_in.readlines()):
            jpg_path, md5 = s.strip().split('\t')
            jpg_dir = os.path.dirname(jpg_path)
            dir_lists[jpg_dir].append(md5)

    # 2. find intersections
    dir_with_same_files = list()
    for dir in tqdm(dir_lists):
        for dir2 in dir_lists:
            if dir != dir2:
                intersection = set.intersection(set(dir_lists[dir]), set(dir_lists[dir2]))
                if intersection:
                    dir_with_same_files.append([dir, len(dir_lists[dir]), 
                                                dir2, len(dir_lists[dir2]), 
                                                len(intersection), sorted(list(intersection))])
    
    # drop duplicates

    dir_with_same_files_dedup = list()
    for line in dir_with_same_files:
        line_reordered = [line[2], line[3], line[0], line[1], line[4], line[5]]
        if line_reordered in dir_with_same_files_dedup:
            continue
        else:
            dir_with_same_files_dedup.append(line)


    dir_with_same_files_dedup = sorted(dir_with_same_files_dedup, key=lambda x: max(x[1],x[3]), reverse=True)
    
    # 3. save result to file
    with open(args.result_file, 'w') as f_out:
        data = [ '\t'.join([str(item) for item in line]) + '\n' for line in dir_with_same_files_dedup]
        f_out.writelines(data)
    
    
if __name__ == '__main__':
    args = init_args().parse_args()
    main(args)
