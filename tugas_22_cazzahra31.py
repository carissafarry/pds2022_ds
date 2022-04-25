# %%
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# %%
alamat = "https://www.kompas.com/"
html = urlopen(alamat)
data = BeautifulSoup(html, 'html.parser')


# %%
table = data.findAll("div", {"class": "most__wrap"})[0]
titles = table.findAll("h4", {"class": "most__title"})

hasil = []
for title in titles:
    hasil.append(title.get_text())

df = pd.DataFrame(hasil, columns=['Judul Berita Populer'])
print(df)
