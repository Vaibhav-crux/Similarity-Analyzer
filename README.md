# Similarity-Analyzer
This Python script in the repository compares textual similarity between files in Google Cloud Storage. It uses NLP techniques like tokenization, stemming, and cosine similarity to measure similarity between file pairs in two folders within a bucket. The results are written to a CSV file for a detailed comparison.

## Overview
The Similarity Analyzer script compares the textual content of files in two folders within a Google Cloud Storage (GCS) bucket and calculates the similarity between each pair of files using cosine similarity. The results are saved to a CSV file for further analysis.

## Usage
1. **Google Cloud Storage Setup:** Ensure you have a GCS bucket with the necessary files in the specified folders.
2. **Install Dependencies:** Run `pip install nltk scikit-learn google-cloud-storage` to install the required libraries.
3. **Run the Script:** Copy and paste the provided script into a Python file (e.g., `text_similarity_analyzer.py`). Update the GCS bucket name, folder paths, and output CSV file path.
4. **Execute the Script:** Run the script to compare the textual similarity between files in the specified folders. Progress and results will be displayed in the console.
5. **Review Results:** Open the generated CSV file to analyze the similarity scores between file pairs.

## Script Components
- **Tokenization and Stemming:** The script tokenizes and stems the words in each file's content using the NLTK library.
- **Cosine Similarity Calculation:** It calculates the cosine similarity between pairs of files using the CountVectorizer and cosine_similarity modules from scikit-learn.
- **Google Cloud Storage Integration:** The script utilizes the Google Cloud Storage client library to access files stored in GCS.

## Example
```python
gcs_bucket_name = 'your-gcs-bucket'
folder1 = 'folder1/'
folder2 = 'folder2/'
output_csv = '/path/to/output.csv'

print("Processing...")

compare_folders(gcs_bucket_name, folder1, folder2, output_csv)
