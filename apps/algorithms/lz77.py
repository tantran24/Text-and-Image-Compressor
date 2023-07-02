import os
import re
import numpy as np
from PIL import Image


class LZ77:
    def __init__(self, path=None, searchWindowSize=6, previewWindowSize=7):
        self.path = path
        # if path != None:
        #     self.original_file_size = os.path.getsize(path)
        self.data = None
        self.searchWindowSize = searchWindowSize
        self.previewWindowSize = previewWindowSize

    def longest_common_substring(self, s1, s2):
        maxLongest = 0
        offset = 0
        for i in range(0, len(s1)): #abab    ab
            longest = 0
            if ((i == len(s1) - len(s2) - 0)):
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

    def encode_lz77(self, text):
        encodedNumbers = []
        encodedSizes = []
        encodedLetters = []
        encodeStr = ""
        i = 0
        while i < len(text):
            if i < self.previewWindowSize:
                encodedNumbers.append(0)
                encodedSizes.append(0)
                encodedLetters.append(text[i])
                encodeStr += f'0,0,{text[i]},'
                i = i + 1
            else:
                previewString = text[i:i+self.previewWindowSize]
                searchWindowOffset = 0
                if (i < self.searchWindowSize):
                    searchWindowOffset = i
                else:
                    searchWindowOffset = self.searchWindowSize
                searchString = text[i - searchWindowOffset:i]
                result = self.longest_common_substring(searchString + previewString, previewString) # searchString + prevString, prevString
                nextLetter = ''
                if (result[0] == len(previewString)):
                    if (i + result[0] == len(text)):
                        nextLetter = ''
                    else:
                        nextLetter = text[i+self.previewWindowSize]
                else:
                    nextLetter = previewString[result[0]]
                if (result[0] == 0):
                    encodedNumbers.append(0)
                    encodedSizes.append(0)
                    encodedLetters.append(nextLetter)
                    encodeStr += f'0,0,{nextLetter},'
                else:
                    encodedNumbers.append(searchWindowOffset - result[1])
                    encodedSizes.append(result[0])
                    encodedLetters.append(nextLetter)
                    encodeStr += f'{searchWindowOffset - result[1]},{result[0]},{nextLetter},'
                i = i + result[0] + 1
        # encodeStr = encodeStr[:-1]
        # if "," == encodeStr[-1]:
        #     encodeStr = encodeStr[:-1]
        return encodeStr

    def decode_lz77(self, encodeStr):
        i = 0
        list_data = encodeStr.split(',')
        decodedString = ""
        list_data = list_data[:-1]
        while i < len(list_data)/3:
            if (int(list_data[i*3 + 0]) == 0):
                decodedString += (list_data[i*3 + 2])
            else:
                currentSize = len(decodedString)
                for j in range(0, int(list_data[i*3 + 1])):
                    decodedString += (decodedString[currentSize-int(list_data[i*3 + 0])+j])
                decodedString += (list_data[i*3 + 2])
            i = i+1
        return decodedString



    def compress(self):
        my_string = np.asarray(Image.open(self.path),np.uint8)
        stringToEncode = str(my_string.tolist())
        self.shape = my_string.shape
        self.string = my_string
        compressed_data = self.encode_lz77(stringToEncode)
        print("Compressed file generated as compressed.txt")
        filesplit = str(os.path.basename(self.path)).split('.')
        filename = filesplit[0] + '_LZ77Compressed.txt'
        savingDirectory = os.path.join(os.getcwd(),'CompressedFiles')

        if not os.path.isdir(savingDirectory):
            os.makedirs(savingDirectory)
        with open(os.path.join(savingDirectory,filename),'w+') as file:
            file.write(str(compressed_data))

        self.compressed_file_size = os.path.getsize(os.path.join(savingDirectory,filename))
        
    def decompress(self):
        with open(self.path,"r") as file:
            data_comp = file.read()

        decodedString = self.decode_lz77(data_comp)
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


# cp = LZ77(searchWindowSize=6, previewWindowSize=3)
# a = cp.encode_lz77("ababcbababaa")
# print(a)



# # print(cp.encode_lz77("ababc"))
# # print(cp.longest_common_substring("abab", "ab"))
# print(cp.decode_lz77(a))

