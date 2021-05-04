import os
from collections import OrderedDict


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
                tmp_path = os.path.join(abs_dir, f)
                abs_file_path = os.path.abspath(tmp_path)

                if os.path.isfile(abs_file_path):

                    # logging.info('This is an abs_path')
                    # logging.info(abs_file_path)

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