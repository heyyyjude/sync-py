import os
import hashlib
import logging


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',  # this is for turning off the logging
                    level=logging.DEBUG)

logging.getLogger().disabled = False


class ComparisonPathOfFiles(object):
    def __init__(self, PrePathOfFiles, sourcePathOfFiles):
        # path of files in the previous directory
        self._pre_path_of_files = PrePathOfFiles
        # path of files in the source directory
        self._source_path_of_files = sourcePathOfFiles
        self._symlinks_for_dest_dir_list = None
        self._copy_files_for_dest_dir_list = None
        self.compare_files()

    @property
    def pre_dir_pre_fix_path(self):
        return self._pre_path_of_files.pre_fix_path

    @property
    def source_dir_pre_fix_path(self):
        return self._source_path_of_files.pre_fix_path

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
        return "symlinks for dest dir : {}\n copy files for dest dir {}".format(self.symlinks_for_dest_dir_list,
                                                                                self.copy_files_for_dest_dir_list)

    # def compare_files(pre_dir, source_dir, pre_file_path_list, source_file_path_list):
    def compare_files(self):

        '''

        :param pre_file_path_list:
        :param source_file_path_list:
        :return:
        '''

        logging.info("self.pre_dir_pre_fix_path")
        logging.info(self.pre_dir_pre_fix_path)
        logging.info("self.source_dir_pre_fix_path")
        logging.info(self.source_dir_pre_fix_path)

        symlinks_for_dest_dir_list = list()
        copy_files_for_dest_dir_list = list()

        pre_relative_path_of_files_list = [i.replace(self.pre_dir_pre_fix_path, "") for i in
                                           self.pre_path_of_files.abs_path_of_files_list]

        for abs_path_src_file in self.source_path_of_files.abs_path_of_files_list:

            src_file = abs_path_src_file.replace(self.source_dir_pre_fix_path, "")
            if src_file in pre_relative_path_of_files_list:

                abs_pre_file = os.path.abspath(self.pre_dir_pre_fix_path + src_file)
                assert (os.path.isfile(abs_pre_file))

                abs_src_file = os.path.abspath(self.source_dir_pre_fix_path + src_file)
                assert (os.path.isfile(abs_pre_file))

                ## if the two files are identical                logging.info("\n")
                logging.info("---begin to calculate md5sum---")
                logging.info("This is an abs path of a file in the previous directory and its md5sum.")
                logging.debug(abs_pre_file)

                abs_pre_file_md5 = self.calculate_md5sum(abs_pre_file)
                logging.debug(abs_pre_file_md5)

                logging.info("This is an abs path of a file in the source directory and its md5sum.")
                logging.debug(abs_src_file)

                abs_src_file_md5 = self.calculate_md5sum(abs_src_file)
                logging.debug(abs_src_file_md5)
                logging.info('---End calculating md5sum---')
                logging.info("\n")

                if abs_src_file_md5 == abs_pre_file_md5:
                    symlinks_for_dest_dir_list.append(abs_src_file)
                ## if they are not identical
                else:
                    copy_files_for_dest_dir_list.append(abs_src_file)
            ## if the file in source directory is not found in the previous directory
            else:
                ## abs_src_file = os.path.join(source_dir, src_file)
                copy_files_for_dest_dir_list.append(abs_path_src_file)

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
        return file_hash.hexdigest()
