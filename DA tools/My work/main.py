from text_similarity import TextSimilarity 
from config import input_path, output_path, encoding_list, corpus_field, flag_field, file_name, embedding_method

def main(input_path: str, output_path: str, encoding_list: list, corpus_field: str, flag_field: str, file_name: str, embedding_method: str):

    text_similarity_obj = TextSimilarity(input_path, output_path, encoding_list, corpus_field, flag_field)
    
    df_input = text_similarity_obj.read_data(file_name)
    text_similarity_obj.embedding(embedding_method)
    df_cos_similarity = text_similarity_obj.get_cos_similarity()
    df_most_similar_text = text_similarity_obj.get_most_similar_text(df_cos_similarity)
    text_similarity_obj.output_data(df_cos_similarity, df_most_similar_text)


if __name__ == '__main__':
    main(input_path, output_path, encoding_list, corpus_field, flag_field, file_name, embedding_method)


