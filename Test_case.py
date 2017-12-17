import random
import Woerterbuch_generator as wb

dimensionen_karte=(26,12)
moegliche_richtungen = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
datei = open('./PW_Test_Liste.txt', 'w')
cntr=0
while cntr<1000:
    x=random.randint(0,25)
    y=random.randint(0,11)

    laenge=random.randint(8,11)
    anzahl_teilwege=4

    l1=random.randint(1,laenge-anzahl_teilwege+1)
    l2=random.randint(1,laenge-l1-anzahl_teilwege+2)
    l3=random.randint(1,laenge-l1-l2-anzahl_teilwege+3)
    l4=random.randint(1,laenge-l1-l2-l3)

    teilwege=(l1,l2,l3,l4)

    r1=random.choice(moegliche_richtungen)
    r2=random.choice(moegliche_richtungen)
    while r2==r1:
        r2 = random.choice(moegliche_richtungen)
    r3=random.choice(moegliche_richtungen)
    while r3==r2:
        r3 = random.choice(moegliche_richtungen)
    r4=random.choice(moegliche_richtungen)
    while r4==r3:
        r4 = random.choice(moegliche_richtungen)
    richtungen=(r1,r2,r3,r4)

    pfad=[x,y,teilwege,richtungen]

    if wb.teste_grenzen(x,y,teilwege,richtungen):
        wort=wb.generiere_wort(x,y,teilwege,richtungen)
        datei.write(wort+' : '+str(pfad)+'\n')
        cntr+=1