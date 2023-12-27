import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

def preprocess_data(folder, processed_data_path):
    amazonprime = pd.read_csv(folder + 'amazonprime.csv')
    appletv = pd.read_csv(folder + 'appletv.csv')
    disneyplus = pd.read_csv(folder + 'disneyplus.csv')
    hbomax = pd.read_csv(folder + 'hbomax.csv')
    netflix = pd.read_csv(folder + 'netflix.csv')
    paramountplus = pd.read_csv(folder + 'paramountplus.csv')

    dfs = [amazonprime, appletv, disneyplus, hbomax, netflix, paramountplus]
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df.drop_duplicates(subset='title', inplace=True)
    df = df.drop(columns=['id', 'release_year', 'age_certification', 'runtime', 'seasons', 'imdb_id', 'imdb_score', 'imdb_votes', 'tmdb_popularity', 'tmdb_score'])
    df.dropna(subset=['title'], inplace=True)
    df['type'].fillna('', inplace=True)
    df['description'].fillna('', inplace=True)
    df['genres'].fillna('', inplace=True)
    df['production_countries'].fillna('', inplace=True)
    
    df.to_csv(processed_data_path, index=False)
    return df

def get_description_similarity_scores(input_movie_title, df: pd.DataFrame):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_description = tfidf_vectorizer.fit_transform(df['description'].fillna(''))

    input_movie_features = tfidf_vectorizer.transform(df[df['title'] == input_movie_title]['description'].fillna(''))

    cosine_sim = cosine_similarity(input_movie_features, tfidf_matrix_description)
    similarity_scores = pd.DataFrame({'title': df['title'], 'description_similarity_score': cosine_sim[0]})
    return similarity_scores

def get_genre_similarity_scores(input_movie_title, df: pd.DataFrame):
    df['genres'] = df['genres'].apply(lambda x: x.split(','))
    input_movie_genres = set(df[df['title'] == input_movie_title]['genres'].iloc[0])
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_genre = tfidf_vectorizer.fit_transform(df['genres'].apply(lambda x: ' '.join(x)))

    input_movie_features = tfidf_vectorizer.transform([' '.join(input_movie_genres)])

    cosine_sim = cosine_similarity(input_movie_features, tfidf_matrix_genre)
    similarity_scores = pd.DataFrame({'title': df['title'], 'genre_similarity_score': cosine_sim[0]})
    return similarity_scores

def get_country_similarity_scores(input_movie_title, df: pd.DataFrame):
    df['production_countries'] = df['production_countries'].apply(lambda x: eval(x))
    input_movie_countries = set(df[df['title'] == input_movie_title]['production_countries'].iloc[0])
    
    similarity_scores = pd.DataFrame({
        'title': df['title'],
        'country_similarity_score': df['production_countries'].apply(
            lambda x: len(set(x).intersection(input_movie_countries)) / len(set(x).union(input_movie_countries)) if x else 0)
    })
    return similarity_scores

def get_recommendations(input_movie_title, df: pd.DataFrame, number_of_recommendations: int):
    df.fillna('', inplace=True)

    description_similarity_scores = get_description_similarity_scores(input_movie_title, df)
    genre_similarity_scores = get_genre_similarity_scores(input_movie_title, df)
    country_similarity_scores = get_country_similarity_scores(input_movie_title, df)

    description_weight = 0.6
    genre_weight = 0.3
    country_weight = 0.1

    similarity_scores_df = pd.merge(description_similarity_scores, genre_similarity_scores, on='title')
    similarity_scores_df = pd.merge(similarity_scores_df, country_similarity_scores, on='title')

    similarity_scores_df['similarity_score'] = (
        description_weight * similarity_scores_df['description_similarity_score'] +
        genre_weight * similarity_scores_df['genre_similarity_score'] +
        country_weight * similarity_scores_df['country_similarity_score']
    )

    df = pd.merge(df, similarity_scores_df[['title', 'similarity_score']], on='title')
    df = df[df['title'] != input_movie_title]

    recommendations = df.sort_values(by='similarity_score', ascending=False).head(number_of_recommendations).reset_index()
    return recommendations[['title', 'type', 'similarity_score']]


def main():
    folder = 'data/'
    processed_data_path = 'data/processed_data.csv'
    if not os.path.exists(processed_data_path):
        processed_data = preprocess_data(folder, processed_data_path)
    else:
        processed_data = pd.read_csv(processed_data_path)
    
    while True:
        movie_title = input("Find recommendations based on title: ")
        if movie_title in processed_data['title'].values:
            recommendations = get_recommendations(movie_title, processed_data, 10)
            print(recommendations)
        else:
            print(f"{movie_title} is not in the datasets.")
        print()

if __name__ == "__main__":
    main()
