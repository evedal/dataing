from struct import unpack, pack
from datetime import datetime
import time
import os
from collections import defaultdict

class Compression:

    def __init__(self,MIN_MATCH_LEN = 6, REVERSE_BYTES=2):
        self.REVERSE_BYTES =  (2**(REVERSE_BYTES*8 -1)) -1
        self.MIN_MATCH_LEN  = MIN_MATCH_LEN

    def read_file_as_binary(self,filename):
        with open(filename, 'rb') as file:
            bin_array = []
            c = file.read(1)
            while c:
                bin_array.append(c)
                c = file.read(1)
            return bin_array

    def populate_file_with_binary(self,comp_filename, char_array):
        with open(comp_filename, 'wb') as file:
            for char in char_array:
                file.write(char)
            return comp_filename

    def lempel_ziv(self, filename):
        chars = self.read_file_as_binary(filename)
        comp_chars = []
        numb_of_uncompressed = 0
        saved_index = 0
        count = 0
        while count < len(chars):
            end = count-self.REVERSE_BYTES if count-self.REVERSE_BYTES >= 0 else -1

            #Did not utilize named tuple because of perfomance
            #Best_match = (Length of match, distance backwards)
            best_match = (0,0)
            #Simple text search algorithm for increased performance. (Runtime cut by two thirds!!) )
            try:
                word_to_match = {}
                for i, x in enumerate(range(count, count + self.MIN_MATCH_LEN)):
                    if chars[x] not in word_to_match:
                        word_to_match.update({chars[x]:i})

            except IndexError:
                for i, x in enumerate(range(count)):
                    if chars[x] not in word_to_match:
                        word_to_match.update({chars[x]:i})

            inner_count = count-self.MIN_MATCH_LEN
            while inner_count > end:
                match_length = 0
                match_char = chars[inner_count]

                #text search algorithm
                if match_char not in word_to_match:
                    inner_count -= self.MIN_MATCH_LEN-1
                    continue
                inner_count -= word_to_match.get(match_char)
                if inner_count <= end:
                    inner_count = end + 1
                match_char = chars[inner_count]

                current_char = chars[count]
                while current_char == match_char:
                    match_length += 1
                    try:
                        current_char = chars[count+match_length]
                        match_char = chars[inner_count+match_length]
                    except IndexError:
                        #Silenced exeption handling when end of file
                        break

                if match_length > best_match[0]:
                    best_match = (match_length,count-inner_count)
                inner_count -= 1


            if best_match[0] >= self.MIN_MATCH_LEN:
                # Caused an issue, quickfix.
                if best_match[0] > best_match[1]:
                    best_match = (best_match[1],best_match[1])

                #Updates number of uncompressed bytes
                if numb_of_uncompressed > 0:
                    comp_chars[saved_index] = (-numb_of_uncompressed).to_bytes(1,"big",signed=True)#fordi bin(-1) er lagt inn på plassen før første bokstav som komprimeres
                    numb_of_uncompressed = 0
                #Creates bytes from ints, then splits 1 byte into two.
                len_bytes = best_match[0].to_bytes(2,"big",signed=True)
                dist_bytes = (best_match[1]).to_bytes(2, "big", signed=True)
                len1, len2 = unpack('bb', len_bytes)
                dist1, dist2 = unpack('bb', dist_bytes)
                comp_chars.extend([pack("b",len1),pack("b",len2),pack("b",dist1),pack("b",dist2)])
                count += best_match[0]

            #Adds uncompressed char to array, increments number of uncompressed.
            #Saves the index to use when finished adding all uncompressed chars
            else:
                if numb_of_uncompressed is 0:
                    comp_chars.append(None)
                    saved_index = len(comp_chars)-1
                comp_chars.append(chars[count])
                numb_of_uncompressed += 1
                count += 1

                if numb_of_uncompressed >= 127:
                    comp_chars[saved_index] = (-numb_of_uncompressed).to_bytes(1, "big", signed=True)
                    numb_of_uncompressed = 0

        #If there are uncompressed chars not updated when finished reading, update at saved index.
        if numb_of_uncompressed is not 0:
            comp_chars[saved_index] = (-numb_of_uncompressed).to_bytes(1,"big",signed=True)

        return self.populate_file_with_binary("comp_"+filename,comp_chars)

    def extract(self, from_filnavn, to_filnavn):
        byte_array = self.read_file_as_binary(from_filnavn)
        char_array = []
        iter_bytes = iter(enumerate(byte_array))
        for i, byte in iter_bytes:
            val1 = int.from_bytes(byte, byteorder='big', signed=True)
            if val1 < 0:
                val1 *= -1
                for j in range(val1):
                    if len(byte_array) < (i + j + 2):
                        break
                    char_array.append(byte_array[i + j + 1])
                try:
                    [iter_bytes.__next__() for x in range(val1)]
                except:
                    #End of file
                    break

            else:
                try:
                    byte_combination_len = (byte_array[i] + byte_array[i + 1])
                    byte_combination_back = (byte_array[i + 2] + byte_array[i + 3])
                except IndexError:
                    #End of file
                    break

                match_length = int.from_bytes(byte_combination_len, byteorder='big', signed=True)
                backwards = int.from_bytes(byte_combination_back, byteorder='big', signed=True)
                if backwards < 0:
                    backwards = backwards * -1
                start_pos = len(char_array) - backwards
                for c in char_array[start_pos: start_pos + match_length]:
                    char_array.append(c)
                try:
                    [iter_bytes.__next__() for x in [0, 1, 2]]
                except:
                    #End of file
                    break
        return self.populate_file_with_binary(to_filnavn, char_array)

    def check_differences(self,original, extracted):
        with open(original, "rb") as orig_file, open(extracted, "rb") as comp_file:
            c1 = orig_file.read(1)
            c2 = comp_file.read(1)
            c1_a = []
            c2_a = []
            count = 0
            print("Finner ulikheter")
            while c1 or c2:
                if not c1 == c2:
                    count += 1
                    print(c1, c2)
                if c1:
                    c1_a.append(c1)
                if c2:
                    c2_a.append(c2)
                c1 = orig_file.read(1)
                c2 = comp_file.read(1)
            print(c1_a)
            print(c2_a)
            print("Fant", count, "ulikheter mellom original og utpakket fil")
            print("Original:", str(len(c1_a)) + "B", "Utpakket:", str(len(c2_a)) + "B")


def compress():
    comp = Compression()
    filnavn = input("Skriv fil for komprimering:")
    print("Fil som pakkes:",filnavn,"| Original størrelse:",str(os.path.getsize(filnavn))+"B | Lagres som: comp_"+filnavn)
    start = datetime.now()
    comp_filnavn = comp.lempel_ziv(filnavn)
    print("Komprimering tok:",str((datetime.now()-start).seconds)+'s')
    print("Ny størrelse er:",str(os.path.getsize(comp_filnavn))+"B")

def extract():
    comp = Compression()
    print("----------------------------------------")
    filnavn = input("Skriv navn til komprimert fil:")
    ferdig_filnavn = "ferdig_"+filnavn
    print("Fil som pakkes ut:",filnavn,"| Original størrelse",str(os.path.getsize(filnavn))+"B", "Lagres som: "+ferdig_filnavn)
    start = datetime.now()
    comp.extract(filnavn,ferdig_filnavn)
    print("Utpakking tok:", str((datetime.now() - start).seconds) + 's')
    print("Ny størrelse er:", str(os.path.getsize(ferdig_filnavn)) + "B")
    print("----------------------------------------")
    comp.check_differences(filnavn.replace("comp_",""),ferdig_filnavn)

if __name__ == '__main__':
    compress()
    extract()