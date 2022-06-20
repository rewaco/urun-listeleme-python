from tkinter import ttk
from tkinter import *
import sqlite3


class Urun:
    db_name = "ürüneklekediyim.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Ürünler uygulaması")
        self.create_tables()
        # Frame Oluşturdum
        frame = LabelFrame(self.wind, text="Yeni ürün ekle")
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # ürün adı bölümü
        Label(frame, text="Ürün adı").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # ürün fiyatı bölümü
        Label(frame, text="Fiyat").grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # ürün ekleme butonu
        ttk.Button(frame, text="Ürünü ekle", command=self.add_product).grid(row=3, columnspan=2, sticky=W + E)

        # Mesajlar
        self.message = Label(text=' ', fg="red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # ürünler tablosu bölümü
        self.tree = ttk.Treeview(height=10)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="Ürün Adı", anchor=CENTER)
        # self.tree.heading("#1", text="Fiyat", anchor=CENTER)

        # silme ve düzenleme butonları bölümü
        ttk.Button(text="Sil", command=lambda: self.delete_product()).grid(row=5, column=0, sticky=W + E)
        ttk.Button(text="Düzenle", command=lambda: self.edit_product()).grid(row=5, column=1, sticky=W + E)
        ttk.Label(text="geliştirici discord: benkedyim#4550",font="bold").grid(row=6, column=0,)
        # ürünleri getirme fonksiyon
        self.get_products()

    def create_tables(self):
        with sqlite3.connect(self.db_name) as baglanti:
            im = baglanti.cursor()
            im.execute("""
                CREATE TABLE IF NOT EXISTS urunler (productID INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (32), price VARCHAR (32))
            """)
            baglanti.commit()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as baglanti:
            im = baglanti.cursor()
            result = im.execute(query, parameters)
            baglanti.commit()
        return result

    # ürünleri databaseden getirme fonksiyonu
    def get_products(self):
        # tabloyu sıfırlaya
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        query = 'SELECT * FROM urunler ORDER BY name DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO urunler VALUES(NULL,?,?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Ürün {} başarıyla eklendi'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Ürün adı ve fiyatı zorunludur'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Lütfen bir ürün seçiniz'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM urunler WHERE name = ?'
        self.run_query(query, (name,))
        self.message['text'] = 'Ürün {} başarıyla silindi'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Lütfen bir ürün seçiniz'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Ürünü düzenle"
        #eski ad
        Label(self.edit_wind, text= "Eski Adı").grid(row=0, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=name), state='readonly').grid(row=0, column=2)
        #yeni ad
        Label(self.edit_wind, text="Yeni Adı").grid(row=1, column=1)
        yeni_ad = Entry(self.edit_wind)
        yeni_ad.grid(row=1, column=2)

        # eski fiyat
        Label(self.edit_wind, text="Eski Fiyatı").grid(row=2, column=1)
        Entry(self.edit_wind, textvariable=StringVar(self.edit_wind, value=old_price), state='readonly').grid(row=2, column=2)
        # yeni fiyat
        Label(self.edit_wind, text="Yeni Fiyat").grid(row=3, column=1)
        yeni_fiyat = Entry(self.edit_wind)
        yeni_fiyat.grid(row=3, column=2)






        Button(self.edit_wind, text="Güncelle", command=lambda: self.edit_records(yeni_ad.get(), name, yeni_fiyat.get(), old_price)).grid(row=4, column=2, sticky=W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = "UPDATE urunler SET `name` = ?, price = ? WHERE `name` = ? AND price = ?"
        parameters = (new_name, new_price, name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Ürün {} başarıyla güncellendi'.format(name)
        self.get_products()


if __name__ == '__main__':
    window = Tk()
    application = Urun(window)
    window.mainloop()