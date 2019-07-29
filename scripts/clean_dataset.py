import pandas as pd 
import glob 
import os 
from sklearn.model_selection import train_test_split

directory = "C:/Users/gabof/Downloads/rap_videos/train_videos/csvs"
translate = {
 "carilBad1": "manos_abajo",
   "carilBad2": "bolsillos",
    "carilBad3": "manos_juntas",
    "carilBad4": "manos_atras",
    "carilBad5": "brazos_cruzados",
    "carilGood1": "gesticulando",
    "carilGood2": "pointing",
    "fernandoBad1": "manos_abajo",
    "fernandoBad2": "bolsillos",
    "fernandoBad3": "manos_juntas",
    "fernandoBad4": "manos_atras",
    "fernandoBad5": "brazos_cruzados",
    "ferGood1": "gesticulando",
    "ferGood2": "gesticulando",
    "ferGood3": "pointing",
    "gabrielBad1": "manos_abajo",
    "gabrielBad2": "manos_juntas",
    "gabrielBad3": "bolsillos",
    "gabrielBad4": "brazos_cruzados",
    "gabrielGood1": "pointing",
    "gabrielGood2": "gesticulando"
}
csvs = glob.glob(f"{directory}/*csv")
goods = [csv for csv in csvs if "Good" in csv]
bads = [csv for csv in csvs if "Bad" in csv]

print("Goods:", len(goods), "Bads:", len(bads))

#Read all csvs add posture columns and ds column
def concat_dfs(csvs, postura_b):
    dfs = []
    for csv in csvs:
        df = pd.read_csv(csv)
        print(csv, len(df))
        df["ds"] = os.path.basename(csv).split(".")[0]
        df["postura_b"] = postura_b
        dfs.append(df)
    return pd.concat(dfs)

good_dfs = concat_dfs(goods, 1)
bad_dfs = concat_dfs(bads, 0)
print("Good dfs:", len(good_dfs), "Bads:", len(bad_dfs))

total_df = pd.concat([good_dfs, bad_dfs])

#Add tipo de postura column according to filename
total_df["tipo_postura"] = total_df.ds
for k,v in translate.items():
    total_df["tipo_postura"] = total_df.tipo_postura.str.replace(k,v)
total_df["tipo_postura"] = pd.Categorical(total_df.tipo_postura)
total_df["postura"] = total_df.tipo_postura.cat.codes

print(total_df.ds.value_counts())
print(total_df.tipo_postura.value_counts())
print(total_df.postura.value_counts())
print(total_df.head())
print(total_df.columns)
total_df.to_csv(f"{directory}/complete.csv", index=False)


# TRAIN/TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(total_df, total_df.postura_b, test_size=0.20, random_state=42, stratify=total_df.postura)

print("X_train", len(X_train))
print(X_train.postura_b.value_counts())
print(X_train.postura.value_counts())

print("X_test", len(X_test))
print(X_test.postura_b.value_counts())
print(X_test.postura.value_counts())
X_train.to_csv(f"{directory}/train.csv", index=False)
X_test.to_csv(f"{directory}/test.csv", index=False)