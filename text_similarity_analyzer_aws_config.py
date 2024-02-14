# For AWS S3
import os
import csv
import nltk
import time
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import boto3
from botocore.exceptions import NoCredentialsError

# Download NLTK data
nltk.download('punkt')

# Define function to stem tokens
def stem_tokens(tokens, stemmer):
    return [stemmer.stem(token) for token in tokens]

# Define function to get text from a file in S3
def get_text_from_file(bucket_name, file_path, stemmer, encoding='utf-8'):
    try:
        # Create S3 client and access the file
        s3 = boto3.client('s3', aws_access_key_id='AKIA6GBMC2IYNDPZG3UB', aws_secret_access_key='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')
        # s3 = boto3.client('s3')
        
        # Download file content and preprocess it
        raw = s3.get_object(Bucket=bucket_name, Key=file_path)['Body'].read().decode(encoding)
        tokens = word_tokenize(raw)
        tokens = stem_tokens(tokens, stemmer)
        text = ' '.join(tokens)

        return text
    except Exception as e:
        print(f"Error extracting text from s3://{bucket_name}/{file_path}: {e}")
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

        # Create S3 client and access specified folders
        s3 = boto3.client('s3', aws_access_key_id='AKIA6GBMC2IYNDPZG3UB',
                          aws_secret_access_key='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')

        objs_folder1 = [obj['Key'] for obj in s3.list_objects(Bucket=bucket_name, Prefix=folder1).get('Contents', [])]
        objs_folder2 = [obj['Key'] for obj in s3.list_objects(Bucket=bucket_name, Prefix=folder2).get('Contents', [])]

        total_files = len(objs_folder1) * len(objs_folder2)
        processed_files = 0

        # Compare each pair of files
        for file1 in objs_folder1:
            for file2 in objs_folder2:
                text1 = get_text_from_file(bucket_name, file1, stemmer, encoding='ISO-8859-1')
                text2 = get_text_from_file(bucket_name, file2, stemmer, encoding='ISO-8859-1')

                if text1 is not None and text2 is not None:
                    similarity = calculate_similarity(text1, text2)
                    writer.writerow({'File1': file1, 'File2': file2, 'Similarity': similarity})

                processed_files += 1
                progress_percentage = (processed_files / total_files) * 100
                remaining_files = total_files - processed_files
                time_elapsed = time.time() - start_time
                time_per_file = time_elapsed / processed_files if processed_files > 0 else 0
                remaining_time = remaining_files * time_per_file

                hours, remainder = divmod(remaining_time, 3600)
                minutes, _ = divmod(remainder, 60)

                print(f"Progress: {progress_percentage:.2f}% "
                      f"({processed_files}/{total_files} files processed) "
                      f"Estimated Time Remaining: {int(hours)}h {int(minutes)}m", end='\r')

    # Record end time and calculate total execution time
    end_time = time.time()
    total_time_minutes = (end_time - start_time) / 60

    print(f"\nTask completed. Total execution time: {total_time_minutes:.2f} minutes.")


# Specify S3 bucket and folder paths
s3_bucket_name = 'S3_BUCKET_NAME'
folder1 = 'FOLDER1/'
folder2 = 'FOLDER2/'
output_csv = '/home/CSV_FILE_NAME.csv'

# Run the script
print("Processing...")

compare_folders(s3_bucket_name, folder1, folder2, output_csv)
