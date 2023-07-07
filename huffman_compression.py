import heapq
from collections import Counter


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_frequency_table(text):
    frequency_table = Counter(text)
    return frequency_table


def build_huffman_tree(frequency_table):
    heap = [HuffmanNode(char, freq) for char, freq in frequency_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged_freq = node1.freq + node2.freq
        merged_node = HuffmanNode(None, merged_freq)
        merged_node.left = node1
        merged_node.right = node2

        heapq.heappush(heap, merged_node)

    return heap[0]


def build_codewords_mapping(node, current_code, codewords_mapping):
    if node.char is not None:
        codewords_mapping[node.char] = current_code
        return

    build_codewords_mapping(node.left, current_code + '0', codewords_mapping)
    build_codewords_mapping(node.right, current_code + '1', codewords_mapping)


def get_encoding_table(codewords_mapping):
    encoding_table = {}
    for char, codeword in codewords_mapping.items():
        encoding_table[codeword] = char
    return encoding_table


def compress(text):
    frequency_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(frequency_table)

    codewords_mapping = {}
    build_codewords_mapping(huffman_tree, '', codewords_mapping)

    compressed_text = ''.join(codewords_mapping[char] for char in text)

    return compressed_text, get_encoding_table(codewords_mapping)


def decompress(compressed_text, encoding_table):
    decoded_text = ""
    codeword = ""
    for bit in compressed_text:
        codeword += bit
        if codeword in encoding_table:
            decoded_text += encoding_table[codeword]
            codeword = ""
    return decoded_text

