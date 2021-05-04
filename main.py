import hashlib
import logging
import os
import sys
from collections import OrderedDict

#logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s- %(message)s')

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',# this is for turning off the logging
    level=logging.DEBUG)

logging.getLogger().disabled = False


class PathOfFiles(object):
    def __init__(self, pre_fix_path):
        self._pre_fix_path = pre_fix_path
        self._abs_path_of_files_list = None
        self.get_path_of_files()
        ## key - abs path of symlink : value - abs path of origin file
        self._symlink_dict = OrderedDict()

    @property
    def pre_fix_path(self):
        return self._pre_fix_path

    @property
    def symlink_dict(self):
        return self._symlink_dict

    @property
    def abs_path_of_files_list(self):
        return self._abs_path_of_files_list

    def get_path_of_files(self):
        '''
        get the absolute path of files from the previous directory or the source directory
        :param dir_path: previous directory or source directory
        :set: set symlink_dict, abs_path_of_files_list
        '''
        abs_path_of_files_list = list()
        for abs_dir, sub_dirs, files in os.walk(self.pre_fix_path):
            for f in files:
                tmp_path = os.path.join(abs_dir,f)
                abs_file_path = os.path.abspath(tmp_path)

                if os.path.isfile(abs_file_path):

                    logging.info('This is an abs_path')
                    logging.info(abs_file_path)

                    abs_path_of_files_list.append(abs_file_path)
                elif os.path.islink(abs_file_path):
                    symlink_path_of_file = os.path.abspath(abs_file_path)
                    symlink_origin_path_of_file = os.path.abspath(os.readlink(abs_file_path))
                    self._symlink_dict[symlink_path_of_file] = symlink_origin_path_of_file
                else:
                    print(self.pre_fix_path, f)
                    raise ValueError("This is not a file nor a link")
        self._abs_path_of_files_list = abs_path_of_files_list
        return None


class ComparisonFilesPath(object):
    def __init__(self, PrePathOfFiles, sourcePathOfFiles):
        # path of files in the previous directory
        self._pre_path_of_files = PrePathOfFiles
        # path of files in the source directory
        self._source_path_of_files = sourcePathOfFiles
        self._symlinks_for_dest_dir_list = None
        self._copy_files_for_dest_dir_list = None
        self.compare_files()

    @property
    def pre_path_of_files(self):
        return self._pre_path_of_files

    @property
    def source_path_of_files(self):
        return self._source_path_of_files

    @property
    def symlinks_for_dest_dir_list(self):
        return self._symlinks_for_dest_dir_list

    @property
    def copy_files_for_dest_dir_list(self):
        return self._copy_files_for_dest_dir_list

    def __str__(self):
        return "symlinks for dest dir : {}\n copy files for dest dir {}".format(self.symlinks_for_dest_dir_list, self.copy_files_for_dest_dir_list)

    # def compare_files(pre_dir, source_dir, pre_file_path_list, source_file_path_list):
    def compare_files(self):

        '''

        :param pre_file_path_list:
        :param source_file_path_list:
        :return:
        '''
        symlinks_for_dest_dir_list = list()
        copy_files_for_dest_dir_list = list()

        pre_relative_path_of_files_list = [ i.replace(self.pre_path_of_files.pre_fix_path,"") for i in self.pre_path_of_files.abs_path_of_files_list]
        ## a src_file is in source file path list
        # for src_file in source_file_path_list:
        for abs_path_src_file in self.source_path_of_files.abs_path_of_files_list:
            src_file = abs_path_src_file.replace(self.source_path_of_files.pre_fix_path, "")
            if src_file in pre_relative_path_of_files_list:

                abs_pre_file = os.path.join(self.pre_path_of_files.pre_fix_path, src_file)
                abs_src_file = os.path.join(self.source_path_of_files.pre_fix_path, src_file)

                logging.info("This is a pre file.")
                logging.info(abs_pre_file)
                logging.info("This is a src file.")
                logging.info(abs_src_file)
                ## if the two files are identical

                logging.info('cal md5sum abs_src_file')
                logging.info(abs_src_file)
                abs_src_file_md5 = self.calculate_md5sum(abs_src_file)
                abs_pre_file_md5 = self.calculate_md5sum(abs_pre_file)
                if abs_src_file_md5 == abs_pre_file_md5:
                    symlinks_for_dest_dir_list.append(abs_src_file)
                ## if they are not identical
                else:
                    copy_files_for_dest_dir_list.append(abs_src_file)
            ## if the file in source directory is not found in the previous directory
            else:
                abs_src_file = os.path.join(source_dir, src_file)
                copy_files_for_dest_dir_list.append(abs_src_file)

        self._symlinks_for_dest_dir_list = symlinks_for_dest_dir_list
        self._copy_files_for_dest_dir_list = copy_files_for_dest_dir_list
        return None


    def calculate_md5sum(self, a_file):
        with open(a_file, 'rb')as fin:
            file_hash = hashlib.md5()
            chunk = fin.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = fin.read(8192)
        logging.info(file_hash.hexdigest())
        return file_hash.hexdigest()


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

    source_dir_files_path = PathOfFiles(source_dir)

    tmp = ComparisonFilesPath(pre_dir_files_path, source_dir_files_path)
    print(tmp)
    print(pre_dir_files_path.symlink_dict)

    # validate_files_path(pre_path)
    # validate_files_path(source_path)
    pass


if __name__ == '__main__':
    #pre_dir = '/Users/Jay.Kim/rsync-test/latest/'
    #source_dir = '/Users/Jay.Kim/rsync-test/source/'

    pre_dir, source_dir = sys.argv[1], sys.argv[2]
    test(pre_dir, source_dir)
    ##main()
