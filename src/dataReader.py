import pandas as pd
from tqdm.autonotebook import tqdm
import pickle
import os

# Define data path
data_path = '../data/the-movies-dataset/'

# All file paths
credits_file = data_path + 'credits.csv'
keywords_file = data_path + 'keywords.csv'
links_file = data_path + 'links.csv'
metadata_file = data_path + 'movies_metadata.csv'
ratings_file = data_path + 'ratings.csv'

# Path for serializing processed objects to disk
movies_pkl_file = '../data/processed/movies.pkl'

# Read the metadata and keywords
metadata = pd.read_csv(metadata_file, index_col='id')
keywords = pd.read_csv(keywords_file, index_col='id')

# Perform natural join on the tables using 'id' column
print('Joining metadata and keywords')
movies = metadata.join(keywords, sort=True)


class Movie:
    """
    Store information about a movie. Has attributes like the movie id, title, budget
    keywords etc
    """

    def __init__(self, movie_id, movie):
        self.id = movie_id
        self.title = movie.original_title
        self.budget = movie.budget
        self.keywords = movie.keywords
        self.genres = movie.genres
        self.lang = movie.original_language
        self.overview = movie.overview
        self.revenue = movie.revenue
        self.vote_average = movie.vote_average
        self.vote_count = movie.vote_count


def convert_to_list(movies_df):
    """
    Convert a dataframe of movie information to a list of `Movie` objects

    :param movies_df: dataframe of movie information
    :type movies_df: pandas.DataFrame
    :return: list of Movie objects
    :rtype: list
    """
    movie_objects = []

    for row in tqdm(movies_df.iterrows(), total=len(movies_df), desc='Converting dataframe to Movie objects'):
        movie_id, row = row
        movie_objects.append(Movie(movie_id, row))

    return movie_objects


# Create a list of movie objects from the dataframe
movie_list = convert_to_list(movies)

# Serialize the list to disk
with open(movies_pkl_file, 'wb') as movies_pkl:
    pickle.dump(movie_list, movies_pkl)
