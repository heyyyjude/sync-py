import hashlib
import logging
import os
import sys
from collections import OrderedDict
from comparison_path_files import ComparisonPathOfFiles
from path_of_files import PathOfFiles

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',  # this is for turning off the logging
                    level=logging.DEBUG)

logging.getLogger().disabled = False


def validate_files_path(a_file):
    '''
    validate files in lists
    :param file_path_list:
    :return: None or Error raised.
    '''

    ## key - abs path of symlink : value - abs path of origin file
    symlink_path_of_file = None
    symlink_origin_path_of_file = None
    if os.path.isfile(a_file):
        pass
    elif os.path.islink(a_file):
        os.readlink(a_file)

        symlink_path_of_file = os.path.abspath(a_file)
        symlink_origin_path_of_file = os.path.abspath(os.readlink(a_file))
    else:
        print("Error")
        print(a_file)
        raise ValueError('This is not a file nor a link')
    logging.info('Validation is done')
    return symlink_path_of_file, symlink_origin_path_of_file


def create_symlinks(pre_file, dest_file):
    pass


def copy_file(source_file, dest_file):
    pass


def main():
    pass


def test(pre_dir, source_dir):
    pre_dir_files_path = PathOfFiles(pre_dir)
    logging.info("pre_dir_pre_fix_path")
    logging.info(pre_dir_files_path.pre_fix_path)

    source_dir_files_path = PathOfFiles(source_dir)
    logging.info("source_dir_pre_fix_path")
    logging.info(source_dir_files_path.pre_fix_path)

    tmp = ComparisonPathOfFiles(pre_dir_files_path, source_dir_files_path)

    print(tmp.symlinks_for_dest_dir_list)
    print(tmp.copy_files_for_dest_dir_list)

    # validate_files_path(pre_path)
    # validate_files_path(source_path)
    pass


if __name__ == '__main__':
    pre_dir = '/Users/Jay.Kim/rsync-test/latest/'
    source_dir = '/Users/Jay.Kim/rsync-test/source/'

    # pre_dir, source_dir = sys.argv[1], sys.argv[2]
    test(pre_dir, source_dir)
    ##main()
