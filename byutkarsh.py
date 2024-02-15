import os
import csv
import nltk
import time
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')

# Define function to stem tokens
def stem_tokens(tokens, stemmer):
    return [stemmer.stem(token) for token in tokens]

# Define function to get text from a local file
def get_text_from_file(file_path, stemmer, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            raw = file.read()
            tokens = word_tokenize(raw)
            tokens = stem_tokens(tokens, stemmer)
            text = ' '.join(tokens)

            return text
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return None

# Define function to calculate cosine similarity between two texts
def calculate_similarity(text1, text2):
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    similarity = cosine_similarity(vectorizer)
    similarity_value = similarity[0, 1]
    return similarity_value

# Define function to compare files in two folders and write results to CSV
def compare_folders(folder1, folder2, output_csv):
    stemmer = PorterStemmer()

    # Record start time
    start_time = time.time()

    # List files in specified folders
    files_folder1 = [os.path.join(folder1, file) for file in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, file))]
    files_folder2 = [os.path.join(folder2, file) for file in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, file))]

    # Open CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header row
        header_row = ['Files from Folder1'] + [os.path.basename(file) for file in files_folder2]
        writer.writerow(header_row)

        # Compare each file in folder1 with each file in folder2
        for file1 in files_folder1:
            row = [os.path.basename(file1)]
            text1 = get_text_from_file(file1, stemmer, encoding='ISO-8859-1')
            if text1 is not None:
                for file2 in files_folder2:
                    text2 = get_text_from_file(file2, stemmer, encoding='ISO-8859-1')
                    if text2 is not None:
                        similarity = calculate_similarity(text1, text2)
                        row.append(similarity)
            writer.writerow(row)

    # Record end time and calculate total execution time
    end_time = time.time()
    total_time_minutes = (end_time - start_time) / 60

    print(f"\nTask completed. Total execution time: {total_time_minutes:.2f} minutes.")

# Specify local folder paths
folder1 = 'path/to/folder1'
folder2 = 'path/to/folder2'
output_csv = 'path/to/output.csv'

# Run the script
print("Processing...")
compare_folders(folder1, folder2, output_csv)
