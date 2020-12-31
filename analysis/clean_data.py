from combine_files import combine_files

# Combine tweets
combine_files(source_folder='../Data/tweet/', results_folder='./formated_data/tweet/')

# Combine users
combine_files(source_folder='../Data/user/', results_folder='./formated_data/user/')
