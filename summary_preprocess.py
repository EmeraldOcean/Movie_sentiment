import pandas as pd
import numpy as np
import re

from tqdm import tqdm
tqdm.pandas()

data_name = "2014_2023_ForeignMovie_summary"
data = pd.read_csv(f"{data_name}.csv")

# remove space
print("Remove Space...")
data['줄거리'] = data['줄거리'].progress_map(lambda x:str(x).replace("\n", " ").replace("\t", " ").replace("\r", " "))
data['줄거리'] = data['줄거리'].progress_map(lambda x:str(x).strip())


text_pattern = '[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9\\s]+'
special_pattern = ""

print("Extract Special Text...")
for text in data['줄거리']:
    text = re.sub(text_pattern, "", str(text)).replace("(", "").replace(")", "").replace("[", "").replace("]", "")
    special_pattern = special_pattern + text

special_pattern = list(special_pattern)
special_pattern.remove(".")
special_pattern = "".join(set(special_pattern))
special_pattern = "[" + special_pattern + "]"

special_pattern = special_pattern[:special_pattern.index('-')] + "\\" + special_pattern[special_pattern.index('-'):]

print(f"Special Text: {special_pattern}")

print("Remove Special Text...")
data['줄거리2'] = data['줄거리'].progress_map(lambda x:re.sub(special_pattern, "", x))
data['줄거리2'] = data['줄거리2'].progress_map(lambda x:str(x).replace("(", "").replace(")", "").replace("[", "").replace("]", ""))

data.to_csv(f"{data_name}_preprocess.csv", index=False, encoding="utf-8-sig")