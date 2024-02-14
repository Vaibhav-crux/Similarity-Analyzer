# For GCP
# Import necessary libraries
import os
import csv
import nltk
import time
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google.cloud import storage

# Download NLTK data
nltk.download('punkt')

# Define function to stem tokens
def stem_tokens(tokens, stemmer):
    return [stemmer.stem(token) for token in tokens]

# Define function to get text from a file in GCS
def get_text_from_file(bucket_name, file_path, stemmer, encoding='utf-8'):
    try:
        # Create GCS client and access the file
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        # Download file content and preprocess it
        raw = blob.download_as_text(encoding=encoding)
        tokens = word_tokenize(raw)
        tokens = stem_tokens(tokens, stemmer)
        text = ' '.join(tokens)

        return text
    except Exception as e:
        print(f"Error extracting text from gs://{bucket_name}/{file_path}: {e}")
        return None

# Define function to calculate cosine similarity between two texts
def calculate_similarity(text1, text2):
    # Tokenize and convert text to a matrix of token counts
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(vectorizer)
    
    # Extract the similarity value
    similarity_value = similarity[0, 1]
    
    return similarity_value

# Define function to compare files in two folders and write results to CSV
def compare_folders(bucket_name, folder1, folder2, output_csv):
    # Initialize stemming
    stemmer = PorterStemmer()
    
    # Record start time
    start_time = time.time()

    # Open CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['File1', 'File2', 'Similarity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write CSV header
        writer.writeheader()

        # Create GCS client and access specified folders
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blobs_folder1 = [blob.name for blob in bucket.list_blobs(prefix=folder1)]
        blobs_folder2 = [blob.name for blob in bucket.list_blobs(prefix=folder2)]

        total_files = len(blobs_folder1) * len(blobs_folder2)
        processed_files = 0

        # Compare each pair of files
        for file1 in blobs_folder1:
            for file2 in blobs_folder2:
                text1 = get_text_from_file(bucket_name, file1, stemmer, encoding='ISO-8859-1')
                text2 = get_text_from_file(bucket_name, file2, stemmer, encoding='ISO-8859-1')

                if text1 is not None and text2 is not None:
                    similarity = calculate_similarity(text1, text2)
                    writer.writerow({'File1': file1, 'File2': file2, 'Similarity': similarity})

                processed_files += 1
                progress_percentage = (processed_files / total_files) * 100
                print(f"Progress: {progress_percentage:.2f}% ({processed_files}/{total_files} files processed)", end='\r')
                
    # Record end time and calculate total execution time
    end_time = time.time()
    total_time_minutes = (end_time - start_time) / 60

    print(f"\nTask completed. Total execution time: {total_time_minutes:.2f} minutes.")

# Specify GCS bucket and folder paths
gcs_bucket_name = 'GCP Bucket Name'
folder1 = 'folder1/'
folder2 = 'folder2/'
output_csv = '/path/to/vectorCount.csv'

# Run the script
print("Processing...")

compare_folders(gcs_bucket_name, folder1, folder2, output_csv)
