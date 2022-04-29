import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_json(r'db/media.json')
genres = df["Genre"]
genres_list =[]
for i in range(len(genres)):
    genres_list.append(" ".join(genres[i]))
media_df = pd.DataFrame(genres_list, columns=["genres"], index=df['Title'])

recommended_ids = [0, 1, 10, 18, 35, 47, 76, 95, 115, 137, 170, 180, 199, 215, 237, 242]

def content_based_recommendation():
    global recommended_ids
    recommended_ids = np.random.randint(low=0, high=249, size=30).tolist()
    print("Updated recommendations!")

def recommend(movie_index):
    cv = CountVectorizer()
    X = cv.fit_transform(media_df["genres"]).toarray()
    output = df.loc[:,['Title']]
    output = output.join(pd.DataFrame(X))
    similarities = cosine_similarity(X) 
    similarity_values = pd.Series(similarities[movie_index])
    similarity_values.sort_values(ascending=False)
    similar_movie_indexes = list(similarity_values.sort_values(ascending=False).index)
    similar_movie_indexes.remove(movie_index)

    for i in range(15):
        print(similar_movie_indexes[i])

if __name__ == '__main__':
    recommend(220)