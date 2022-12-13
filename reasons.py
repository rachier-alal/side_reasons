# Import the python-docx library
import docx

users = ['Raymond Gitonga', 'Dennis Gituma', 'Phyllis Wachiuri', 'Raymond Chepkwony', 'Sharon Oyoo', 'Becca Nouvelle', 'John Ngone', 'Collins Kemboi','Annbel Kamau','Linda Chalker','Ann Njeri']




# Open the Word document
document = docx.Document('nov22rejects.docx')

# Loop through all the paragraphs in the document
for paragraph in document.paragraphs:
  # Check if the paragraph has any text
  if not paragraph.text:
    # The paragraph doesn't have any text, so delete it
    paragraph.clear()

  if paragraph.bold:
    if paragraph not in  

# Save the changes to the Word document
document.save('nov22rejects.docx')
