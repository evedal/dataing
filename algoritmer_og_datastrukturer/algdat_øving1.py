from datetime import datetime
import random
#kursEndringer = [-1,3,-9,2,2,-1,2,-1,-5,2,3,4,5,6,-1,2,2,-4] #1

for i in range(1,10):
    liste = [0]*(i*100)
    for j in range(i*100):      #lager liste med random tall, første med 100, neste 200 osv helt til 1000
        liste[i] = random.randint(-10,10)
    listlength = i*100
    fortjeneste = 0
    runder = 0;
    start = datetime.now() #Starter tidtakning
    while True:
        for k in range(listlength):              #1+2n  #Blar gjennom listen, starter på første innkjøpsmulighet helt til siste
            inntjent = 0                         #n     #Resetter hva den beste inntjeningen er
            for j in range(k, listlength):       #n+2n^2 #Sjekker alle utsellings-datoer
                inntjent += liste[j]             #n^2      #regner ut fortjeneste på gitt utsalgsdato
                if inntjent > fortjeneste:       #n^2   #Sjekker om det er en ny beste inntjening
                    fortjeneste = inntjent       #n^2   #Lagrer den nye beste inntjeningen
        runder += 1
        if (datetime.now()-start).total_seconds() > 1:
            break
    print("Antall:",i*100,"Tid:",(datetime.now()-start)/runder,"Runder:,",runder)

#5n^2 + 4n + 1
#n --> infinity, går uttrykket mot n^2
#øvre og nedre grense er like, derfor T(n) = Θ(n^2)


