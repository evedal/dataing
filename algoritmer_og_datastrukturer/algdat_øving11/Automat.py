class Automat:
    def __init__(self, inputalfabet, aksept_tilstander, neste_tilstand_tabell):
        self.inputalfabet = inputalfabet
        self.aksept_tilstander = aksept_tilstander
        self.neste_tilstand_tabell = neste_tilstand_tabell

    def sjekkInput(self, _input):
        tilstand_nå = 0
        for char in _input:
            if char in self.inputalfabet:
                tilstand_nå = self.neste_tilstand_tabell[tilstand_nå][self.inputalfabet.index(char)]
            else:
                raise ValueError("Input er ikke en del av automaten sitt alfabet")
        return tilstand_nå in self.aksept_tilstander

if __name__ == '__main__':

    alfabet = [0,1]
    aksept = [2]
    neste_tilstand = [[1,3],[1,2],[2,3],[3,3]]
    automat = Automat(alfabet, aksept, neste_tilstand)

    print("Input = 010 -- >", automat.sjekkInput([0,1,0]))
    print("Input = 111 -- >", automat.sjekkInput([1,1,1]))
    print("Input = 010110 -- >", automat.sjekkInput([0,1,0,1,1,0]))
    print("Input = 001000 -- >", automat.sjekkInput([0,0,1,0,0,0]))

    print("\n-------------\n")

    alfabet = ['a','b']
    aksept = [3]
    neste_tilstand = [[1,2],[4,3],[3,4],[3,3],[4,4]]
    automat = Automat(alfabet, aksept, neste_tilstand)

    print("Input = abbb -- >", automat.sjekkInput(['a', 'b', 'b','b']))
    print("Input = aaab -- >", automat.sjekkInput(['a', 'a', 'a','b']))
    print("Input = babab -- >", automat.sjekkInput(['b', 'a', 'b','a','b']))
