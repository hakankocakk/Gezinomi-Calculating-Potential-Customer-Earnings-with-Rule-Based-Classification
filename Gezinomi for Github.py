#Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama

#Kütüphaneleri tanımladım

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Veriyi okudum
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df = pd.read_excel("miuul_gezinomi.xlsx")


#Unique şehirler ve Frekansları
df["SaleCityName"].nunique()
df["SaleCityName"].value_counts()

#Unique Konseptler
df["ConceptName"].nunique()

#Hangi Concept’den kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()

#Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})

#Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"})

#Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})

#Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})

#Şehir-Concept kırılımındaPRICE ortalamaları nedir?
df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"})



#Şehir-Concept- Sezon kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceledim.

df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": ["mean", "count"]})
df.groupby(["SaleCityName", "ConceptName", "CInDay"]).agg({"Price": ["mean", "count"]})

#City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending = False)


#Indekste yer alan isimleri değişken ismine çevirdim.
agg_df.reset_index(inplace=True)

#Yeni seviye tabanlı müşterileri (persona) tanımladım.
agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].agg(lambda x: "_".join(x).upper(), axis=1)


#Yeni müşterileri (personaları) segmentlere ayırdım
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"Price": ["mean", "max", "sum"]})


#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediyoruz
agg_df.sort_values(by="Price")


def sales(new_user):
    print(agg_df[agg_df["sales_level_based"] == new_user])

print(agg_df["sales_level_based"].unique())
print()
print("Lütfen ŞEHİR_KONSEPT_SEZON Bilgisi Girin")

new_user = input("Yeni Müşteri: ")

sales(new_user)

#Projeyi Geliştirmeye Devam Ediyorum.





