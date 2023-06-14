def compress(text):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256

    compressed_text = []
    current_code = ""
    for char in text:
        current_code += char
        if current_code not in dictionary:
            compressed_text.append(dictionary[current_code[:-1]])
            dictionary[current_code] = next_code
            next_code += 1
            current_code = char

    compressed_text.append(dictionary[current_code])

    return compressed_text, dictionary


def decompress(compressed_text, dictionary):
    next_code = 256

    decompressed_text = ""
    current_code = compressed_text[0]
    decompressed_text += dictionary[current_code]
    for code in compressed_text[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = current_code + current_code[0]
        else:
            raise ValueError("Invalid compressed text")

        decompressed_text += entry

        dictionary[next_code] = current_code + entry[0]
        next_code += 1
        current_code = entry

    return decompressed_text


def compress_text(text):
    compressed_text, dictionary = compress(text)
    compressed_text = ''.join(chr(code) for code in compressed_text)
    return compressed_text, dictionary


def decompress_text(compressed_text):
    dictionary = {i: chr(i) for i in range(256)}
    compressed_text = [ord(char) for char in compressed_text]
    return decompress(compressed_text, dictionary)
