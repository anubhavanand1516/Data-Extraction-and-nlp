import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from textstat import textstat

# Load Positive and Negative Words
positive_words = set(line.strip() for line in open("MasterDictionary/positive-words.txt", encoding="ISO-8859-1"))
negative_words = set(line.strip() for line in open("MasterDictionary/negative-words.txt", encoding="ISO-8859-1"))

# Load Stop Words
stop_words = set()
for stopword_file in os.listdir("StopWords"):
    with open(f"StopWords/{stopword_file}", encoding="ISO-8859-1") as file:
        stop_words.update(line.strip() for line in file)

# Helper Functions
def remove_stopwords(text, stop_words):
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

def calculate_positive_score(text, positive_words):
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for word in words if word in positive_words)

def calculate_negative_score(text, negative_words):
    words = re.findall(r'\b\w+\b', text.lower())
    return sum(1 for word in words if word in negative_words)

def calculate_polarity_score(positive_score, negative_score):
    return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

def calculate_subjectivity_score(text, positive_score, negative_score):
    words = len(re.findall(r'\b\w+\b', text))
    return (positive_score + negative_score) / (words + 0.000001)

def count_complex_words(text):
    words = re.findall(r'\b\w+\b', text)
    return sum(1 for word in words if textstat.syllable_count(word) > 2)

def calculate_syllable_per_word(text):
    words = re.findall(r'\b\w+\b', text)
    total_syllables = sum(textstat.syllable_count(word) for word in words)
    return total_syllables / len(words) if words else 0

def calculate_avg_word_length(text):
    words = re.findall(r'\b\w+\b', text)
    total_length = sum(len(word) for word in words)
    return total_length / len(words) if words else 0

# Data Extraction
def extract_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1')
        title_text = title.get_text(strip=True) if title else "No Title Found"
        paragraphs = soup.find_all('p')
        content = ' '.join(p.get_text(strip=True) for p in paragraphs) if paragraphs else "No Content Found"
        return title_text + "\n" + content
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""

# Input File Processing
input_file = "Input.xlsx"
output_file = "Output_Data_Structure.xlsx"
input_data = pd.read_excel(input_file)

results = []

# Process Each URL
for _, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Extract Text
    article_text = extract_article_text(url)
    os.makedirs("articles", exist_ok=True)
    with open(f"articles/{url_id}.txt", 'w', encoding='utf-8') as file:
        file.write(article_text)

    # Preprocess Text
    cleaned_text = remove_stopwords(article_text, stop_words)

    # Text Analysis
    positive_score = calculate_positive_score(cleaned_text, positive_words)
    negative_score = calculate_negative_score(cleaned_text, negative_words)
    polarity_score = calculate_polarity_score(positive_score, negative_score)
    subjectivity_score = calculate_subjectivity_score(cleaned_text, positive_score, negative_score)
    
    word_count = len(re.findall(r'\b\w+\b', cleaned_text))
    if word_count > 0:
        percentage_complex_words = (count_complex_words(cleaned_text) / word_count) * 100
        fog_index = textstat.gunning_fog(cleaned_text)
        avg_words_per_sentence = textstat.avg_sentence_length(cleaned_text)
        syllable_per_word = calculate_syllable_per_word(cleaned_text)
        avg_word_length = calculate_avg_word_length(cleaned_text)
    else:
        percentage_complex_words = 0
        fog_index = 0
        avg_words_per_sentence = 0
        syllable_per_word = 0
        avg_word_length = 0

    # Append Results
    results.append({
        "URL_ID": url_id,
        "URL": url,
        "POSITIVE SCORE": positive_score,
        "NEGATIVE SCORE": negative_score,
        "POLARITY SCORE": polarity_score,
        "SUBJECTIVITY SCORE": subjectivity_score,
        "AVG SENTENCE LENGTH": avg_words_per_sentence,
        "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_words_per_sentence,
        "COMPLEX WORD COUNT": count_complex_words(cleaned_text),
        "WORD COUNT": word_count,
        "SYLLABLE PER WORD": syllable_per_word,
        "AVG WORD LENGTH": avg_word_length
    })

# Save Results to Output File
output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)

print(f"Analysis complete. Results saved to {output_file}.")
