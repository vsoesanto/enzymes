import os
import gzip

dir_name = "./pubmed/baseline-2018-sample"
extension = ".gz"

os.chdir(dir_name)

# unzips .gz files automatically
for item in os.listdir("./"):  # loop through items in dir
    file_name = os.path.abspath(item)  # get full path of files
    if file_name.endswith(extension):
        with gzip.open(file_name, mode="rb") as gz_file:
            output = open(file_name[:-3], "wb")
            print("Creating file: " + file_name[:-3])
            gz_file_content = gz_file.read()
            output.write(gz_file_content)
            output.close()
            os.remove(file_name)


