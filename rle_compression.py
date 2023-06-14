def rle_compress(text):
    compressed_text = ""
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            compressed_text += str(count) + text[i - 1]
            count = 1
    compressed_text += str(count) + text[-1]
    return compressed_text


def compress(text):
    compressed_text = ""
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1
        else:
            compressed_text += str(count) + text[i - 1]
            count = 1
    compressed_text += str(count) + text[-1]
    return compressed_text


def decompress(compressed_text):
    decompressed_text = ""
    i = 0
    while i < len(compressed_text):
        count = int(compressed_text[i])
        char = compressed_text[i + 1]
        decompressed_text += char * count
        i += 2
    return decompressed_text
