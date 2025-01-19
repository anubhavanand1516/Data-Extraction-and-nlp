# Text Analysis Pipeline

A comprehensive pipeline for analyzing text by extracting articles from URLs, processing the content, and generating insightful metrics such as sentiment scores, readability, and complexity.

## Key Features

- **Sentiment Analysis**:
  - Calculates Positive, Negative, Polarity, and Subjectivity scores.
- **Readability Metrics**:
  - Computes Gunning Fog Index, Average Sentence Length, and Percentage of Complex Words.
- **Text Extraction**:
  - Automatically scrapes article titles and content from provided URLs.
- **Text Preprocessing**:
  - Removes stop words and cleanses text for accurate analysis.
- **Results Export**:
  - Outputs processed data into a well-structured Excel file.

## Project Structure

```
.
├── MasterDictionary/
│   ├── positive-words.txt      # List of positive sentiment words
│   └── negative-words.txt      # List of negative sentiment words
├── StopWords/
│   ├── stop-words-file1.txt    # Stop word list (customizable)
│   ├── stop-words-file2.txt    # Additional stop word list
│   └── ...
├── Input.xlsx                  # Input file containing URLs
├── Output_Data_Structure.xlsx  # Output file with analysis results
├── articles/                   # Folder for storing extracted articles
│   └── (article text files)
├── main.py                     # Main script for running the analysis
└── README.md                   # Documentation
```

## Requirements

- **Python Version**: 3.x
- **Dependencies**:
  Install required libraries using pip:
  ```bash
  pip install pandas beautifulsoup4 requests textstat openpyxl
  ```

## Usage

1. **Prepare Input Files**:
   - Place `positive-words.txt` and `negative-words.txt` inside the `MasterDictionary/` folder.
   - Add stop word files in the `StopWords/` folder.
   - Provide an `Input.xlsx` file containing two columns:
     - `URL_ID`: Unique identifier for the URL.
     - `URL`: The web address to analyze.

2. **Run the Script**:
   Execute the script using:
   ```bash
   python main.py
   ```

3. **View the Results**:
   - Processed data will be saved in `Output_Data_Structure.xlsx`.
   - Extracted articles will be saved as `.txt` files in the `articles/` folder.

## Input and Output Examples

### Input File (`Input.xlsx`)
| URL_ID | URL                     |
|--------|-------------------------|
| 1      | https://example.com/foo |
| 2      | https://example.com/bar |

### Output File (`Output_Data_Structure.xlsx`)
| URL_ID | URL                     | POSITIVE SCORE | NEGATIVE SCORE | POLARITY SCORE | WORD COUNT | ... |
|--------|-------------------------|----------------|----------------|----------------|------------|-----|
| 1      | https://example.com/foo | 20             | 5              | 0.6            | 200        | ... |

## Additional Notes

- **Stop Words**:
  - You can customize stop word files in the `StopWords/` folder for specific use cases.
- **Sentiment Dictionaries**:
  - Ensure that the `positive-words.txt` and `negative-words.txt` files are complete and relevant to your analysis.
- **Error Handling**:
  - Any issues during article scraping will be logged in the console for troubleshooting.

## License

This project is open-source and available under the MIT License.

## Acknowledgements

- **Beautiful Soup**: Used for web scraping.
- **TextStat**: Utilized for computing readability and complexity metrics.
- **Pandas**: For data manipulation and Excel file handling.
