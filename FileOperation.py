"""
# @author: xuwang
# @function: 文件操作（压缩及解压）
# @date: 2017/11/20 22:24
"""
import  six
import os
import sys
from HuffmanTree import HuffmanTree
from HuffmanTree import HuffmanTreeOperation
class FileOperation(object):
    def __init__(self):
        pass


    def zipFile(self, originalFileName, zipFileName):
        zipFileWrite = open(zipFileName, 'wb')

        with open(originalFileName, 'rb') as originalFile:
            originalData = originalFile.read()
        # print(type(originalData))
        # print(len(originalData))
        # print(originalDataLength)
        # for i in range(originalDataLength):
        #     print(originalData[i])
        intValueWeightDict = {} # 统计原始文件中的各个字节出现的次数即weight
        for i in range(len(originalData)):
            if not (originalData[i] in intValueWeightDict.keys()):
                intValueWeightDict[originalData[i]] = 1
            else:
                intValueWeightDict[originalData[i]] = intValueWeightDict[originalData[i]] + 1
        # 构造初始HuffmanTree，每个字节为一个Tree
        huffmanTreeList = []
        for intValue in intValueWeightDict:
            # print(byteValue)
            # print(byteNumDict[byteValue])
            huffmanTree = HuffmanTree(rootFlag=0, value=intValue, weight=intValueWeightDict[intValue])
            # print(huffmanTree.getWeight())
            huffmanTreeList.append(huffmanTree)

        # 调用BuildHuffmanTree构造一个完整的huffmanTree
        huffmanTreeOperation = HuffmanTreeOperation()
        huffmanTree = huffmanTreeOperation.getHuffmanTree(huffmanTreeList)

        # 存储huffmanTree中的各个字节的int型value对应的字符串编码
        # {intValue:huffmanCode}
        huffmanCodeDict = huffmanTreeOperation.getHuffmanCode(huffmanTree=huffmanTree, huffmanCodeDict={}, binaryCode="")

        # 存储原始文件总的字符的个数信息，方便解压缩
        originalDataLength = len(intValueWeightDict.keys())
        originalDataLen_0 = originalDataLength & 255 # 最低8位
        originalDataLength = originalDataLength >> 8
        originalDataLen_1 = originalDataLength & 255
        originalDataLength = originalDataLength >> 8
        originalDataLen_2 = originalDataLength & 255
        originalDataLength = originalDataLength >> 8
        originalDataLen_3 = originalDataLength & 255

        zipFileWrite.write(six.int2byte(originalDataLen_0))
        zipFileWrite.write(six.int2byte(originalDataLen_1))
        zipFileWrite.write(six.int2byte(originalDataLen_2))
        zipFileWrite.write(six.int2byte(originalDataLen_3))


        # 存储原始文件的weight信息
        for intValue in intValueWeightDict.keys():
            # 以byte形式存储原始数据value，占一个字节

            zipFileWrite.write(six.int2byte(intValue))

            # 以byte形式存储原始数据value对应的权重，占4个字节
            weight = intValueWeightDict[intValue]
            weight_0 = weight & 255
            weight = weight >> 8
            weight_1 = weight & 255
            weight = weight >> 8
            weight_2 = weight & 255
            weight = weight >> 8
            weight_3 = weight & 255

            zipFileWrite.write(six.int2byte(weight_0))
            zipFileWrite.write(six.int2byte(weight_1))
            zipFileWrite.write(six.int2byte(weight_2))
            zipFileWrite.write(six.int2byte(weight_3))


        binaryCode = ''
        for i in range(len(originalData)):
            intData = originalData[i]
            binaryCode = binaryCode + huffmanCodeDict[intData]
            outputValue = 0 # 8位一输出
            while len(binaryCode) > 8:
                for j in range(8):
                    outputValue = outputValue << 1
                    if binaryCode[j] == "1":
                        outputValue = outputValue | 1
                binaryCode = binaryCode[8:]

                zipFileWrite.write(six.int2byte(outputValue))

                outputValue = 0

        # 若最后有不满8位的binaryCode

        zipFileWrite.write(six.int2byte(len(binaryCode)))

        outputValue = 0
        for i in range(len(binaryCode)):
            outputValue = outputValue << 1
            if binaryCode[i] == "1":
                outputValue = outputValue | 1
        for i in range(8-len(binaryCode)):
            # 补0，补全8位
            outputValue = outputValue << 1

        zipFileWrite.write(six.int2byte(outputValue))

        zipFileWrite.close()

    def unzipFile(self, zipFileName, unzipFileName):
        unzipFileWrite = open(unzipFileName, "wb")
        # 以二进制格式读取文件
        with open(zipFileName, "rb") as zipFile:
            zipFileData = zipFile.read()
        '''
        压缩文件结构：
        1. 4个byte的叶节点个数，低八位在前
        2. 各个叶节点的value值和其对应的weight（1个byte的value值，4个byte的weight（低八位在前））
           一共有第一步统计的数值的个数
        3：源文件的huffman码存储，8个凑为一个字节存储
           
        '''

        # 读取前四个字节，为原文件中字节的int型value的总个数，即huffmanTree的叶节点个数，低8位开始
        leafNodeNum_0 = zipFileData[0] # 最低8位
        leafNodeNum_1 = zipFileData[1]
        leafNodeNum_2 = zipFileData[2]
        leafNodeNum_3 = zipFileData[3]

        # 计算叶节点个数
        leafNodeNum = 0
        leafNodeNum = leafNodeNum | leafNodeNum_3 #先计算高八位
        leafNodeNum = leafNodeNum << 8
        leafNodeNum = leafNodeNum | leafNodeNum_2
        leafNodeNum = leafNodeNum << 8
        leafNodeNum = leafNodeNum | leafNodeNum_1
        leafNodeNum = leafNodeNum << 8
        leafNodeNum = leafNodeNum | leafNodeNum_0

        # 读取各个叶节点的value值和其对应的weight，存入intValueWeightDict
        # 从zipFileData[4]开始
        intValueWeightDict = {}
        for i in range(leafNodeNum):
            intValue = zipFileData[4 + i * 5 + 0]

            # 4个字节的权重，低八位在前
            weight_0 = zipFileData[4 + i * 5 + 1]
            weight_1 = zipFileData[4 + i * 5 + 2]
            weight_2 = zipFileData[4 + i * 5 + 3]
            weight_3 = zipFileData[4 + i * 5 + 4]
            # 计算weight
            weight = 0
            weight = weight | weight_3  # 先计算高八位
            weight = weight << 8
            weight = weight | weight_2
            weight = weight << 8
            weight = weight | weight_1
            weight = weight << 8
            weight = weight | weight_0

            intValueWeightDict[intValue] = weight

        # 根据得到的intValueWeightDict构建huffmanTree
        # 构造初始HuffmanTree，每个字节为一个Tree
        huffmanTreeList = []
        for intValue in intValueWeightDict:
            # print(byteValue)
            # print(byteNumDict[byteValue])
            huffmanTree = HuffmanTree(rootFlag=0, value=intValue, weight=intValueWeightDict[intValue])
            # print(huffmanTree.getWeight())
            huffmanTreeList.append(huffmanTree)
        # 调用BuildHuffmanTree构造一个完整的huffmanTree
        huffmanTreeOperation = HuffmanTreeOperation()
        huffmanTree = huffmanTreeOperation.getHuffmanTree(huffmanTreeList)
        # 存储huffmanTree中的各个字节的int型value对应的字符串编码
        # {intValue:huffmanCode}
        huffmanCodeDict = huffmanTreeOperation.getHuffmanCode(huffmanTree=huffmanTree, huffmanCodeDict={}, binaryCode="")

        # 对源文件压缩部分进行解压缩
        binaryCode = ""
        currentNode = huffmanTree.getRoot()
        for i in range(leafNodeNum * 5 + 4, len(zipFileData)):
            intValue = zipFileData[i]
            for j in range(8):
                if intValue & 128:
                    binaryCode = binaryCode + "1"
                else:
                    binaryCode = binaryCode + "0"
                intValue = intValue << 1

            #因为256个编码的huffman树最多8层，24个足够
            while len(binaryCode) > 24:
                if currentNode.isLeafNode():
                    unzipFileWrite.write(six.int2byte(currentNode.getValue()))
                    currentNode = huffmanTree.getRoot()

                if binaryCode[0] == "1":
                    currentNode = currentNode.getRightChild()
                else:
                    currentNode = currentNode.getLeftChild()
                binaryCode = binaryCode[1:]

        #处理最后24位
        subBinaryCode = binaryCode[-16:-8]
        lastLength = 0
        for i in range(8):
            lastLength = lastLength << 1
            if subBinaryCode[i] == "1":
                lastLength = lastLength | 1
        binaryCode = binaryCode[:-16] + binaryCode[-8:-8 + lastLength]
        while len(binaryCode) > 0:
            if currentNode.isLeafNode():
                unzipFileWrite.write(six.int2byte(currentNode.getValue()))
                currentNode = huffmanTree.getRoot()
            if binaryCode[0] == "1":
                currentNode = currentNode.getRightChild()
            else:
                currentNode = currentNode.getLeftChild()
            binaryCode = binaryCode[1:]

        if currentNode.isLeafNode():
            unzipFileWrite.write(six.int2byte(currentNode.getValue()))
            currentNode = huffmanTree.getRoot()

        unzipFileWrite.close()



