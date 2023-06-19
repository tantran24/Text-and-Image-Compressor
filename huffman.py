class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


def Calculate_Codes(node, val='', codes={}):
    newVal = val + str(node.code)

    if node.left:
        codes = Calculate_Codes(node.left, newVal, codes)
    if node.right:
        codes = Calculate_Codes(node.right, newVal, codes)

    if not node.left and not node.right:
        codes[node.symbol] = newVal

    return codes


def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) is None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])

    string = ''.join([str(item) for item in encoding_output])
    return string


def Total_Gain(data, coding):
    before_compression = len(data) * 8
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])
    return before_compression, after_compression


def encoding_text(data):
    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()

    nodes = []
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)

        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    codes = Calculate_Codes(nodes[0])
    before_compression, after_compression = Total_Gain(data, codes)
    encoded_output = Output_Encoded(data, codes)

    return encoded_output, nodes[0], codes, before_compression, after_compression


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

    string = ''.join([str(item) for item in decoded_output])
    return string
