# 数字媒体作业二

谢昆成

## 实验题目

使用自适应Huffman 编码对英语小说（群上提供）进行压缩。

## 实验原理

Huffman算法需要有关信息源的先验统计知识，而这样的信息通常很难获取。例如在直播或流式的音频和视频中，数据在到达前是未知的。即时能够获得这些统权值字，符号表的传输仍然是一笔相当大的开销。

自适应的Huffman编码解决了上述问题。在这种算法中，统权值字是随数据流的到达而动态收集和更新的。随着接收到的符号的概率分布的改变，符号会被赋予新的长度的码字。

自适应的Huffman编码用伪代码描述如下：

```cpp
//ENCODER 
Initial_code();
while not EOF{ 
    get(c);
    encode(c);
    update_tree(c);
}

//DECODER
Initial_code();
while not EOF{
    decode(c);
    output(c);
	update_tree(c);
}
```

在Huffman树中，总是满足如下两个原则：

1. 父节点的节点编号一定比子节点大

2. 节点编号大的节点，权重值也一定大。

这两个原则被称为**兄弟属性。**

这个属性是Huffman树中最为重要。如果违反了兄弟属性，将交换节点使其重新满足兄弟属性。

交换的方法是：

具有权值N的最远的节点将会与权值刚刚增加到N+1的节点交换。如果权值为N的节点不是叶子节点，则将该节点的整个子树与其一起交换。交换的节点不能是该节点的子节点。

在Huffman编码中，是以每个字符为单位进行编码。在扩展的Huffman编码中，可以将k个符号为一组，形成扩展的符号集。

## 实验流程

（可简述核心代码模块）

注：以下流程以非扩展的Huffman编码为例说明。扩展的Huffman编码的不同之处仅是以k个字节为单位进行编码。

本实验采用python编写，实现自适应Huffman 编码，以字节为单位进行编码。主要分为5个模块：

- 编码模块Encoder
  - 负责编码文件
- 解码模块Decoder
  - 负责解码文件
- HuffmanTree 模块，维护一棵Huffman树，功能有
  - 对字节形成HuffmanTree编码
  - HuffmanTree解码
  - 添加字节节点
  - 更新树
  - 打印树（调试用）
- 节点模块，Node，HuffmanTree的节点，负责
  - 维护节点父亲、左右孩子、权值、字节等状态信息
  - 设置左右子树
  - 与其他节点交换
  - 判断是否为某节点的祖先
- 位流模块，BitStream，以位为单位进行文件读写，功能有
  - 读取文件字节形成01字符串
  - 将01字符串编码压缩成字节写入编码文件



### 编码流程

1. Encoder以二进制方式打开一个文件
2. Encoder读取文件中的一个字节，交由HuffmanTree编码。

2. HuffmanTree判断此字节是否存在HuffmanTree中
   - 不存在则在字节的二进制编码前加上NEW节点的Huffman编码形成编码，并把此字节加入到HuffmanTree中
   - 存在则编码为HuffmanTree编码
3. HuffmanTree更新树。从刚才访问的节点向上一路更新到根节点。如果不满足兄弟属性则进行交换。
4. HuffmanTree返回编码
5. Encoder将编码交给BitStream压缩成二进制写入编码文件
6. 如果文件读取完毕，则结束，否则跳到2



### 解码流程

1. Decoder用BitStream打开编码文件，交给HuffmanTree
2. HuffmanTree读取文件中的一个位，HuffmanTree解码出叶子节点。
   - 如果此节点是NEW节点，说明有新的字符出现，读取8位产生新字符，并把此字节加入到HuffmanTree中
   - 否则，解码结果为节点的字节

2. HuffmanTree更新树。从刚才访问的节点向上一路更新到根节点。如果不满足兄弟属性则进行交换。
3. HuffmanTree返回解码字节
4. Decoder将字节写入解码文件
5. 如果文件读取完毕，则结束，否则跳到2



### 部分算法说明

#### 更新树算法

从刚才访问的节点向上一路更新到根节点。如果不满足兄弟属性则进行交换。

1. 从刚才访问的节点开始作为当前节点
2. 找到具有权值N的最远的节点
3. 如果具有权值N的最远的节点不是当前节点且非当前节点的祖先，则进行交换
4. 当前节点的权值加一，变为具有权值N+1的节点
5. 当前节点变为节点的父亲
6. 如果当前节点为空，算法结束；否则跳到2

相关代码

```python
    def updateTree(self, node):
        while node:
            node.swap(self.findFarthestNode(node.weight))
            node.weight += 1
            node = node.parent
```



#### 找到具有权值N的最远的节点算法

因为此算法从上到下，从右往左搜索节点，故第一个找到的权值为N的节点必是具有权值N的最远的节点。

1. 将根节点入队
2. 当队不空时，出队一个节点
3. 如果节点的权值等于N，返回此节点
4. 如果节点有右孩子，将其入队
5. 如果节点有左孩子，将其入队
6. 跳到2

相关代码

```python
    def findFarthestNode(self, weight):
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node.weight == weight:
                return node
            if node.right:
                q.put(node.right)
            if node.left:
                q.put(node.left)
```



#### 位流读写

位流用于以位为单位对文件进行读写，实现01字符串和字节之间的转化。位流维护一个8位的字节数据word，存放已读出或要写入的字节。pos维护读或写到第几位。

- 读

1. 若pos==-1，则读出一个字节word，pos置为7
2. 将word & 1<<pos，得出此位是0或1
3. pos-=1
4. 跳到1，直至读出长度为size的位串，读结束

相关代码

```python
    def read(self, size):
        ret = ''
        for i in range(size):
            if self.pos == -1:
                self.word = self.file.read(1)
                if self.word == b'':
                    return ''
                else:
                    self.word = ord(self.word)
                    self.pos = 7
            if self.word & (1 << self.pos):
                ret += '1'
            else:
                ret += '0'
            self.pos -= 1
        return ret
```



- 写

1. 从01字符串中得出1个字符
2. 若字符为'0'，word<<=1
3. 若字符为'1'，word<<=1; wrod+=1
4. pos-=1
5. 若pos等于-1，将word写入文件
6. 跳到1，直至写完01字符串，写结束



相关代码

```python
    def write(self, string):
        for char in string:
            if char == '0':
                self.word <<= 1
                self.pos -= 1
            elif char == '1':
                self.word <<= 1
                self.word += 1
                self.pos -= 1
            else:
                continue
            if self.pos == -1:
                self.flush()
```



## 实验结果

（压缩比、实际压缩质量等实验结果和实验参数的讨论）

- 以非扩展的Huffman编码进行编码时

原文件为92.2KB，[编码文件](./code1.txt)为52.4KB。压缩比为1.76。运行时间为83秒

- 以2个符号为一组进行扩展的Huffman编码时

原文件为92.2KB，[编码文件](./code2.txt)为46.7KB。压缩比为2.16。运行时间为400秒

- 以3个符号为一组进行扩展的Huffman编码时

原文件为92.2KB，[编码文件](./code3.txt)为49.4KB。压缩比为1.87。运行时间为1525秒。

解压后能正常阅读，和原文一致，无乱码。

在本实验中，实验参数只有k个字符为1组编码。当k=2时，压缩比最高，为2.16。但随着k的增加，压缩比却下降了。原因应该是当k增加时，一组重复出现的次数减少，从而不能很好的利用文本的冗余信息。同时，运行时间随k增加也增加得非常快。因为随k增加，节点数迅速增加，处理时间也大大增加。



## 心得体会

- 这次实验中，我实现了自适应Huffman编码，并可以以扩展的方式k位为一组进行Huffman编码。

  自适应的Huffman编码解决了传输码表花费大量开销的问题。在这种算法中，统权值字是随数据流的到达而动态收集和更新的。随着接收到的符号的概率分布的改变，符号会被赋予新的长度的码字。

- 通过这次实验，我对自适应Huffman编码的细节有了深刻的认识。在实现算法时也有自己独特的思考。

- 实现自适应Huffman编码加强了我的算法实现能力和创造力。如为了压缩成二进制编写了位流，可以以位为单位对文件进行读写，实现01字符串和字节之间的转化。

- python运行速度太慢。其弱类型也给调试带来一定的困难。个人觉得用java或c++写更好。



## 代码附录

[encode.py](./encode.py)

[decode.py](./decode.py)

[huffmanTree.py](./huffmanTree.py)

[bitStream.py](./bitStream.py)

[node.py](./node.py)