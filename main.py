import random
import tkinter.messagebox
import cx_Oracle
from faker import Faker
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
from datetime import date, timedelta
import calendar

root = tk.Tk()
root.title("Generator to Oracle")
root.geometry("750x300")
root.resizable(False, False)

try:
    fake = Faker()
    #productB = ['okularki adidas', 'okularki nike', 'kapielowki nike', 'kapielowki arena', 'zatyczki do nosa', 'czepek arena',
    #           'okularki arena', 'klapki adidas', 'recznik arena', 'bidon nike', 'bidon adidas', 'stroj arena']
    #productS = ['woda 1l', 'woda 500ml', 'snickers 90g', 'mars 90g', 'izotonik oshee 700ml', 'baton protein go 60g', 'knoppers 50g',
    #           'pepsi 330ml', 'mirinda 330ml', 'sprite 330ml', 'sok cappy 250ml', 'sok tarczyn 330ml']
    typbiletu = [1, 2, 3, 4, 5]
    platnosc = ['Karta', 'Gotowka']

    #connection
    connection = cx_Oracle.connect('login/password@ip:1234/tpdb')
    cursor = connection.cursor()


    def checkMaxIDProduktS():
        query = "SELECT MAX(id_produkt) FROM produkty_spozywcze"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDProduktB():
        query = "SELECT MAX(id_produkt) FROM produkty_basenowe"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDRelation1():
        query = "SELECT MAX(transakcja_id_transakcja) FROM relation_1"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDRelation7():
        query = "SELECT MAX(transakcja_id_transakcja) FROM relation_7"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDTransakcja():
        query = "SELECT MAX(id_transakcja) FROM transakcja"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDData_zakupu():
        query = "SELECT MAX(data_zakupu) FROM Transakcja"
        cursor.execute(query)
        id = cursor.fetchone()
        if (id == None):
            id = 0
        return id

    def checkMaxIDBilet():
        query = "SELECT MAX(id_bilet) FROM bilet"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDKarnet():
        query = "SELECT MAX(id_karnet) FROM karnet"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDPracownik():
        query = "SELECT MAX(id_pracownik) FROM pracownik"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkMaxIDKlient():
        query = "SELECT MAX(id_klient) FROM klient"
        cursor.execute(query)
        id = cursor.fetchone()[0]
        if (id == None):
            id = 0
        return id

    def checkTimeAndRandom():
        startDate = fake.date_this_century()
        id = checkMaxIDData_zakupu()
        if id[0] is None:
            lastStartDate = startDate
        else:
            lastStartDate = id[0].date()

        while (lastStartDate > startDate):
            startDate = fake.date_this_century()

        days = [7, 14, 31, 91, 183]
        diff = timedelta(days=random.choice(days)) if random.randint(0, 1) else timedelta(days=30)
        endDate = startDate + diff

        while endDate == startDate or (endDate - startDate).days not in days and (
                endDate - startDate).days != 30:
            endDate = startDate + timedelta(days=calendar.monthrange(startDate.year, startDate.month)[1])
            diff = timedelta(days=random.choice(days)) if random.randint(0, 1) else timedelta(days=30)
            endDate += diff
        return startDate, endDate

    def zegarek():
        number_list = list(range(1, 201))
        while True:
            random_number = random.choice(number_list)
            yield random_number
            number_list.remove(random_number)
            if not number_list:
                number_list = list(range(1, 201))

    def randomPrice():
        while True:
            price = random.randint(10, 300)
            if price % 5 == 0:
                return price

    def transakcja():
        with tqdm(total=val) as pbar:
            t = f"----------------" \
                f"Tabela transakcja" \
                f"----------------\n"
            with open('inserts.txt', 'a') as f:
                f.write(t)
                idT = checkMaxIDTransakcja()
                idKR = checkMaxIDKarnet()
                idB = checkMaxIDBilet()
                idKL = checkMaxIDKlient()
                idPB = checkMaxIDProduktB()
                idPS = checkMaxIDProduktS()

                karnetidkarnet = []
                for i in range(1, idKR + 1):
                    karnetidkarnet.append(i)
                biletidbilet = []
                for i in range(1, idB + 1):
                    biletidbilet.append(i)
                klientidklient = []
                for i in range(1, idKL + 1):
                    klientidklient.append(i)
                produktbidprodukt = []
                for i in range(1, idPB + 1):
                    produktbidprodukt.append(i)
                produktsidprodukt = []
                for i in range(1, idPS + 1):
                    produktsidprodukt.append(i)

                for il in range(1, val + 1):
                    startDate, endDate = checkTimeAndRandom()
                    zeg = zegarek()

                    query = f"INSERT INTO Transakcja(id_transakcja, typplatnosci, nrkluczyka, cena, ilosc, data_zakupu, data_waznosci," \
                            f"produkty_spozywcze_id_produkt, produkty_basenowe_id_produkt, karnet_id_karnet, bilet_id_bilet) VALUES " \
                            f"('{idT + il}', '{random.choice(platnosc)}', '{next(zeg)}', '{randomPrice()}', '{random.choice(typbiletu)}', TO_DATE('{startDate}', 'RRRR-MM-DD'), TO_DATE('{endDate}', 'RRRR-MM-DD'),'{random.choice(produktsidprodukt)}', '{random.choice(produktbidprodukt)}', '{random.choice(karnetidkarnet)}', '{random.choice(biletidbilet)}')\n"
                    cursor.execute(query)
                    f.write(query)
                    pbar.update(1)
                connection.commit()

    def bilet():
        with tqdm(total=val) as pbar:
            t = f"----------------" \
                f"Tabela bilet" \
                f"----------------\n"
            with open('inserts.txt', 'a') as f:
                f.write(t)
                idB = checkMaxIDBilet()
                idKL = checkMaxIDKlient()

                klientidklient = []
                for i in range(1, idKL + 1):
                    klientidklient.append(i)

                for il in range(1, val + 1):
                    query = f"INSERT INTO Bilet(id_bilet, typbiletu, nrbiletu, klient_id_klient, rodzajbiletu_id_rodzaj) VALUES ({idB + il}, '{random.choice(typbiletu)}', '{idB + il}','{random.choice(klientidklient)}', '{random.choice(typbiletu)}')\n "
                    cursor.execute(query)
                    f.write(query)
                    pbar.update(1)
                connection.commit()

    def relation1():
        with tqdm(total=val) as pbar:
            t = f"----------------" \
                f"Tabela relation_1" \
                f"----------------\n"
            with open('inserts.txt', 'a') as f:
                f.write(t)
                idR1 = checkMaxIDRelation1()
                idKL = checkMaxIDKlient()

                klientidklient = []
                for i in range(1, idKL + 1):
                    klientidklient.append(i)

                for il in range(1, val + 1):
                    query = f"INSERT INTO Relation_1(klient_id_klient, transakcja_id_transakcja) VALUES ('{random.choice(klientidklient)}', '{idR1+il}')\n "
                    cursor.execute(query)
                    f.write(query)
                    pbar.update(1)
                connection.commit()

    def relation7():
        with tqdm(total=val) as pbar:
            t = f"----------------" \
                f"Tabela relation_7" \
                f"----------------\n"
            with open('inserts.txt', 'a') as f:
                f.write(t)
                idR7 = checkMaxIDRelation7()
                idP = checkMaxIDPracownik()

                pracownikidpracownik = []
                for i in range(1, idP + 1):
                    pracownikidpracownik.append(i)

                for il in range(1, val + 1):
                    query = f"INSERT INTO Relation_7(pracownik_id_pracownik, transakcja_id_transakcja) VALUES ('{random.choice(pracownikidpracownik)}', '{idR7 + il}')\n "
                    cursor.execute(query)
                    f.write(query)
                    pbar.update(1)
                connection.commit()

    def karnet():
            idKR = checkMaxIDKarnet()
            idKL = checkMaxIDKlient()

            klientidklient = []
            for i in range(1, idKL + 1):
                klientidklient.append(i)

            with tqdm(total=val) as pbar:
                t = f"----------------" \
                    f"Tabela karnet" \
                    f"----------------\n"
                with open('inserts.txt', 'a') as f:
                    f.write(t)
                    for il in range(1, val + 1):
                        query = f"INSERT INTO Karnet(id_karnet, typkarnetu, klient_id_klient, rodzajkarnetu_id_rodzaj) VALUES ({idKR + il}, '{random.choice(typbiletu)}','{random.choice(klientidklient)}', '{random.choice(typbiletu)}')\n "
                        cursor.execute(query)
                        f.write(query)
                        pbar.update(1)
                connection.commit()

    def pracownik():
            idP = checkMaxIDPracownik()

            with tqdm(total=val) as pbar:
                t = f"----------------" \
                    f"Tabela pracownik" \
                    f"----------------\n"
                with open('inserts.txt', 'a') as f:
                    f.write(t)
                    for il in range(1, val + 1):
                        query = f"INSERT INTO Pracownik(id_pracownik, imie, nazwisko) VALUES ({idP + il}, '{fake.first_name()}', '{fake.last_name()}')\n"
                        cursor.execute(query)
                        f.write(query)
                        pbar.update(1)
                connection.commit()

    def klient():
        idKL = checkMaxIDKlient()

        with tqdm(total=val) as pbar:
            t = f"----------------" \
                f"Tabela klient" \
                f"----------------\n"
            with open('inserts.txt', 'a') as f:
                f.write(t)
                for il in range(1, val + 1):
                    query = f"INSERT INTO Klient(id_klient, imie, nazwisko) VALUES ({idKL + il}, '{fake.first_name()}', '{fake.last_name()}')\n"
                    cursor.execute(query)
                    f.write(query)
                    pbar.update(1)
                connection.commit()

    def save_input():
        global val
        val = int(all.get())

        klient()
        bilet()
        karnet()
        transakcja()
        pracownik()
        relation1()
        relation7()

    title = tk.Label(root, text="Generator to Oracle - 2023")
    title.config(font=("Helvetica", 16, "bold"))
    title.grid(row=0, column=1, sticky="", padx=10, pady=10)

    label1 = tk.Label(root, text="Generate to all tables in database: ", name="l1")
    label1.grid(row=1, column=0)

    all = tk.Entry(root, name="all", width=10)
    all.insert(0, "10")
    all.grid(row=2, column=1)

    button1 = tk.Button(root, text="GENERATE", command=save_input, width=22, height=1)
    button1.grid(row=2, column=0)

    label2 = tk.Label(root, text="Generate for only the selected table in database: ", name="l2")
    label2.grid(row=1, column=2, sticky="W")

    combo = ttk.Combobox(root)

    table_names = []
    table_names.append("")
    for row in cursor.execute("SELECT * FROM user_tables WHERE table_name not in ('PRODUKTY_BASENOWE', 'PRODUKTY_SPOZYWCZE', 'RODZAJBILETU', 'RODZAJKARNETU')"):
        table_names.append(row[0])
    table_names.sort()

    combo_values = []
    for name in table_names:
        combo_values.append(name)
    combo['values'] = combo_values

    combo.current(0)
    combo.grid(row=2, column=2)

    combo2 = ttk.Combobox(root)

    table_names = []
    table_names.append("")
    for row in cursor.execute(
            "SELECT * FROM user_tables WHERE table_name not in ('PRODUKTY_BASENOWE', 'PRODUKTY_SPOZYWCZE', 'RODZAJBILETU', 'RODZAJKARNETU')"):
        table_names.append(row[0])
    table_names.sort()

    combo_values = []
    for name in table_names:
        combo_values.append(name)
    combo2['values'] = combo_values

    combo2.current(0)
    combo2.grid(row=4, column=1)

    def buttonGenerateSelected():
        global val
        val = int(all.get())

        if(combo.get()=="BILET"):
            bilet()
        elif(combo.get()=="TRANSAKCJA"):
           transakcja()
        elif(combo.get()=="RELATION_1"):
            relation1()
        elif (combo.get() == "RELATION_7"):
            relation7()
        elif (combo.get() == "KARNET"):
            karnet()
        elif (combo.get() == "PRACOWNIK"):
            pracownik()
        elif (combo.get() == "KLIENT"):
            klient()

    def clearBilet():
        id = checkMaxIDBilet()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table BILET is empty!")
        else:
            query = "DELETE FROM BILET"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in BILET " + str(id) + " elements!")
        return id

    def clearTransakcja():
        id = checkMaxIDTransakcja()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table TRANSAKCJA is empty!")
        else:
            query = "DELETE FROM TRANSAKCJA"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in TRANSAKCJA " + str(id) + " elements!")
        return id

    def clearRelation1():
        id = checkMaxIDRelation1()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table RELATION_1 is empty!")
        else:
            query = "DELETE FROM RELATION_1"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in RELATION_1 " + str(id) + " elements!")
        return id

    def clearRelation7():
        id = checkMaxIDRelation7()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table RELATION_7 is empty!")
        else:
            query = "DELETE FROM RELATION_7"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in RELATION_7 " + str(id) + " elements!")

    def clearKarnet():
        id = checkMaxIDKarnet()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table KARNET is empty!")
        else:
            query = "DELETE FROM KARNET"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in KARNET " + str(id) + " elements!")
        return id

    def clearPracownik():
        id = checkMaxIDPracownik()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table PRACOWNIK is empty!")
        else:
            query = "DELETE FROM PRACOWNIK"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in PRACOWNIK " + str(id) + " elements!")
        return id

    def clearKlient():
        id = checkMaxIDKlient()
        if (id == 0):
            tkinter.messagebox.showinfo("Error", "Table KLIENT is empty!")
        else:
            query = "DELETE FROM KLIENT"
            cursor.execute(query)
            connection.commit()
            tkinter.messagebox.showinfo("Completed", "Deleted in KLIENT " + str(id) + " elements!")
        return id

    def buttonClearSelected():
        if (combo2.get() == "BILET"):
            clearBilet()
        elif (combo2.get() == "TRANSAKCJA"):
            clearTransakcja()
        elif (combo2.get() == "RELATION_1"):
            clearRelation1()
        elif (combo2.get() == "RELATION_7"):
            clearRelation7()
        elif (combo2.get() == "KARNET"):
            clearKarnet()
        elif (combo2.get() == "PRACOWNIK"):
            clearPracownik()
        elif (combo2.get() == "KLIENT"):
            clearKlient()

    def clearFile():
        with open("inserts.txt", 'w') as f:
            f.write('')
        tkinter.messagebox.showinfo("Completed", "File is empty!")

    def buttonClearAll():
        clearRelation1()
        clearRelation7()
        clearTransakcja()
        clearBilet()
        clearKarnet()
        clearPracownik()
        clearKlient()
        clearFile()

    generateSelected = tk.Button(root, text="GENERATE", name="generateSelected", command=buttonGenerateSelected, width=22)
    generateSelected.grid(row=3, column=2, sticky="S")

    label = tk.Label(root, text="Clear selected table:")
    label.grid(row=4, column=0, pady=50 ,sticky="E")
    button3 = tk.Button(root, text="CLEAR", name="button3", command=buttonClearSelected)
    button3.grid(row=4, column=1, sticky="E")
    label = tk.Label(root, text="Clear all tables:")
    label.grid(row=5, column=0, sticky="E")
    button4 = tk.Button(root, text="CLEAR", name="button4", command=buttonClearAll)
    button4.grid(row=5, column=1, sticky="W")

    label = tk.Label(root, text="Copyright © 2023 Jakub Pieszczek")
    label.grid(row=6, column=2, sticky="E")

    root.mainloop()

except cx_Oracle.DatabaseError as e:
    print(f'Error: {e}')
finally:
    cursor.close()
    connection.close()