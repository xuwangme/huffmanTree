"""
# @author: xuwang
# @function: huffman Tree的相关类
# @date: 2017/11/20 16:14
"""
import abc

# 定义HuffmanTree节点抽象类
class HuffmanNode(object):

    __metaclass__ = abc.ABCMeta

    # 返回当前节点权重
    @abc.abstractmethod
    def getWeight(self):
        return
    # 返回当前节点是否为叶子节点
    @abc.abstractmethod
    def isLeafNode(self):
        return

# 定义叶子节点类
class LeafNode(HuffmanNode):

    def __init__(self, weight=0, value=0):
        super(LeafNode, self).__init__()

        self.weight = weight # 当前节点权重
        self.value = value # 当前节点的字符值

    def getWeight(self):
        return self.weight

    def isLeafNode(self):
        return True

    # 返回当前节点的字符值
    def getValue(self):
        return self.value

# 定义中间节点类
class IntermediateNode(HuffmanNode):

    def __init__(self, leftChild=None, rightChild=None):
        super(IntermediateNode, self).__init__()

        self.leftChild = leftChild # 左孩子
        self.rightChild = rightChild # 右孩子
        self.weight = leftChild.getWeight() + rightChild.getWeight() # 得到当前节点的权重

    def getWeight(self):
        return self.weight

    def isLeafNode(self):
        return False

    # 返回当前节点的左孩子
    def getLeftChild(self):
        return self.leftChild

    # 返回当前节点的右孩子
    def getRightChild(self):
        return self.rightChild

# 定义huffmanTree类
class HuffmanTree(object):

    def __init__(self, rootFlag, value=0, weight=0, leftTree=None, rightTree=None):

        super(HuffmanTree, self).__init__()
        self.leftTree = leftTree
        self.rightTree = rightTree

        if rootFlag == 0:
            self.root = LeafNode(weight=weight, value=value)  # 只有一个点
        else:
            self.root = IntermediateNode(leftChild=leftTree.getRoot(), rightChild=rightTree.getRoot())

    def getRoot(self):
        """
        获取huffman tree 的根节点
        """
        return self.root

    def getWeight(self):
        """
        获取这个huffman树的根节点的权重
        """
        return self.root.getWeight()

    def getLeftTree(self):
        return self.leftTree

    def getRightTree(self):
        return self.rightTree

     #     """
    #     利用递归的方法遍历huffman_tree，并且以此方式得到每个 字符 对应的huffman编码
    #     保存在字典 char_freq中
    #     """
    #     if root.isleaf():
    #         char_freq[root.get_value()] = code
    #         print("it = %c  and  freq = %d  code = %s") % (chr(root.get_value()), root.get_wieght(), code)
    #         return None
    #     else:
    #         self.traverse_huffman_tree(root.get_left(), code + '0', char_freq)
    #         self.traverse_huffman_tree(root.get_right(), code + '1', char_freq)

class HuffmanTreeOperation(object):

    def getHuffmanTree(self, huffmanTreeList):
        while (len(huffmanTreeList) > 1):
            huffmanTreeList.sort(key=lambda x: x.getWeight()) #将list中的huffmanTree按照根节点权重从小到大排列

            newHuffmanTree = HuffmanTree(rootFlag=1, rightTree=huffmanTreeList[0], leftTree=huffmanTreeList[1])# 取最小权重的两个树组成新的树
            huffmanTreeList = huffmanTreeList[2:] # 去掉最小的两个
            huffmanTreeList.append(newHuffmanTree)# 加入新的

        return huffmanTreeList[0]

    # 宽度优先遍历树
    def widthFirstTraversal(self,huffmanTree, nodeWeightList):
        # nodeWeightList.append(huffmanTree.getWeight())
        #递归截止条件
        if huffmanTree.getRoot().isLeafNode():
            nodeWeightList.append(huffmanTree.getWeight())
            return nodeWeightList

        self.widthFirstTraversal(huffmanTree.getLeftTree(), nodeWeightList)
        self.widthFirstTraversal(huffmanTree.getRightTree(), nodeWeightList)

        return nodeWeightList

    def getHuffmanCode(self, huffmanTree, huffmanCodeDict, binaryCode):
        # 递归截止条件
        if huffmanTree.getRoot().isLeafNode():
            huffmanCodeDict[huffmanTree.getRoot().getValue()] = binaryCode
            return huffmanCodeDict

        self.getHuffmanCode(huffmanTree.getLeftTree(), huffmanCodeDict, binaryCode+"0")

        self.getHuffmanCode(huffmanTree.getRightTree(), huffmanCodeDict, binaryCode+"1")

        return huffmanCodeDict