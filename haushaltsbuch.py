# Haushaltsbuchsoftware
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import der verwendeten Libarys.
from numpy import number
import pandas as pd # Zum erstellen der Dataframes und dem einfacheren einlesen der CSV
import matplotlib.pyplot as plt # Zur erstellung und Ausgabe der Grafiken
import time # Damit sleep verwendet werden kann
from datetime import datetime # Für das Datum
import os # Zur Prüfung, ob Output.csv im Verzeichnis des Programms vorhanden ist
from sklearn.linear_model import LinearRegression # Damit eine automatische Vorhersage erstellt werden kann

# Output Pfad in dem die Datei erstellt werden soll / gesucht werden soll.
out_path = os.path.join(os.path.dirname(__file__), 'output.csv')

# Datum vom jeweiligen Tag wird in der Variable gespeichert, damit es hinterher in der Output.csv mit eingetragen werden kann.
current_date = datetime.now()

# Kategorie Textdokumenten Pfad / Main Verzeichnis
category_path = os.path.join(os.path.dirname(__file__), 'kategorien.txt')

# Datumsformatierung
corrected_date = current_date.strftime('%d.%m.%Y')

# Kategorien Liste
category_list = set()

# Klasse für Saldo
class Saldo:

    # Übernahme der Startbetrags
    def __init__(self, start, current):
        self.start = start
        self.current = current

    # Funktion zur suche des Anfangsbetrags
    def anfangsbetrag(self):
        
        # Ist die Output.csv Datei vorhaben, werden die Werte aus dieser ausgelesen.
        if os.path.isfile(out_path):
            df = pd.read_csv(out_path, error_bad_lines=False)
            print(df.iloc[-5:])
            self.start = float(df['Saldo'].iloc[-1])
            print(f'Dein Saldo betraegt: {self.start:.2f} €'.replace('.', ','))
            self.current = self.start
            time.sleep(5)
        
        # Ist die Output.csv Datei nicht vorhanden, wird diese erstellt und mit den Werten gespeichert.
        if not os.path.isfile(out_path):
            self.start = float(
                input('Bitte gebe den Startbetrag ein: ').replace(',', '.'))
            with open(out_path, 'w') as file:
                file.write(f'Art,Betrag,Datum,Saldo,Kategorie\nStartbetrag,{self.start:.2f},{corrected_date},{self.start}')
            print(f'Dein Saldo betraegt: {self.start:.2f} €'.replace('.', ','))
            self.current = self.start
            time.sleep(5)

    # Funktion zum eintragen einer Einnahme.
    def einnahme(self, betrag):
        
        if os.path.isfile(category_path):
            with open(category_path) as file:
                for line in file:
                    stripped = line.strip()
                    category_list.add(stripped)
        
        # Oeffnet die Output.csv im Erweiterungsmodus und trägt die Einnahme ein, sowie den neu errechneten Saldo.
        with open(out_path, 'a') as file:
            einnahme_betrag = self.current + betrag
            if len(category_list) == 0:
                file.write(f'\nEinnahme,{betrag:.2f},{corrected_date},{einnahme_betrag:.2f}')
            else:
                corrected_list = []
                for element in sorted(category_list):
                    if element in corrected_list:
                        pass
                    corrected_list.append(element)
                ausgabe_liste = []
                auswahl_ziffer = [(i + 1) for i in range(len(corrected_list))]
                index_nummer = 0
                for element in corrected_list:
                    if element in ausgabe_liste:
                        pass
                    ausgabe_liste.append(f'{auswahl_ziffer[index_nummer]}: {element}')
                    index_nummer += 1
                print(ausgabe_liste)
                time.sleep(3)
                kategorie_wahl = input(f'Bitte wähle die Kategorie aus (1 - {len(category_list)}): ')
                auswahl = int(kategorie_wahl) - 1
                kategorie = corrected_list[auswahl]
                file.write(f'\nEinnahme,{betrag:.2f},{corrected_date},{einnahme_betrag:.2f},{kategorie}')
        df = pd.read_csv(out_path, error_bad_lines=False)
        saldo_new = df['Saldo'].iloc[-1]
        print(f'Dein neuer Saldo beträgt {saldo_new:.2f}€'.replace('.', ','))
        self.current = saldo_new
        time.sleep(5)
           
    # Funktion zum eintragen einer Ausgabe.    
    def ausgabe(self, betrag2):
        
        if os.path.isfile(category_path):
            with open(category_path) as file:
                for line in file:
                    stripped = line.strip()
                    category_list.add(stripped)
        
        # Öffnet die Output.csv im Erweiterungsmodus und trägt die Einnahme ein, sowie den neu errechneten Saldo.
        with open(out_path, 'a') as file:
            ausgabe_betrag = self.current - betrag2
            
            # Abfrage ob ein Negatives Saldo erreicht werden wuerde.
            if ausgabe_betrag > 0:
                if len(category_list) == 0:
                    file.write(f'\nAusgabe,{betrag2:.2f},{corrected_date},{ausgabe_betrag:.2f}')
                else:
                    corrected_list = []
                    for element in sorted(category_list):
                        if element in corrected_list:
                            pass
                        corrected_list.append(element)
                    ausgabe_liste = []
                    auswahl_ziffer = [(i + 1) for i in range(len(corrected_list))]
                    index_nummer = 0
                    for element in corrected_list:
                        if element in ausgabe_liste:
                            pass
                        ausgabe_liste.append(f'{auswahl_ziffer[index_nummer]}: {element}')
                        index_nummer += 1
                    print(ausgabe_liste)
                    time.sleep(3)
                    kategorie_wahl = input(f'Bitte wähle die Kategorie aus (1 - {len(category_list)}): ')
                    auswahl = int(kategorie_wahl) - 1
                    kategorie = corrected_list[auswahl]
                    file.write(f'\nAusgabe,{betrag2:.2f},{corrected_date},{ausgabe_betrag:.2f},{kategorie}')
            else:
                print(f'Dein Restguthaben für diesen Monat Beträgt: {self.current:.2f}\nDu hast versucht {betrag2:.2f} auszugeben, was ein Negatives Saldo zur Folge hätte.'.replace('.', ',', 2))
        df = pd.read_csv(out_path, error_bad_lines=False)
        saldo_new = df['Saldo'].iloc[-1]
        print(f'Dein neuer Saldo beträgt {saldo_new:.2f}€'.replace('.', ','))
        self.current = saldo_new
        time.sleep(5)
    
    # Ausgabe aller Buchungen als Liste.    
    def liste(self):
        df = pd.read_csv(out_path)
        print(df)
        time.sleep(5)
    
    # Ausgabe aller vorhanden Buchungen in einer Grafik.    
    def grafik(self):
        
        # Output.csv wird eingelesen.
        df = pd.read_csv(out_path)
        
        # Datum wird in die XS Liste geschrieben, Saldo in die YS Liste.
        xs = [x for x in df['Datum']]
        ys = [y for y in df['Saldo']]
        
        # Grafik wird erstellt und ausgegeben.
        plt.plot(xs, ys, label='Saldoänderung')
        plt.xlabel('Saldi')
        plt.ylabel('Datum')
        plt.legend()
        plt.show()
    
    #Funktion zum erstellen der Kategorien       
    def kategorien(self):
        if os.path.isfile(category_path):
            with open(category_path, 'r+') as file:
                new_category = input('Möchtest du weitere Kategorien hinzufügen?\nJa oder Nein: ')
                if new_category.lower() == 'ja':
                    while True:
                        cat = input('Kategorie eingeben, stop umd die Eingabe zu beenden: ')
                        if cat.lower() == 'stop':
                            print('Eingabe wird beendet!')
                            time.sleep(2)
                            return False
                        else:
                            file.write(f'{cat}\n')
                            
        if not os.path.isfile(category_path):
            print('Es wurden keine Kategorien gefunden!')
            print('Bitte gebe deine Kategorien ein.')
            time.sleep(3)
            with open(category_path, 'w+') as file:
                while True:
                    cat = input('Bitte gebe deine Kategorien ein, oder schreibe stop um die Eingabe zu beenden: ')
                    if cat.lower() == 'stop':
                        print('Eingabe wird beendet!')
                        time.sleep(2)
                        return False
                    else:
                        file.write(f'{cat}\n')
                        
    # Kategorie Ausgabe
    def kategorie_ausgabe(self):
        if not os.path.isfile(category_path):
            print('Du hast noch keine Kategorien erstellt / die Datei ist noch nicht existent!'
                  '\nBitte führe zuerst die Kategorienfunktion aus.')
            time.sleep(3)
        else:
            with open(category_path, 'r') as file:
                for line in file:
                    stripped = line.strip()
                    category_list.add(stripped)
            print(sorted(category_list))
            time.sleep(5)
    
    # Ausgabe einer Grafik, welche anhand von Machine-Learning eine Vorhersage über die erwarteten Änderungen trifft.    
    def vorhersage(self):
        df = pd.read_csv(out_path)
        xs = [x for x in df['Datum']]
        ys = [y for y in df['Saldo']]
        
        # Die X-Werte aus XS und die Y-Werte aus YS werden in 2D Arrays umgewandelt, damit sklearn damit arbeiten kann.
        xss = []
        # [x[:1]]for x in xs] <- Alte Listcomprehension, zur Sicherheit als Kommentar hinterlegt, auch wenn es auch ohne Funktionieren sollte. 
        for x in xs:
            if x[0] == 0:
                x.replace(0, '')
            xss.append([x[:2]])
        yss = [[y] for y in ys]
        
        # sklearn liest die Werte ein.
        model = LinearRegression().fit(xss, yss)
        
        # sklearn erstellt eine Vorhersage.
        prediction = model.predict(xss)
        
        plt.plot(xs, ys, label='Saldoänderung')
        plt.plot(xs, prediction, label='Erwartete Saldoänderung')
        plt.xlabel('Datum')
        plt.ylabel('Saldo')
        plt.legend()
        plt.show()
        
    # Ausgabe der letzten Buchung
    def letzte_buchung(self):
        df = pd.read_csv(out_path)
        print(df.iloc[-1:])
        time.sleep(5)
        
        

# Der Variable s wird die Klasse Saldo zugewiesen, damit sich Tipparbeit gespart wird. Außerdem wird der Wert 0 für start und current übergeben,
# damit der Konstruktur die Werte innerhalb der Klasse weiterverwenden kann.
s = Saldo(0, 0)

# Die Klassenfunktion Anfangsbetrag wird ausgeführt, damit geprüft wird, ob die Output.csv vorhanden ist.
s.anfangsbetrag()

# Dauherhaft laufende Abfrage, damit der User nicht immer das Programm neu öffnen muss.
while True:

            # Erklärung der Auswahlmoeglichkeiten
            print('Um eine Aktion auszuwählen, gebe die entsprechende Ziffer, oder das entsprechende Wort (innerhalb der Anführungsstriche) ein.'
                  '\n1. "Einnahme" um eine Einnahme einzutragen\n2. "Ausgabe" um eine Ausgabe einzutragen\n'
                  '3. "Liste" um alle Saldos und Buchungen anzuzeigen\n4. "Grafik" um eine Grafik der Saldoänderungen anzuzeigen\n'
                  '5. "Vorhersage" um eine Grafik der erwarteten Saldoänderung anzuzeigen\n6. "Letzte Buchung" um die letzte Buchung anzuzeigen'
                  '\n7. "Kategorien" um Buchungskategorien hinzuzufügen\n8. "Kategorien Ausgabe" um dir die hinterlegten Kategorien auszugeben'
                  '\nUm das Programm zu beenden gebe Quit ein.')
            
            # Auswahl wird in einer Vairable zwischengespeichert.
            wahl = input('Was möchtest du tun? ')
            
            # Pruefen ob die Auswahl einer der hier gennanten Moeglichkeiten ist, Auswahl wird automatisch in Kleinbuchstaben konvertiert um alle Moeglichkeiten der User Eingabe zu erkennen.
            if wahl.lower() == 'einnahme' or wahl.lower() == '1':
                betrag = float(input('Gebe den Betrag der Einnahme ein: ').replace(',', '.'))
                s.einnahme(betrag)
            elif wahl.lower() == 'ausgabe' or wahl.lower() == '2':
                betrag2 = float(input('Gebe den Betrag der Ausgabe ein: ').replace(',', '.'))
                s.ausgabe(betrag2)
            elif wahl.lower() == 'quit':
                print('Das Programm wird in 5 Sekunden beendet.')
                
                # Programm wartet 5 Sekunden und schließt sich dann.
                time.sleep(5)
                exit('Beendet durch Nutzer.')
            
            # Ausgabe aller Saldi
            elif wahl.lower() == 'liste' or wahl.lower() == '3':
                s.liste()
                
            elif wahl.lower() == 'grafik' or wahl.lower() == '4':
                s.grafik()
                
            elif wahl.lower() == 'vorhersage' or wahl.lower() == '5':
                s.vorhersage()
                
            elif wahl.lower() == 'letzte buchung' or wahl.lower() == '6':
                s.letzte_buchung()
                
            elif wahl.lower() == 'kategorien' or wahl.lower() == '7':
                s.kategorien()
                
            elif wahl.lower() == 'kategorien ausgabe' or wahl.lower() == '8':
                s.kategorie_ausgabe()
            
            # Sollte keine der Usereingaben erkannt werden, wird die Meldung ausgegeben.
            else:
                print('Fehlerhafte Eingabe, bitte wiederholen!')
                time.sleep(5)
                
                