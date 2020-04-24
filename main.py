import time
import random
from bs4 import BeautifulSoup
import sqlite3
import os
import requests

day = 1
last = 27


def pause():
    time_break = random.randint(1, 2)
    return time.sleep(time_break)


def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


if os.path.isfile('mabase.db'):
    os.remove('mabase.db')
print(" ..... En Chargement.....")
url = 'https://www.pronosoft.com/fr/resultats/football/france/ligue-1/calendrier/journee-'

db = sqlite3.connect('mabase.db')
cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
         id INTEGER PRIMARY KEY AUTOINCREMENT,
        date INTEGER,
        domicile TEXT,
        visiteur TEXT,
        score TEXT,
        scdom INTEGER,
        scvis INTEGER,
        somme INTEGER
    )
""")

while day < last + 1:

    response = requests.get(url + str(day))
    date = int(day)

    if response.ok:

        soup = BeautifulSoup(response.text, 'lxml')
        trs = soup.findAll('tr')
        # print (len(trs))
        for td in trs:
            tds = td.findAll('td')
            #   print(len(tds))
            domicile = td.find('td', {'class': 'home_l'})
            dom = domicile.text
            sco = td.find('td', {'class': 'score'})
            score = sco.text
            # print(score)
            visiteur = td.find('td', {'class': 'ext_l'})
            ext = visiteur.text
            scdom = int(score[1:2])
            scvis = int(score[3:4])
            som = scdom + scvis

            cursor.execute(
                """INSERT INTO users( id, date, domicile, visiteur, score,scdom,scvis,somme) VALUES(null,?,?,?,?,?,?, ?)""",
                (date, dom, ext, score, scdom, scvis, som))
            db.commit()  # enregistre la base
            cursor.execute("""SELECT id, date, domicile, visiteur,score,scdom,scvis,somme date FROM users""")

    day = day + 1
    pause()
print("Bravo !")
db.close()

#########################
teamdom = []
teamvis = []
team = []
dbteam = sqlite3.connect('mabase.db')
cur = dbteam.cursor()
req1 = "select domicile from users where date=1"
req2 = "select visiteur from users where date=1"

for row1 in cur.execute(req1):
    teamdom1 = row1[0];
    teamdom.append(teamdom1)

for row2 in cur.execute(req2):
    teamvis1 = row2[0];
    teamvis.append(teamvis1)

team = teamdom + teamvis
dbteam.close()
for equipe in team:

    histo = sqlite3.connect('mabase.db')

    histob = sqlite3.connect('mabase.db')

    cursor = histo.cursor()
    cursorb = histob.cursor()
    # equipe = "Monaco"
    # print (isbn2)

    # cursor.execute("SELECT id, isbn, name, price, date FROM users WHERE isbn = ? ORDER BY date DESC", isbn2)
    cursor.execute("SELECT *,date FROM users WHERE domicile = ? AND scdom=0 ORDER BY date DESC", [equipe])

    rows = cursor.fetchall()

    hh = ''

    for row in rows:
        # hh = ('{0} : {1} - {2} - {3} -{4}'.format(row[0], row[4], row[1], row[2], row[3]))
        hh += str(row[1]) + "---" + str(row[5]) + "  ---->  " + str(row[3]) + "\n"

    cursorb.execute("SELECT *,date FROM users WHERE visiteur = ? AND scvis=0 ORDER BY date DESC", [equipe])

    rowsb = cursorb.fetchall()

    hhb = ''

    for rowb in rowsb:
        hhb += str(rowb[1]) + "---" + str(rowb[6]) + "  ---->  " + str(rowb[2]) + "\n"

    histo.close()
    histob.close()
    lasty = int(last - 1)

    conn = sqlite3.connect('mabase.db')
    noms = []
    for row in conn.execute("SELECT domicile FROM users WHERE date >= ? AND scdom =0 ", [lasty]):
        nom = row[0];

        noms.append(nom)

    conn.close()

    conn = sqlite3.connect('mabase.db')
    nomsa = []
    for row in conn.execute("SELECT visiteur FROM users WHERE date >= ? AND scvis =0 ", [lasty]):
        noma = row[0];

        nomsa.append(noma)

    conn.close()

    xxx = common_elements(noms, nomsa)
    dupes = [x for n, x in enumerate(noms) if x in noms[:n]]
    dupesa = [x for n, x in enumerate(nomsa) if x in nomsa[:n]]

    lastyx = int(last - 1)

    connx = sqlite3.connect('mabase.db')
    nomsx = []
    for rowx in connx.execute("SELECT domicile FROM users WHERE date >= ? AND somme <= 1  ", [lastyx]):
        nomx = rowx[0];

        nomsx.append(nomx)

    connx.close()

    conny = sqlite3.connect('mabase.db')
    nomsy = []
    for rowy in conny.execute("SELECT visiteur FROM users WHERE date >= ? AND somme <= 1  ", [lastyx]):
        nomy = rowy[0];

        nomsy.append(nomy)

    conny.close()

    yyy = common_elements(nomsx, nomsy)
    dupesx = [x for n, x in enumerate(nomsx) if x in nomsx[:n]]
    dupesy = [x for n, x in enumerate(nomsy) if x in nomsy[:n]]

print("Pari sur l'equipe +0.5 but: " + str(xxx) + str(
    dupes) + str(dupesa))
print("Pari sur le match à +1.5 buts: " + str(
    yyy))
