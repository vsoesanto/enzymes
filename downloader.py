import ftputil
import os
from read_xml import XMLReader
import util

base_path = "../pubmed/baseline-2018-sample"  # local folder where downloaded files will reside in
host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')  # set up FTP server credentials
host.chdir('/pubmed/baseline-2018-sample/')  # change into desired directory
enzyme_list = util.get_enzymes()  # retrieve given list of enzymes to find in abstracts

# downloading files from host: ftp.ncbi.nlm.nih.gov/pubmed/baseline-2018-sample/
abstracts = []
file_list = host.listdir(host.curdir)  # get file list in directory
for i, file_name in enumerate(file_list):
    if file_name[-3:] == ".gz":  # ensure files end with .gz extension
        print("File " + file_name)
        # location of downloaded file
        print("Downloading file to " + os.path.join(base_path, file_name))
        # download file from FTP server
        host.download(file_name, os.path.join(base_path, file_name), callback=None)

        downloaded_file_path_gz = base_path + "/" + file_name
        util.unzip(downloaded_file_path_gz)  # unzip .gz file so the contents can be read
        downloaded_file_path_xml = downloaded_file_path_gz[:-3]  # path of the .xml file
        file_reader = XMLReader(downloaded_file_path_xml)  # create an XMLReader object (supply path to .xml file)
        file_reader.read()  # read the .xml file

        file_reader.get(enzyme=None, enzyme_list=enzyme_list)
        # abstracts_with_enzymes = file_reader.get("TRANSCARBAMOYLASE")
        if len(file_reader.abstracts) == 0:
            print("File does not contain any enzymes from list")
        else:
            abstracts.extend(file_reader.abstracts)

        os.remove(downloaded_file_path_xml)
        print()


util.write(abstracts)


