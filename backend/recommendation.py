import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from collections import OrderedDict

df = pd.read_json(r'db/media.json')
genres = df["Genre"]
genres_list =[]
for i in range(len(genres)):
    genres_list.append(" ".join(genres[i]))
media_df = pd.DataFrame(genres_list, columns=["genres"], index=df['Title'])

recommended_ids = []

def genreBasedRecommender(media_index):
    cv = CountVectorizer()
    X = cv.fit_transform(media_df["genres"]).toarray()
    output = df.loc[:,['Title']]
    output = output.join(pd.DataFrame(X))
    similarities = cosine_similarity(X) 
    similarity_values = pd.Series(similarities[media_index])
    similarity_values.sort_values(ascending=False)
    similar_media_indexes = list(similarity_values.sort_values(ascending=False).index)
    similar_media_indexes.remove(media_index)

    return similar_media_indexes

def contentBasedRecommender(media_index):
    title = df['Title'].iloc[media_index]
    tfidf_vector = TfidfVectorizer(stop_words='english')
    df['Description'] = df['Description'].fillna('')
    tfidf_matrix = tfidf_vector.fit_transform(df['Description'])
    sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['Title']).drop_duplicates()
    idx = indices[title]    
    sim_scores = list(enumerate(sim_matrix[idx]))    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)    
    sim_scores = sim_scores[1:11]    
    movie_indices = [i[0] for i in sim_scores]   

    return movie_indices

def main(media_index):
    global recommended_ids

    genre_based = genreBasedRecommender(media_index)
    content_based = contentBasedRecommender(media_index)

    final_list = []
    final_list.extend(list((value for value in content_based if value in genre_based)))
    final_list.extend(list((value for value in content_based if value not in genre_based)))  
    final_list.extend(list((value for value in genre_based[:15] if value not in content_based))) 
    recommended_ids.extend(final_list)
    recommended_ids = list(OrderedDict.fromkeys(recommended_ids))

if __name__ == '__main__':
    main(220)
    print(recommended_ids)