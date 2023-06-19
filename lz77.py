def get_encoding_table(compressed_text):
    encoding_table = {}
    index = 0
    code = 0
    while index < len(compressed_text):
        if compressed_text[index] == "(":
            end_index = compressed_text.find(")", index)
            substring = compressed_text[index + 1: end_index]
            parts = substring.split(",")
            if len(parts) == 3:
                offset, length, next_char = int(parts[0]), int(parts[1]), parts[2]
                if offset != 0:
                    encoding_table[code] = encoding_table[code - offset] + next_char
                else:
                    encoding_table[code] = next_char
                code += 1
            index = end_index + 1
        else:
            index += 1
    return encoding_table


def compress(text):
    compressed_text = ""
    pos = 0
    while pos < len(text):
        length = 0
        offset = 0
        for i in range(1, min(pos + 1, len(text) - pos)):
            if text[pos - i] == text[pos] and text[pos - i: pos] == text[pos: pos + i]:
                length = i
                offset = i
        if length > 0:
            compressed_text += f"({offset},{length},{text[pos + length]})"
        else:
            compressed_text += f"(0,0,{text[pos]})"
        pos += length + 1
    return compressed_text, get_encoding_table(compressed_text)


def decompress(compressed_text):
    decompressed_text = ""
    pos = 0
    while pos < len(compressed_text):
        if compressed_text[pos] == "(":
            end_index = compressed_text.find(")", pos)
            substring = compressed_text[pos + 1: end_index]
            parts = substring.split(",")
            if len(parts) == 3:
                offset, length, next_char = int(parts[0]), int(parts[1]), parts[2]
                if offset != 0:
                    start_index = len(decompressed_text) - offset
                    for i in range(length):
                        decompressed_text += decompressed_text[start_index + i]
                decompressed_text += next_char
            pos = end_index + 1
        else:
            decompressed_text += compressed_text[pos]
            pos += 1
    return decompressed_text
