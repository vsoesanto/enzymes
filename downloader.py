import ftputil
import os

base_path = "./pubmed/baseline-2018-sample"
host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous', 'password')
host.chdir('/pubmed/baseline-2018-sample/')

# downloads files from host: ftp.ncbi.nlm.nih.gov/pubmed/baseline-2018-sample/
file_list = host.listdir(host.curdir)
for i, file_name in enumerate(file_list):
    if file_name[-3:] == ".gz":
        print("File " + file_name)
        print(os.path.join(base_path,file_name))
        print("Downloading file " + os.path.join(base_path, file_name))
        host.download(file_name, os.path.join(base_path, file_name), callback=None)

    if i == 99:
        break

