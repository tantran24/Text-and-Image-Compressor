import os

class LZ77_TEXT:
    def __init__(self) -> None:
        pass
    def get_encoding_table(self, compressed_text):
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


    def compress(self, text):
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
        return compressed_text, self.get_encoding_table(compressed_text)


    def decompress(self, compressed_text):
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


import re
import numpy as np
from PIL import Image


class LZ77_IMG:
    def __init__(self, path):
        self.path = path
        self.original_file_size = os.path.getsize(path)
        self.data = None

    def longest_common_substring(self, s1, s2):
        maxLongest = 0
        offset = 0
        for i in range(0, len(s1)):
            longest = 0
            if ((i == len(s1) - len(s2) - 2)):
                break
            for j in range(0, len(s2)):
                if (i+j < len(s1)):
                    if s1[i+j] == s2[j]:
                        longest = longest + 1
                        if (maxLongest < longest):
                            maxLongest = longest
                            offset = i
                    else:
                        break
                else:
                    break
        return maxLongest, offset

    def encode_lz77(self, text, searchWindowSize, previewWindowSize):
        encodedNumbers = []
        encodedSizes = []
        encodedLetters = []
        i = 0
        while i < len(text):
            if i < previewWindowSize:
                encodedNumbers.append(0)
                encodedSizes.append(0)
                encodedLetters.append(text[i])
                i = i + 1
            else:
                previewString = text[i:i+previewWindowSize]
                searchWindowOffset = 0
                if (i < searchWindowSize):
                    searchWindowOffset = i
                else:
                    searchWindowOffset = searchWindowSize
                searchString = text[i - searchWindowOffset:i]
                result = self.longest_common_substring(searchString + previewString, previewString) # searchString + prevString, prevString
                nextLetter = ''
                if (result[0] == len(previewString)):
                    if (i + result[0] == len(text)):
                        nextLetter = ''
                    else:
                        nextLetter = text[i+previewWindowSize]
                else:
                    nextLetter = previewString[result[0]]
                if (result[0] == 0):
                    encodedNumbers.append(0)
                    encodedSizes.append(0)
                    encodedLetters.append(nextLetter)
                else:
                    encodedNumbers.append(searchWindowOffset - result[1])
                    encodedSizes.append(result[0])
                    encodedLetters.append(nextLetter)
                i = i + result[0] + 1
        return encodedNumbers, encodedSizes, encodedLetters

    def decode_lz77(self, encodedNumbers, encodedSizes, encodedLetters):
        i = 0
        decodedString = []
        while i < len(encodedNumbers):
            if (encodedNumbers[i] == 0):
                decodedString.append(encodedLetters[i])
            else:
                currentSize = len(decodedString)
                for j in range(0, encodedSizes[i]):
                    decodedString.append(decodedString[currentSize-encodedNumbers[i]+j])
                decodedString.append(encodedLetters[i])
            i = i+1
        return decodedString



    def compress(self, searchWindowSize=6, previewWindowSize=7):
        my_string = np.asarray(Image.open(self.path),np.uint8)
        stringToEncode = str(my_string.tolist())
        self.shape = my_string.shape
        self.string = my_string
        [encodedNumbers, encodedSizes, encodedLetters] = self.encode_lz77(stringToEncode, searchWindowSize, previewWindowSize)
        data =[encodedNumbers, encodedSizes, encodedLetters]
        print(data)
        print("Compressed file generated as compressed.txt")
        filesplit = str(os.path.basename(self.path)).split('.')
        filename = filesplit[0] + '_LZ77Compressed.txt'
        savingDirectory = os.path.join(os.getcwd(),'CompressedFiles')

        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        with open(os.path.join(savingDirectory,filename),'w+') as file:
            file.write(str(data))

        self.compressed_file_size = os.path.getsize(os.path.join(savingDirectory,filename))
        
    def decompress(self):
        encodedNumbers, encodedSizes, encodedLetters = self.data
        decodedString = self.decode_lz77(encodedNumbers, encodedSizes, encodedLetters)
        uncompressed_string ="".join(decodedString)

        temp = re.findall(r'\d+', uncompressed_string)
        res = list(map(int, temp))
        res = np.array(res)
        res = res.astype(np.uint8)
        res = np.reshape(res, self.shape)

        image = Image.fromarray(res)
        image.save('_LZ77Decompressed.jpg')
        self.saveImage(image)
        if self.string.all() == res.all():
            print("Success")


    def saveImage(self, image):
        print("Saving Decompressed File...")
        filesplit = str(os.path.basename(self.path)).split('_LZ77Compressed.txt')
        filename = filesplit[0] + "_LZ77Decompressed.jpg"
        savingDirectory = os.path.join(os.getcwd(),'DecompressedFiles')
        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)

        image.save(os.path.join(savingDirectory,filename))


da = [[1,2,3],[1,1,1],[5,5,6]]
print(str(da))
with open('test.txt','w+') as file:
    file.write(str(da))