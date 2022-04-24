import re
import pandas as pd
import numpy as np

df = pd.read_json(r'db/media.json')

recommended_ids = [0, 1, 10, 18, 35, 47, 76, 95, 115, 137, 170, 180, 199, 215, 237, 242]

def content_based_recommendation():
    global recommended_ids
    recommended_ids = np.random.randint(low=0, high=249, size=30).tolist()
    print("Updated recommendations!")