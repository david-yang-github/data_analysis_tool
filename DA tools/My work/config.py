# Specify absolute path to store input and output data
input_path = 'C:\\Users\\dyang165\\OneDrive\\OneDrive - pwc\\Documents\\DA Toolbox\\Text Similarity\\text_similarity\\test\\input\\'
output_path = 'C:\\Users\\dyang165\\OneDrive\\OneDrive - pwc\\Documents\\DA Toolbox\\Text Similarity\\text_similarity\\test\\output\\'

# There may be encoding errors when reading different csv files, loop through possible encodings to make sure the file is properly loaded.
encoding_list = ['utf_8', 'unicode_escape', 'gbk', 'utf_16', 'ascii']

# Specify the file name without '.csv' suffix
file_name = 'WBC_EMPLOYEE_NAMES'

# Specify the field name of the column to undertake similarity check
corpus_field = 'NAME'

# Specify the field name of the column to distinguish base text and text to be compared 
flag_field = 'SOURCE'

# Specify the embedding method
embedding_method = 'tfidf'