import heapq
import numpy as np
import cv2

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class AdaptiveHuffman:
    def __init__(self):
        self.root = Node(freq=0, symbol=None)
        self.nodes = {}

    def encode_image(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        height, width = image.shape

        encoded_data = []

        for row in range(height):
            for col in range(width):
                symbol = image[row, col]

                if symbol not in self.nodes:
                    self.nodes[symbol] = Node(freq=1, symbol=symbol)
                    self.encode_symbol(self.nodes[symbol], encoded_data)

                else:
                    node = self.nodes[symbol]
                    self.update_tree(node)
                    self.encode_symbol(node, encoded_data)

        return encoded_data

    def update_tree(self, node):
        while node != self.root:
            parent = node
            siblings = [node]

            while parent is not None:
                siblings.append(parent)
                parent = parent.parent

            min_freq_node = min(siblings, key=lambda x: x.freq)

            if node.freq == min_freq_node.freq:
                min_freq_node.freq += 1
                break
            elif node.freq < min_freq_node.freq:
                min_freq_node.freq -= 1
                node.freq += 1
                break

            node = min_freq_node

    def encode_symbol(self, node, encoded_data):
        bit_string = ""
        while node != self.root:
            if node.parent.left == node:
                bit_string += "0"
            else:
                bit_string += "1"
            node = node.parent

        encoded_data.append(bit_string[::-1])

    def decode_image(self, encoded_data, output_shape):
        decoded_image = np.zeros(output_shape, dtype=np.uint8)

        current_node = self.root
        bit_index = 0

        for row in range(output_shape[0]):
            for col in range(output_shape[1]):
                while current_node.left is not None and current_node.right is not None:
                    bit = encoded_data[bit_index]

                    if bit == "0":
                        current_node = current_node.left
                    else:
                        current_node = current_node.right

                    bit_index += 1

                symbol = current_node.symbol
                decoded_image[row, col] = symbol

                if symbol not in self.nodes:
                    self.nodes[symbol] = Node(freq=1, symbol=symbol)
                    self.update_tree(self.nodes[symbol])

                else:
                    self.update_tree(self.nodes[symbol])

                current_node = self.root

        return decoded_image
