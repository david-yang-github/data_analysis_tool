import os 
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

class TextSimilarity:
    """
    1. Load csv data and determine the 1) base text (N rows) and 2) text to be compared (M rows) with base text according to flag_field.
    2. Choose proper embedding method (eg. tfidf ...) to transform text-based data into computer-readable data for further calculation.
    3. Calculate the similarity between base text and compared text, and generate a similarity matrix (N * M) in pandas.DateFrame format.
    4. Pick the compared text with maximum similarity score under each base text, and generate a simpler comparison result (N * 1) for reference. 
    """

    def __init__(self, input_path: str, output_path: str, encoding_list: list, corpus_field: str, flag_field: str):
        """
        Initiate the attributes for the class.

        :param input_path: absolute path storing original text file.
        :type input_path: str
        :param output_path: absolute path to save similarity checked text file.
        :type output_path: str
        :param encoding_list: loop through possible encodings to make sure the original text file could be loaded properly.
        :type encoding_list: list
        :param corpus_field: field name of the column to similarity check in original text file.
        :type corpus_field: str
        :param flag_field: field name of the column to determine base text/text to be compared in original text file (1: base text, 0: text to be compared).
        :type flag_field: str
        """
        self.input_path = input_path
        self.output_path = output_path
        
        self.encoding_list = encoding_list
        
        self.corpus_field = corpus_field
        self.flag_field = flag_field
        
        if not os.path.exists(self.input_path):
            os.mkdir(self.input_path)
        
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        
    def read_data(self, file_name: str) -> pd.DataFrame:
        """
        Read the original text file in input path and sort it (base text -> text to be compared).

        :param file_name: original text file (without ".csv" suffix).
        :type file_name: str
        :return: sorted original text file.
        :rtype: pd.DataFrame
        """
        self.file_name = file_name
        input_file_path = os.path.join(self.input_path, f'{self.file_name}.csv')
        for encoding in self.encoding_list:
            try:
                df = pd.read_csv(input_file_path, encoding=encoding)
                df.sort_values(by=self.flag_field, ascending=False, inplace=True)
                self.corpus = df[self.corpus_field].tolist()
                # TODO: Standardize flag field's category types (1: base text, 0: text to be compared with)
                self.cutoff_value = df.loc[df[self.flag_field] == 'journal'].shape[0]
                return df
            except Exception as err:
                print(f'Read csv error occurred: {err}, trying other encoding')
    
    def tfidf_embedding(self, max_features: int):
        """
        tfidf: Use the methodology of word frequency to transform text-based data into computer-readable data (a matrix of TF-IDF features).

        :param max_features: ordered by term frequency across the corpus. Set to be 20000 at the moment.
        :type max_features: int
        """
        
        self.vectorizer = TfidfVectorizer(max_features=max_features)
        self.embedding = self.vectorizer.fit_transform(self.corpus)
        
    def embedding(self, embedding_method: str):
        """
        More embedding methods to be added, and user could choose practical ones accordingly.

        :param embedding_method: user could choose any method from available list (tfidf, ...).
        :type embedding_method: str
        :return: embedding matrix.
        :rtype: _type_
        """
        self.embedding_method = embedding_method
        if self.embedding_method == 'tfidf':
            # TODO: Need flexible parameter
            return self.tfidf_embedding(20000)
        else:
            print(f'{self.embedding_method} does not exist.')
    
    def get_cos_similarity(self)-> pd.DataFrame:
        """
        Calculate the similarity between base text and compared text using embedding matrix multiplication.
        Each cell stands for the similarity score, the higher, the more similar.

        Matrix size: N * M.
        N: # of base text.
        M: # of text to be compared.

        :return: similarity score matrix dateframe.
        :rtype: pd.DataFrame
        """
        cos_similarity = (round(self.embedding[:self.cutoff_value] * self.embedding[self.cutoff_value:].T, 2)).toarray()
        df_cos_similarity = pd.DataFrame(cos_similarity, index=list(self.corpus)[:self.cutoff_value], columns=list(self.corpus)[self.cutoff_value:])
        
        return df_cos_similarity
    
    def get_most_similar_text(self, df_cos_similarity: pd.DataFrame) -> pd.DataFrame:
        """
        Pick the compared text with maximum similarity score under each base text, and generate a simpler comparison result (N * 1) for reference.

        :param df_cos_similarity: similarity score matrix dateframe.
        :type df_cos_similarity: pd.DataFrame
        :return: most similar text dateframe.
        :rtype: pd.DataFrame
        """
        raw_text_list = []
        max_score_list = []
        for i in df_cos_similarity.index:
            raw_text_list.append(i)

            max_score = df_cos_similarity.loc[i].max()
            max_score_list.append(max_score)

        most_similar_text_list = df_cos_similarity.idxmax(axis=1).tolist()

        df_most_similar_text = pd.DataFrame(list(zip(raw_text_list, most_similar_text_list, max_score_list)),\
                  columns=['raw text','most similar text', 'max similarity score'])
        
        return df_most_similar_text
    
        
    def output_data(self, df_cos_similarity: pd.DataFrame, df_most_similar_text: pd.DataFrame):
        """
        Export similarity score matrix and most similar text under chosen embedding method

        :param df_cos_similarity: similarity score matrix dateframe.
        :type df_cos_similarity: pd.DataFrame
        :param df_most_similar_text: most similar text dateframe.
        :type df_most_similar_text: pd.DataFrame
        """
        output_files = {}
        output_files['similarity_matrix'] = df_cos_similarity
        output_files['most_similar_text'] = df_most_similar_text
        
        for k, v in output_files.items():
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            output_file_path = os.path.join(self.output_path, f'{self.file_name}_{k}_{self.embedding_method}_{current_time}.csv')
            v.to_csv(output_file_path, index=False)
            
        print('Done!')