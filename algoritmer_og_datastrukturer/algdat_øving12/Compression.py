from struct import unpack, pack
from datetime import datetime
import time
import os
import heapq
from collections import defaultdict
from bitstring import BitArray, Bits

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
            print("")
            while c1 or c2:
                if not c1 == c2:
                    count += 1
                if c1:
                    c1_a.append(c1)
                if c2:
                    c2_a.append(c2)
                c1 = orig_file.read(1)
                c2 = comp_file.read(1)
            print("Fant", count, "ulikheter mellom original og utpakket fil")
            print("Original:", str(len(c1_a)) + "B", "Utpakket:", str(len(c2_a)) + "B")


class Node:
    def __init__(self,value,left=None,right=None,char=None,parent = None):
        self.left_branch = left
        self.right_branch = right
        self.parent = parent
        self.value = value
        self.char = char
    def __lt__(self, other):
        if self.value > other.value:
            return 1
        elif self.value == other.value:
            return 0
        else:
            return -1
    def __str__(self):
        out = str(self.char) if self.char else str(self.value)
        return out

class PriorityQue(object):
    def __init__(self, nodes=[]):
        self.heap = []
        self.entry_finder = dict()
        for node in nodes:
            entry = [node.value, node]
            self.add_node2(entry)
        self.REMOVED = '<remove_marker>'

    def add_node(self,node,priority=0):
        if node in self.entry_finder:
            self.remove_node(node)
        entry = [node.value,node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap,entry)

    #Add a node using already created entry, useful for initialization
    def add_node2(self,entry):
        if entry[-1] in self.entry_finder:
            self.remove_node(entry[-1])
        self.entry_finder[entry[-1]] = entry
        heapq.heappush(self.heap,entry)

    def remove_node(self,node):
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED


    def pop_node(self):
        while self.heap:
            node = heapq.heappop(self.heap)[-1]
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return node
        raise KeyError('pop from an empty priority queue')

class HuffmanTree:
    def __init__(self):
        self.nodes = []
    def add_node(self,node):
        pass
    def init_nodes(self,char_array):
        for char in char_array:
            self.nodes.append(Node(char[1],char=char[0]))

    def create_tree(self,char_array):
        self.init_nodes(char_array)
        pq = PriorityQue(self.nodes)
        node = None
        heigth = 0
        while True:
            try:
                rigth_branch = pq.pop_node()
                left_branch = pq.pop_node()
                value = rigth_branch.value + left_branch.value
                node = Node(left=left_branch,right=rigth_branch,value=value)
                left_branch.parent = node
                rigth_branch.parent = node
                pq.add_node(node)
                heigth += 1
            except KeyError:
                break
        return node

    def byte_len(self,int_type):
        length = 0
        while int_type:
            int_type >>= 1
            length += 1
        return length

    def give_char_values(self,for_encoding=False):
        value_pairs = {}
        for node in self.nodes:
            parent_len = 0
            while node.parent:
                parent_len += 1
                node = node.parent
        for node in self.nodes:

            byte_int = 0
            byte_postition = 0
            parent = node.parent
            temp_node = node
            while parent:
                if parent.right_branch == temp_node:
                    byte_int += 2**byte_postition
                byte_postition += 1
                temp_node = parent
                parent = parent.parent
            #Always add a 1 before start of bit_pattern
            byte_int += 2 ** byte_postition
            byte_rep = byte_int.to_bytes(2,"big",signed=False)
            length = self.byte_len(byte_int)
            single_byte1, single_byte2 = unpack('bb', byte_rep)
            value_pairs.update({node.char:[pack("b",single_byte1),pack("b",single_byte2)]})
        return value_pairs

class HuffmanCompression:
    def find_frequency(self,text):
        frequency = []
        for char in text:
            for row in frequency:
                if row[0] is char:
                    row[1] += 1
                    break
            else:
                frequency.append([char, 1])
        return frequency

    def prep_for_print(self,value_pairs, bits_array):
        output = [(10).to_bytes(1,"big",signed=False)] * 512
        for char, char_rep in value_pairs.items():
            char_pos = int.from_bytes(char,'big',signed=False)
            output[char_pos * 2] = char_rep[0]
            output[char_pos * 2 +1] = char_rep[1]
        missing = len(bits_array) % 8
        bits_array.append(Bits(bytes=b'\x00', length=8-missing))
        output.append(bits_array.bytes)
        return output

    def byte_len(self,int_type):
        length = 0
        while int_type:
            int_type >>= 1
            length += 1
        return length

    def encode(self,value_pair,byte_array):
        output_array = BitArray()
        for byte in byte_array:
            byte_value = value_pair.get(byte)
            byte_value = Bits(byte_value[0] + byte_value[1])[1:]
            byte_len = self.byte_len(byte_value)
            byte_value = byte_value[(-byte_len):]
            output_array.append(byte_value)
        return output_array

    def create_lookup_dict(self,byte_array):
        byte_array = byte_array[0:512]
        return_dict = {}
        count = 0
        for i in range(0,len(byte_array),2):
            key = Bits(byte_array[i]+byte_array[i+1])
            byte_len = self.byte_len(key)
            key = key[(-byte_len):]
            value = (count).to_bytes(1,"big")
            count += 1
            return_dict.update({key:value})
        return return_dict

    def decode(self,byte_array):
        lookup = self.create_lookup_dict(byte_array)
        byte_array = byte_array[512:]
        return_array = []
        bit_array = BitArray()
        for byte in byte_array:
            bit_array.append(byte)
        read = 0
        bit_length = 1
        while bit_length + read <= len(bit_array):
            bit_hashable = Bits(bit_array[read:read+bit_length])
            if bit_hashable in lookup:
                return_array.append(lookup.get(bit_hashable))
                read = bit_length + read
                bit_length = 1
            else:
                bit_length += 1


        return return_array


    def compress_file(self,filename):
        comp = Compression()
        char_array = comp.read_file_as_binary(filename)
        frequency = self.find_frequency(char_array)
        ht = HuffmanTree()
        ht.create_tree(frequency)
        value_pairs = ht.give_char_values()
        value_pairs_for_encoding = ht.give_char_values(for_encoding=True)
        bits_array = self.encode(value_pairs_for_encoding,char_array)
        printable = self.prep_for_print(value_pairs,bits_array)
        return comp.populate_file_with_binary("huff_"+filename,printable)

    def decode_file(self,filename,ferdig_filnavn):
        comp = Compression()
        byte_array = comp.read_file_as_binary(filename)
        comp_byte_array = self.decode(byte_array)
        return comp.populate_file_with_binary(ferdig_filnavn,comp_byte_array)



def compress(choice,filnavn):
    choice = int(choice)
    comp = Compression()
    if choice == 3:
        print("Fil som pakkes:",filnavn,"| Original størrelse:",str(os.path.getsize(filnavn))+"B | Lagres som: comp_"+filnavn)
        start = datetime.now()
        comp_filnavn = comp.lempel_ziv(filnavn)
        print("Lempel_ziv tok:",str((datetime.now()-start).seconds)+'s')
        print("Ny størrelse er:",str(os.path.getsize(comp_filnavn))+"B")
        huff_comp = HuffmanCompression()
        start = datetime.now()
        print("Fil som pakkes:",comp_filnavn,"| Original størrelse:",str(os.path.getsize(comp_filnavn))+"B | Lagres som: huff_"+comp_filnavn)
        comp2_filnavn = huff_comp.compress_file(comp_filnavn)
        print("Huffman tok:",str((datetime.now()-start).seconds)+'s')
        print("Ny størrelse er:",str(os.path.getsize(comp2_filnavn))+"B")
    elif choice == 1:
        print("Fil som pakkes:", filnavn, "| Original størrelse:",str(os.path.getsize(filnavn)) + "B | Lagres som: comp_" + filnavn)
        start = datetime.now()
        comp_filnavn = comp.lempel_ziv(filnavn)
        print("Lempel_ziv tok:", str((datetime.now() - start).seconds) + 's')
        print("Ny størrelse er:", str(os.path.getsize(comp_filnavn)) + "B")
    else:
        print("Fil som pakkes:", filnavn, "| Original størrelse:",str(os.path.getsize(filnavn)) + "B | Lagres som: huff_" + filnavn)
        huff_comp = HuffmanCompression()
        start = datetime.now()
        comp2_filnavn = huff_comp.compress_file(filnavn)
        print("Huffman tok:",str((datetime.now()-start).seconds)+'s')
        print("Ny størrelse er:",str(os.path.getsize(comp2_filnavn))+"B")


def extract(choice):
    comp = Compression()
    huff_comp = HuffmanCompression()
    choice = int(choice)
    filnavn = input("Skriv filnavn på komprimert fil:")

    print("----------------------------------------")
    if choice == 3:
        huff_filnavn = "huff_"+filnavn
        print("Fil som pakkes ut:",filnavn,"| Original størrelse",str(os.path.getsize(filnavn))+"B", "Lagres som: "+huff_filnavn)
        start = datetime.now()
        huff_comp.decode_file(filnavn,huff_filnavn)
        print("Utpakking tok:", str((datetime.now() - start).seconds) + 's')
        print("Ny størrelse er:", str(os.path.getsize(huff_filnavn)) + "B")
        print("----------------------------------------")
        lempel_filnavn = "lempel_"+huff_filnavn
        print("Fil som pakkes ut:",huff_filnavn,"| Original størrelse",str(os.path.getsize(huff_filnavn))+"B", "Lagres som: "+lempel_filnavn)
        start = datetime.now()
        comp.extract(huff_filnavn,lempel_filnavn)
        print("Utpakking tok:", str((datetime.now() - start).seconds) + 's')
        print("Ny størrelse er:", str(os.path.getsize(lempel_filnavn)) + "B")
        ferdig_fil = lempel_filnavn
    elif choice == 1:
        print("----------------------------------------")
        lempel_filnavn = "lempel_" + filnavn
        print("Fil som pakkes ut:", filnavn, "| Original størrelse", str(os.path.getsize(filnavn)) + "B","Lagres som: " + lempel_filnavn)
        start = datetime.now()
        comp.extract(filnavn, lempel_filnavn)
        print("Utpakking tok:", str((datetime.now() - start).seconds) + 's')
        print("Ny størrelse er:", str(os.path.getsize(lempel_filnavn)) + "B")
        ferdig_fil = lempel_filnavn
    else:
        huff_filnavn = "huff_"+filnavn
        print("Fil som pakkes ut:",filnavn,"| Original størrelse",str(os.path.getsize(filnavn))+"B", "Lagres som: "+huff_filnavn)
        start = datetime.now()
        huff_comp.decode_file(filnavn,huff_filnavn)
        print("Utpakking tok:", str((datetime.now() - start).seconds) + 's')
        print("Ny størrelse er:", str(os.path.getsize(huff_filnavn)) + "B")
        ferdig_fil = huff_filnavn

    return ferdig_fil

if __name__ == '__main__':
    choice = input("Ønsker du lempel, huffman, begge? Skriv henholdsvis 1,2,3: ")
    filnavn = input("Skriv fil for komprimering:")
    ferdig_fil = compress(choice,filnavn)
    ferdig_fil = extract(choice)
    comp = Compression()
    comp.check_differences(filnavn,ferdig_fil)
