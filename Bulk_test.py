from pymongo import MongoClient
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("datei")
args=parser.parse_args()


client = MongoClient()
db = client.woerterbuch
collection = db.woerter3

pw_List = [wort.split()[0].strip() for wort in open('./'+args.datei).readlines()]
gefunden=[]
nicht_gefunden=[]

for wort in pw_List:
    if collection.find_one({'_id':wort}):
        gefunden.append(wort)
    else:
        nicht_gefunden.append(wort)

print('Gefundene Passwoerter:', len(gefunden))
print('Nicht gefundene Passwoerter:', len(nicht_gefunden))