import pandas as pd

data_path = '../data/the-movies-dataset/'

credits_file  = data_path + 'credits.csv'
keywords_file = data_path + 'keywords.csv'
links_file    = data_path + 'links.csv'
metadata_file = data_path + 'movies_metadata.csv'
ratings_file  = data_path + 'ratings.csv'

metadata = pd.read_csv(metadata_file, index_col='id')
keywords = pd.read_csv(keywords_file, index_col='id')

movies = metadata.join(keywords, sort=True)
print(movies)
