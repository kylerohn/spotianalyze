import ast
from collections import defaultdict
import pandas as pd


# determine most common genres using defaultdict
def select_common_genres(genres: pd.DataFrame):
    common_genres = defaultdict(int)
    for sample in genres["genres"]:
        for genre in ast.literal_eval(sample):
            common_genres[genre] += 1
    
    kv = []
    for key, value in common_genres.items():
        kv.append((value, key))
    
    return sorted(kv, reverse=True)