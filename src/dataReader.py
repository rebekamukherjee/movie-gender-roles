import ast
import pandas as pd
from tqdm.autonotebook import tqdm
import pickle


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
        self.cast = Cast(movie.cast)

    def __repr__(self):
        return 'ID = {}, Title = {}'.format(self.id, self.title)


class Cast:
    """
    Store information about movie cast
    """

    def __init__(self, cast_info):
        self.members = ast.literal_eval(cast_info)

    def get_female_cast(self):
        """
        Get female cast members of the movie

        :return: list of female cast members
        :rtype: list
        """
        return [member for member in self.members if member['gender'] == 1]

    def get_male_cast(self):
        """
        Get male cast members of the movie

        :return: list of male cast members
        :rtype: list
        """
        return [member for member in self.members if member['gender'] == 2]

    def __repr__(self):
        return str(self.members)


def convert_to_list(movies_df):
    """
    Convert a dataframe of movie information to a list of `Movie` objects

    :param movies_df: dataframe of movie information
    :type movies_df: pandas.DataFrame
    :return: list of Movie objects
    :rtype: list
    """
    movie_objects = []
    failed = []

    for row in tqdm(movies_df.iterrows(), total=len(movies_df), desc='Converting dataframe to Movie objects'):
        movie_id, row = row
        try:
            movie_objects.append(Movie(movie_id, row))
        except:
            failed.append((movie_id, row))

    print('Number of failures in processing = {}'.format(len(failed)))

    return movie_objects


# Create a list of movie objects from the dataframe
if __name__ == "__main__":
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

    # Read the metadata, keywords and cast information
    metadata = pd.read_csv(metadata_file, index_col='id')
    keywords = pd.read_csv(keywords_file, index_col='id')
    castinfo = pd.read_csv(credits_file, index_col='id')

    # Perform natural join on the tables using 'id' column
    print('Joining metadata, keywords and cast information')
    movies = metadata.join(keywords, sort=True)
    movies = movies.join(castinfo, sort=True)

    # movie_list = convert_to_list(movies.iloc[:100])
    movie_list = convert_to_list(movies)

    print('Processed total of {} movies'.format(len(movie_list)))

    # t = movie_list[1]

    # Serialize the list to disk
    with open(movies_pkl_file, 'wb') as movies_pkl:
        pickle.dump(movie_list, movies_pkl)
