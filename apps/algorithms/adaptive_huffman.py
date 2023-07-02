from PIL import Image
import os
import numpy as np


class AdaptiveHuffman_IMG:
    def __init__(self, path):
        self.path = path
        self.original_file_size = os.path.getsize(path)

    def compress(self):
        self.initCompress()
        compressedColors = []
        print("Compressing Image ...")
        compressedColors.append(self.compressColor(self.red))
        print("Compressing Image ...")
        compressedColors.append(self.compressColor(self.green))
        print("Compressing Image ...")
        compressedColors.append(self.compressColor(self.blue))
        print("Image Compressed --------- Writing to File")
        filesplit = os.path.basename(self.path).split('.')
        filename = filesplit[0] + '_AdaptiveHuffmanCompressed.txt'
        savingDirectory = os.path.join(os.getcwd(), 'CompressedFiles')
        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        with open(os.path.join(savingDirectory, filename), 'w') as file:
            for color in compressedColors:
                for row in color:
                    file.write(row)
                    file.write("\n")
        self.compressed_file_size = os.path.getsize(os.path.join(savingDirectory, filename))

    def compressColor(self, colorList):
        compressedColor = []
        for currentRow in colorList:
            compressedRow = ""
            freq_dict = {}
            huff_tree = HuffmanTree()
            for char in currentRow:
                if char not in freq_dict:
                    freq_dict[char] = 1
                else:
                    freq_dict[char] += 1
                compressedChar = huff_tree.encode(char)
                compressedRow += compressedChar
            compressedColor.append(compressedRow)
        return compressedColor

    def decompress(self):
        print("Decompressing File ...")
        image = []
        with open(self.path, "r") as file:
            for line in file:
                decodedRow = self.decompressRow(line)
                image.append(np.array(decodedRow))
        image = np.array(image)
        shapeTup = image.shape
        image = image.reshape((3, shapeTup[0] // 3, shapeTup[1]))
        self.saveImage(image)
        print("Decompression Done.")

    def decompressRow(self, line):
        currentRow = line.split(",")
        currentRow[-1] = currentRow[-1][:-1]
        decodedRow = ""
        huff_tree = HuffmanTree()
        for code in currentRow:
            decodedChar = huff_tree.decode(code)
            decodedRow += decodedChar
            huff_tree.update(decodedChar)
        newRow = decodedRow.split(',')
        decodedRow = [int(x) for x in newRow]
        return decodedRow

    def initCompress(self):
        self.image = Image.open(self.path)
        self.height, self.width = self.image.size
        self.red, self.green, self.blue = self.processImage()

    def processImage(self):
        image = self.image.convert('RGB')
        red, green, blue = [], [], []
        pixel_values = list(image.getdata())
        iterator = 0
        for height_index in range(self.height):
            R, G, B = "", "", ""
            for width_index in range(self.width):
                RGB = pixel_values[iterator]
                R = R + str(RGB[0]) + ","
                G = G + str(RGB[1]) + ","
                B = B + str(RGB[2]) + ","
                iterator += 1
            red.append(R[:-1])
            green.append(G[:-1])
            blue.append(B[:-1])
        return red, green, blue

    def saveImage(self, image):
        print("Saving Decompressed File...")
        filesplit = os.path.basename(self.path).split('_AdaptiveHuffmanCompressed.txt')
        filename = filesplit[0] + "_AdaptiveHuffmanDecompressed.jpg"
        savingDirectory = os.path.join(os.getcwd(), 'DecompressedFiles')
        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        imagelist, imagesize = self.makeImageData(image[0], image[1], image[2])
        imagenew = Image.new('RGB', imagesize)
        imagenew.putdata(imagelist)
        imagenew.save(os.path.join(savingDirectory, filename))

    def makeImageData(self, r, g, b):
        imagelist = []
        for i in range(len(r)):
            for j in range(len(r[0])):
                imagelist.append((r[i][j], g[i][j], b[i][j]))
        return imagelist, (len(r), len(r[0]))


class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None


class HuffmanTree:
    def __init__(self):
        self.root = HuffmanNode(None, 0)
        self.dictionary = {}

    def encode(self, char):
        if char not in self.dictionary:
            code = self.generate_code(char)
            self.dictionary[char] = code
            return code
        else:
            return self.dictionary[char]

    def generate_code(self, char):
        node = self.root
        code = ""
        while node.char is not None:
            if char in node.left.char:
                code += "0"
                node = node.left
            elif char in node.right.char:
                code += "1"
                node = node.right
        return code

    def decode(self, code):
        node = self.root
        for bit in code:
            if bit == "0":
                node = node.left
            elif bit == "1":
                node = node.right
        return node.char

    def update(self, char):
        node = self.root
        while node.char is not None:
            if char in node.left.char:
                node = node.left
            elif char in node.right.char:
                node = node.right
        new_node = HuffmanNode(char, 1)
        left_node = HuffmanNode(node.char, node.frequency)
        node.char = None
        node.frequency += 1
        node.left = left_node
        node.right = new_node

        if left_node.frequency > new_node.frequency:
            node.left, node.right = node.right, node.left
        self.rebalance(node)

    def rebalance(self, node):
        while node.char is None:
            left_frequency = node.left.frequency if node.left is not None else float("inf")
            right_frequency = node.right.frequency if node.right is not None else float("inf")
            min_child = node.left if left_frequency <= right_frequency else node.right
            if min_child.frequency < node.frequency:
                node.left, node.right = node.right, node.left
                node.char = min_child.char
                min_child.char = None
                min_child.frequency = 0
                node.frequency += 1
                node = min_child
            else:
                node.frequency += 1
                node = node.parent
                if node is None:
                    break