## Huffman Tree Code 说明文档

------

### 1. 关于程序 Huffman Code

#### 1.1    Problem

​	Write a programin your favorate language to compress a file using Huffman code and thendecompress it. Code information may be contained in the compressed file if youcan. Use your program to compress the two files (graph.txt and AesopFables.txt) and compare the results (Huffman code and compression ratio). 

#### 1.2    Engineering structure

采用python语言进行编程，                

其中：

- HuffmanTree.py中包含HuffmanNode节点抽象类，LeafNode叶子结点类，IntermediateNode中间节点类，HuffmanTree哈夫曼树类，HuffmanTreeOperation哈夫曼树操作类；
- FileOpreation.py中包括FileOperation文件操作类，类中包含zipFile()和unzipFile()两种方法用来压缩和解压文件；
- Main.py中为对文件进行压缩和解压的主函数。

通过对graph.txt和Aesop_Fables.txt进行压缩和解压，成功得到压缩文件，压缩文件大小如下：

 

| 文件名           | 原文件大小 | 压缩后文件大小 | 压缩比 |
| ---------------- | ---------- | -------------- | ------ |
| graph.txt        | 2046KB     | 909KB          | 44.43% |
| Aesop_Fables.txt | 186KB      | 107KB          | 57.52% |

 

通过上表我们可以发现，huffman编码压缩文件对大文件的压缩率更高，graph.txt的压缩比达到了44.43%，Aesop Fables.txt文件的压缩率为58.52%。

 

最后，我们用解压缩程序对文件进行解压，成功得到解压文件，通过比对解压后文件和原文件的各项HASH值，判定解压文件和原文件是一样的，说明我们的压缩算法是正确的！

 



