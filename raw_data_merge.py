import pandas as pd
import numpy as np
import os

korea_movie = pd.DataFrame()
foreign_movie = pd.DataFrame()

for n in os.listdir("./raw_data"):
    path = f"./raw_data/{n}"
    temp = pd.read_csv(path)
    if "Korea" in n:
        korea_movie = pd.concat([korea_movie, temp])
    else:
        foreign_movie = pd.concat([foreign_movie, temp])


korea_movie.to_csv("./2014_2023_KoreaMovie.csv", encoding="utf-8-sig", index=False)
foreign_movie.to_csv("./2014_2023_ForeignMovie.csv", encoding="utf-8-sig", index=False)