"""
# @author: xuwang
# @function: 主程序入口
# @date: 2017/11/20 22:33
"""
from FileOperation import FileOperation


if __name__ == '__main__':
    fileOperation = FileOperation()

    # # 压缩文件
    # originalFileName = "./data/Aesop_Fables.txt"# 原始文件名
    # compressedFileName = "./data/Aesop_Fables_zip.txt"# 压缩后文件名
    # fileOperation.zipFile(originalFileName, compressedFileName)

    # 解压文件
    zipFileName = "./data/Aesop_Fables_zip.txt"# 压缩文件名
    unzipFileName = "./data/Aesop_Fables_zip_unzip.txt"# 解压后文件名
    fileOperation.unzipFile(zipFileName=zipFileName, unzipFileName=unzipFileName)