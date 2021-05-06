import argparse
import logging
import os
import sys

from comparison_path_files import ComparisonPathOfFiles
from path_of_files import PathOfFiles
from copy_files_and_hard_links import CopyFilesHardlinks

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)

# this is for turning off the logging
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


def main(backup_dir, source_dir, dest_dir):
    backup_dir_files_path = PathOfFiles(backup_dir)
    source_dir_files_path = PathOfFiles(source_dir)
    comparison = ComparisonPathOfFiles(backup_dir_files_path, source_dir_files_path)
    start = CopyFilesHardlinks(comparison, dest_dir)
    start.run()


def test(pre_dir, source_dir, dest_dir):
    pre_dir_files_path = PathOfFiles(pre_dir)
    print(pre_dir_files_path.symlink_dict)

    logging.info("backup-dir-prefix_path")
    logging.info(pre_dir_files_path.prefix_path)

    source_dir_files_path = PathOfFiles(source_dir)
    logging.info("source-dir-prefix-path")
    logging.info(source_dir_files_path.prefix_path)

    tmp = ComparisonPathOfFiles(pre_dir_files_path, source_dir_files_path)

    print("hardlinks - unchanged")
    print(tmp.hardlinks_path_from_previous_dir_list)

    print("copy files - changed")
    print(tmp.copy_files_path_from_source_dir_list)
    start = CopyFilesHardlinks(tmp, dest_dir)
    start.run()

    logging.info("hard links backup to dest")
    logging.debug(start.hard_links_list)


if __name__ == '__main__':
    # backup_dir = '/Users/Jay.Kim/rsync-test/latest/'
    # source_dir = '/Users/Jay.Kim/rsync-test/source/'
    # dest_dir = '/Users/Jay.Kim/rsync-test/dest_dir/'

    # backup_dir, source_dir, dest_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    # test(backup_dir, source_dir, dest_dir)

    parser = argparse.ArgumentParser(description="Python scripts for doing the rsync link-dest job")

    parser.add_argument('-b',
                        '--backup_dir',
                        action='store',
                        type=str,
                        required=True,
                        help="backup-dir",
                        )

    parser.add_argument('-s',
                        '--source_dir',
                        action='store',
                        type=str,
                        required=True,
                        help='source-dir',
                        )
    parser.add_argument('-d',
                        '--dest_dir',
                        action='store',
                        type=str,
                        required=True,
                        help='dest-dir',
                        )

    args = parser.parse_args()

    main(args.backup_dir, args.source_dir, args.dest_dir)
