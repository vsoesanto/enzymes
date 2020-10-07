import ftputil
import os
from read_xml import XMLReader
import util

base_path = "../pubmed/baseline-2018-sample"  # local folder where downloaded files will reside in
host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
host.chdir('/pubmed/baseline-2018-sample/')
enzymes_list = util.get_enzymes()

# downloads files from host: ftp.ncbi.nlm.nih.gov/pubmed/baseline-2018-sample/
abstracts = []
file_list = host.listdir(host.curdir)
for i, file_name in enumerate(file_list):
    if file_name[-3:] == ".gz":
        print("File " + file_name)
        # print(os.path.join(base_path, file_name))  # location of file

        print("Downloading file to " + os.path.join(base_path, file_name))
        host.download(file_name, os.path.join(base_path, file_name), callback=None)

        downloaded_file_path = base_path + "/" + file_name
        util.unzip(downloaded_file_path)
        file_reader = XMLReader(downloaded_file_path[:-3])
        file_reader.read()

        # abstracts_with_enzymes = file_reader.get(enzymes_list)
        abstracts_with_enzymes = file_reader.get("TRANSCARBAMOYLASE")
        if len(abstracts_with_enzymes) == 0:
            print("File does not contain any enzymes from list")
            os.remove(downloaded_file_path[:-3])
        else:
            abstracts.extend(abstracts_with_enzymes)
            break
        print()

print(abstracts)


