import pickle
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))  # Dict mapping movie titles to metadata
new_df = pd.DataFrame.from_dict(movies_dict)
movie_index = new_df[new_df['title'] == "Avatar"].index[0]
print(movie_index)
print(new_df['title'][movie_index])
movie_id = new_df.iloc[507].movie_id
print(new_df['title'][movie_id])
# if "Avatar" in movies_dict['title'].values():
    # print("True, damnn true !!!!!!")