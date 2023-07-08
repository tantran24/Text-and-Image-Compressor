import os
import numpy as np
from PIL import Image
from io import StringIO


class AdaptiveHuffman:
    class Node:
        def __init__(self, symbol=None, weight=0, parent=None, left=None, right=None):
            self.symbol = symbol
            self.weight = weight
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self, path=None, file=None):
        self.path = path
        if file != None:
            self.file = str(file.read())[2:]

        self.data = None
        self.tree = None
        self.dictionary = {}
        self.next_code = 0

    def initialize_tree(self):
        self.tree = self.Node(weight=0)
        self.dictionary = {}
        self.next_code = 0

    def update_tree(self, symbol):
        if symbol in self.dictionary:
            node = self.dictionary[symbol]
            while node.parent is not None:
                node.weight += 1
                node = node.parent
            node.weight += 1
        else:
            if self.tree.left is None:
                new_node = self.Node(symbol=symbol, weight=1, parent=self.tree, left=None, right=None)
                self.tree.left = new_node
                self.dictionary[symbol] = new_node
                self.next_code += 1
                self.check_node(new_node)
            else:
                node = self.tree.left
                while node.right is not None:
                    node = node.right
                new_node = self.Node(symbol=symbol, weight=1, parent=node.parent, left=None, right=None)
                node.right = new_node
                self.dictionary[symbol] = new_node
                self.next_code += 1
                self.check_node(new_node)

    def check_node(self, node):
        while node is not None:
            max_weight_node = self.get_max_weight_node(node)
            if max_weight_node is not None and max_weight_node is not node:
                self.swap_nodes(node, max_weight_node)
            node = node.parent

    def get_max_weight_node(self, node):
        max_weight_node = None
        if node is not None and node.parent is not None:
            if node.parent.left is not None:
                max_weight_node = node.parent.left
            if node.parent.right is not None and node.parent.right.weight > max_weight_node.weight:
                max_weight_node = node.parent.right
        return max_weight_node

    def swap_nodes(self, node1, node2):
        node1.symbol, node2.symbol = node2.symbol, node1.symbol
        self.dictionary[node1.symbol], self.dictionary[node2.symbol] = self.dictionary[node2.symbol], self.dictionary[node1.symbol]

    def decode_adaptive_huffman(self, encoded_data):
        decoded_string = ""
        i = 0
        while i < len(encoded_data):
            code = int(encoded_data[i])
            if code in self.dictionary:
                symbol = self.dictionary[code].symbol
                decoded_string += symbol
                self.update_tree(symbol)
            else:
                symbol = encoded_data[i + 1]
                decoded_string += symbol
                self.update_tree(symbol)
                i += 1
            i += 1
        return decoded_string

    def get_code(self, node):
        code = ""
        while node.parent is not None:
            if node.parent.left is node:
                code = "0" + code
            else:
                code = "1" + code
            node = node.parent
        return code

    def decode_adaptive_huffman(self, encode_str):
        encoded_data = encode_str.split(",")[:-1]  # Exclude the last empty element
        decoded_string = ""
        i = 0
        while i < len(encoded_data):
            code = int(encoded_data[i])
            if code in self.dictionary:
                symbol = self.dictionary[code].symbol
                decoded_string += symbol
                self.update_tree(symbol)
            else:
                symbol = encoded_data[i + 1]
                decoded_string += symbol
                self.update_tree(symbol)
                i += 1
            i += 1
        return decoded_string

    def compress(self):
        image = Image.open(self.path)
        data = np.asarray(image, dtype=np.uint8)
        string_to_encode = data.tobytes()
        compressed_data = self.encode_adaptive_huffman(string_to_encode)
        return compressed_data

    def decompress(self):
        self.initialize_tree()
        data_comp = self.file
        decoded_string = self.decode_adaptive_huffman(data_comp)
        # decompressed_image = Image.frombytes('RGB', self.get_image_size(), decoded_string)
        digitImageflaten = np.array(decoded_string, dtype=np.uint8)
        shape =(512, 512)
        digitImage = digitImageflaten.reshape(int(shape[0]), int(shape[1][:-1]), 3)
        decompressed_image = Image.fromarray(digitImage)
        return decompressed_image

    def get_image_size(self):
        with Image.open(self.path) as image:
            return image.size
