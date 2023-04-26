import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n")

product_code = input("Wprowadź kod produktu: ")

opinions = pd.read_json(f"./opinions/{product_code}.json")

#opinions.score = opinions.score.map(lambda x: float(x[:-2].replace(",",".")))
opinions.score = opinions.score.map(lambda x: float(x.split("/")[0].replace(",",".")))

print(opinions)

opinions_count = len(opinions.index)
pros_count = opinions.pros.map(bool).sum()
cons_count = opinions.cons.map(bool).sum()
avg_score = round(opinions.score.mean(), 2)

print(f'''Dla produktu o kodzie {product_code} dostepnych jest {opinions_count} opinii. 
Dla {pros_count} opinii jest dostepna lista zalet. 
Dla {cons_count} opinii jest dostepna list wad. 
Srednia ocena produktu wynosi {avg_score}''')

#histogram czestosci wystepowania poszczegolnych ocen

score = opinions.score.value_counts().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
score.plot.bar(color="skyblue")
plt.xticks(rotation=0)
plt.title("Histogram ocen")
plt.xlabel("Liczba gwiazdek")
plt.ylabel("Liczba opinii")
for index, value in enumerate(score):
    plt.text(index, value+0.22, str(value), ha="center")
try:
    os.mkdir(path="./plots")
except FileExistsError:
    pass
plt.savefig(f"./plots/{product_code}_score.png")

#udzial poszczegolnych rekomendacji w ogolnej liczbie opinii

recommendation = opinions["recommendation"].value_counts(dropna = False).sort_index()
print(recommendation)
recommendation.plot.pie(
    label = "",
    autopct="%1.1f%%",
    labels = ["Nie polecam", "Polecam", "Nie mam zdania"],
    colors = ["crimson", "forestgreen", "gray"]
)

plt.legend(bbox_to_anchor=(1.0,1.0))
plt.savefig(f"./plots/{product_code}_recommendation.png")

plt.close()