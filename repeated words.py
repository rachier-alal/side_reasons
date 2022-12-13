import docx
from collections import Counter
filepath = 'nov22rejects.docx'
def count_repeated_words(filepath):
  # Open the file
  doc = docx.Document(filepath)

  # Create an empty list to store the words
  words = []

  # Loop through the paragraphs in the document
  for paragraph in doc.paragraphs:
    # Loop through the runs in the paragraph
    for run in paragraph.runs:
      # Extract the text from the run and split it into words
      run_words = run.text.split()

      # Add the words to the list
      words.extend(run_words)

  # Count the number of times each word appears in the list
  word_counts = Counter(words)

  # Loop through the word counts and print the results
  for word, count in word_counts.items():
    print(f"The word '{word}' appears {count} times.")

# Call the function to count the words in the file
count_repeated_words("path/to/file.docx")
