class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


class Huffman:
    def __init__(self, data):
        self.data = data
        self.symbol_with_probs = self.calculate_probability(data)
        self.symbols = self.symbol_with_probs.keys()
        self.nodes = self.build_tree()
        self.codes = self.calculate_codes(self.nodes[0])
        self.before_compression, self.after_compression = self.calculate_total_gain()

    def calculate_probability(self, data):
        symbols = dict()
        for element in data:
            symbols[element] = symbols.get(element, 0) + 1
        return symbols

    def build_tree(self):
        nodes = []
        for symbol in self.symbols:
            nodes.append(Node(self.symbol_with_probs.get(symbol), symbol))

        while len(nodes) > 1:
            nodes = sorted(nodes, key=lambda x: x.prob)

            right = nodes[0]
            left = nodes[1]

            left.code = 0
            right.code = 1

            new_node = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

            nodes.remove(left)
            nodes.remove(right)
            nodes.append(new_node)

        return nodes

    def calculate_codes(self, node, val='', codes={}):
        new_val = val + str(node.code)

        if node.left:
            codes = self.calculate_codes(node.left, new_val, codes)
        if node.right:
            codes = self.calculate_codes(node.right, new_val, codes)

        if not node.left and not node.right:
            codes[node.symbol] = new_val

        return codes

    def calculate_total_gain(self):
        before_compression = len(self.data) * 8
        after_compression = 0

        for symbol in self.symbols:
            count = self.data.count(symbol)
            after_compression += count * len(self.codes[symbol])

        return before_compression, after_compression

    def encode_text(self):
        encoded_output = self.output_encoded(self.data, self.codes)
        return encoded_output, self.nodes[0], self.codes, self.before_compression, self.after_compression

    @staticmethod
    def output_encoded(data, coding):
        encoding_output = []
        for c in data:
            encoding_output.append(coding[c])

        return ''.join([str(item) for item in encoding_output])

    @staticmethod
    def decoding_text(encoded_data, huffman_tree):
        tree_head = huffman_tree
        decoded_output = []
        for x in encoded_data:
            if x == '1':
                huffman_tree = huffman_tree.right
            elif x == '0':
                huffman_tree = huffman_tree.left
            try:
                if huffman_tree.left.symbol is None and huffman_tree.right.symbol is None:
                    pass
            except AttributeError:
                decoded_output.append(huffman_tree.symbol)
                huffman_tree = tree_head

        return ''.join([str(item) for item in decoded_output])
