import itertools, argparse
from tqdm import tqdm
from pymongo import MongoClient

# interne Repräsentation der Karte

karte = ['Uk8Wg2Uq2Mu13p9Sd1Fz9Yr6Hg', '2h66#Q4sB7#D9CS2$45gT9#tX1', 'aWy3tCp1u7y6kEg4nBq6mDg7rV',
         '$1O@2Y&8P§1E&6O&95§8K$6Q$1',
         '§&I4#Hfy65&a9AGdo#O@oQI&1#', 'Oa11b3ZI2Ky9Sm6Po14i4Bk8Fa', '7kV2%E3nO5&O3rA7@W5vG3@y31',
         'iMo3qDq1pOp1yUq6u1b6nDh7xO',
         '§1T$1X@27#5F@1Y#2L§1X$69§6', '%§X5%HpcA7e5S5wy$7@gRbp#3#', 'Pd7Re9HI12e7Kq7Mj8Ew4Yt25e',
         '2oI6$V3jS2%I2o53&T9hP6&tH1']

dimensionen_karte = (len(karte[0]), len(karte))
moegliche_richtungen = {(1, 0): 'A', (1, 1): 'B', (0, 1): 'C', (-1, 1): 'D', (-1, 0): 'E', (-1, -1): 'F',(0, -1): 'H', (1, -1): 'I'}

#Verbindungsaufbau zur Datanbank

def connect_db(col):
    client = MongoClient('localhost', 27017)
    # Hier die Datenbank und die Collection einstellen
    db = client['woerterbuch']
    collection = db[col]
    return collection

    # Generierung der Teilabschnitte

def gehe_horizontal(spalte, zeile, schritte, richtung=1):
    '''
    Generiert ein Wort indem es vom Startpunkt aus horizontal die angegebene Anzahl Schritte in die
    vorgegebene Richtugn macht

    spalte = Spalte in der begonnen wird
    zeile = Zeile in der sich bewegt wird
    anzahl = Anzahl Zeichen, die zurückgegeben werden, inklusive dem Zeichen an der Startposition
    richtung:
        +1 : nach rechts
        -1 : nach links

    Return: Tupel aus (Zeichenkette der Länge schritte, Endposition_X, Endposition_Y)
    '''
    zeichen = ''
    for i in range(0, schritte):
        zeichen += karte[zeile][spalte]
        spalte += richtung
    return (zeichen, spalte - richtung, zeile)


def gehe_vertikal(spalte, zeile, schritte, richtung=1):
    '''
    Generiert ein Wort indem es vom Startpunkt aus vertikal die angegebene Anzahl Schritte in die
    vorgegebene Richtugn macht

    spalte = Spalte in der sich bewegt wird
    zeile = Zeile in der begonnen wird (inklusive)
    anzahl = Anzahl Zeichen, die zurückgegeben werden, inklusive dem Zeichen an der Startposition
    richtung:
        +1 : nach unten
        -1 : nach oben

    Return: Tupel aus (Zeichenkette der Länge schritte, Endposition_X, Endposition_Y)
    '''
    zeichen = ''
    for i in range(0, schritte):
        zeichen += karte[zeile][spalte]
        zeile += richtung
    return (zeichen, spalte, zeile - richtung)


def gehe_diagonal(spalte, zeile, schritte, richtung_X, richtung_Y):
    '''
    Generiert ein Wort indem es vom Startpunkt aus diagonal die angegebene Anzahl Schritte in die
    vorgegebene Richtugn macht

    spalte = Spalte in der begonnen wird (inklusive)
    zeile = Zeile in der begonnen wird (inklusive)
    anzahl = Anzahl Zeichen, die zurückgegeben werden, inklusive dem Zeichen an der Startposition
    richtung_X:
        +1 : nach rechts
        -1 : nach links
    richtung_Y:
        +1 : nach unten
        -1 : nach oben

    Return: Tupel aus (Zeichenkette der Länge schritte, Endposition_X, Endposition_Y)
    '''
    zeichen = ''
    for i in range(0, schritte):
        zeichen += karte[zeile][spalte]
        spalte += richtung_X
        zeile += richtung_Y
    return (zeichen, spalte - richtung_X, zeile - richtung_Y)

def richtungs_permutationen(anzahl_teilwege):
    '''
    Bildet alle möglichen Kombinationen von Richtungen für anzahl_teilwege Teilwege innerhalb des Passwortes

    anzahl_teilwege: Anzahl der Unterteilungen des Passwortes

    Richtungen:
    X-Achse
        +1 : nach rechts
         0 : keine Bewegung in X Richtung
        -1 : nach links
    Y-Achse:
        +1 : nach unten
         0 : keine Bewegung in X Richtung
        -1 : nach oben
    Definiert als Tupel (X,Y)
    1,0 horizontal nach rechts; 1,1 diagonal nach rechts unten, 0,1 vertikal nach unten,
    -1,1 diagonal nach links unten, -1,0 horizontal nach links, -1,-1 diagonal nach links oben
    0,-1 vertikal nach oben, 1,-1 diagonal nach rechts oben

    Return: Liste aller möglichen Kombinationen (Tupel von Tupeln)
    '''
    #moegliche_richtungen = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    alle_moeglichen_richtungswechsel = []
    for perm in itertools.product(moegliche_richtungen.keys(), repeat=anzahl_teilwege):
        if all([True if perm[i] != perm[i + 1] else False for i in range(0, anzahl_teilwege - 1)]):
            alle_moeglichen_richtungswechsel.append(perm)
    return alle_moeglichen_richtungswechsel


def bilde_teilwege(gesamtweg, teilwege, prev_teilweg=None, ergebnis=None):
    '''
    gesamtweg: Länge des Passworts
    teilwege: Anzahl der Teilwege (Teilweg: Mehrere Zeichen in eine einzige Richtung)

    Return: Liste von möglichen Kombinationen von Teilwegen unterschiedlicher Länge, die zusammen den Gesamtweg ergeben

    '''
    if prev_teilweg == None:
        prev_teilweg = ()
    if ergebnis == None:
        ergebnis = []
    if teilwege == 1:
        ergebnis.append(prev_teilweg + (gesamtweg,))
        return ergebnis
    if teilwege > 1:
        for i in range(1, gesamtweg - teilwege + 2):
            ergebnis = bilde_teilwege(gesamtweg - i, teilwege - 1, prev_teilweg + (i,), ergebnis)
    return ergebnis


def teste_grenzen(spalte, zeile, teilwege, richtungs_permutation):
    '''
    Überprüft ob ein vorgegebener Weg innerhalb der Grenzen der Karte liegt

    Return: True falls ja
            False sonst
    '''
    for i in range(len(teilwege)):
        spalte += (teilwege[i] - 1) * richtungs_permutation[i][0]
        zeile += (teilwege[i] - 1) * richtungs_permutation[i][1]
        if zeile < 0 or zeile > dimensionen_karte[1] - 1 or spalte < 0 or spalte > dimensionen_karte[0] - 1:
            return False
        if i < len(teilwege) - 1:
            spalte += richtungs_permutation[i + 1][0]
            zeile += richtungs_permutation[i + 1][1]
    return True

# Generierung eines kompletten Wortes

def generiere_wort(spalte, zeile, teilwege, richtungs_permutation):
    '''
    Generiert ein Wort

    spalte = Spalte in der begonnen wird (inklusive)
    zeile = Zeile in der begonnen wird (inklusive)
    teilwege: Tupel aus den Längen der Teilabschnitte des endgültigen Wortes
    richtungs_permutation: Tupel aus den Tupel der Richtungen der korrespondierenden Teilabschnitte

    Return: Das Wort, das dem angegebenen Pfad entspricht
    '''

    wort = ''
    for i in range(len(teilwege)):
        if richtungs_permutation[i][0]:
            if not richtungs_permutation[i][1]:
                wort_tpl = gehe_horizontal(spalte, zeile, teilwege[i], richtungs_permutation[i][0])
            else:
                wort_tpl = gehe_diagonal(spalte, zeile, teilwege[i], richtungs_permutation[i][0], richtungs_permutation[i][1])
        else:
            wort_tpl = gehe_vertikal(spalte, zeile, teilwege[i], richtungs_permutation[i][1])
        wort += wort_tpl[0]
        if i < len(teilwege) - 1:
            spalte = wort_tpl[1] + richtungs_permutation[i + 1][0]
            zeile = wort_tpl[2] + richtungs_permutation[i + 1][1]
    return wort

# Generierung eines Wörterbuches

def generiere_woerterbuch(maxLaenge,maxRichtungsWechsel, collection):
    '''
    Generiert ein Wörterbuch

    maxLaenge: Passwortlänge bis zu der das Wörterbuch erstellt wird
    maxRichtungsWechsel: Maximale Anzahl Teilabschnitte bis zu denen das Wörterbuch erstellt werden soll
    '''

    batch_Liste=[]
    id_Liste=[]
    for x in tqdm(range(0,dimensionen_karte[0])):
        for y in range(0,dimensionen_karte[1]):
            for i in range(1,maxLaenge+1):
                for j in range(1,maxRichtungsWechsel+1):
                    for k in bilde_teilwege(i,j):
                        for l in richtungs_permutationen(j):
                            if teste_grenzen(x,y,k,l):
                                wort_tmp=generiere_wort(x,y,k,l)
                                if (wort_tmp not in id_Liste) and (not (collection.find({"_id":wort_tmp},{'_id':1}).limit(1)).count()):
                                    path=[x,y]+[str(k[teilweg])+moegliche_richtungen[l[teilweg]] for teilweg in range(0,len(k))]
                                    batch_Liste.append({"_id":wort_tmp, "path":path})
                                    id_Liste.append(wort_tmp)
                                if len(id_Liste)>700:
                                    collection.insert_many(batch_Liste)
                                    batch_Liste=[]
                                    id_Liste=[]


# Main Funktion, die beim Start über die Kommandozeile ausgeführt wird

if __name__=='__main__':

    # Parser für die Argumente
    parser = argparse.ArgumentParser()
    parser.add_argument("maxLaenge", action="store", type=int, help="Maximale Passwortlaenge")
    parser.add_argument("maxRichtungswechsel", type=int, help="Maximale Anzahl an Richtungswechseln")
    parser.add_argument("collection1", action="store", type=str, default="woerter_Neu", help="Namen der Collection,in die das Wörterbuch gespeichert werrden soll")
    args = parser.parse_args()

    # Verbindung zur Datenbak aufbauen
    collection=connect_db(args.collection1)



    # Da in der internen Repräsentation der Pfade icht mit der Anzahl an Richtungswechseln
    # sondern mit der sich darau ergebenden Anzahl an Teilabschnitten innerhalb des Passworts
    # gearbeitet wird, muss der Aufrauf des Generator mit maxRichtungswechsel+1 geschehen
    generiere_woerterbuch(args.maxLaenge, (args.maxRichtungswechsel+1),collection)