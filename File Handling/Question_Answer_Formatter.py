"""
Program: Flashcard Text Formatter
Author: Madhurima Rawat
Description:
    This script reads a text file containing question–answer pairs
    (separated by a TAB) and formats them neatly for study or revision.

Input File Format (Question_Answer_Input.txt):
    Question<TAB>Answer

Output File:
    formatted_qa.txt

Output Style:
    ============================================================

    Q.1 Question text here
    Answer:
    Answer text here
"""

# ----------------------- FILE PATHS -----------------------

# Input file containing raw questions and answers
file_path = "Question_Answer_Input.txt"

# Output file to store formatted content
output_file = "Formatted_Question_Answer_Input.txt"

# -------------------- FILE PROCESSING --------------------

# Open input file for reading and output file for writing
with open(file_path, "r", encoding="utf-8") as infile, open(
    output_file, "w", encoding="utf-8"
) as outfile:

    # Enumerate through each line to auto-number questions
    for i, line in enumerate(infile, start=1):

        # Skip empty lines (if any)
        if line.strip():

            # Split the line into question and answer using TAB separator
            question, answer = line.strip().split("\t")

            # Write separator line
            outfile.write("=" * 60 + "\n\n")

            # Write formatted question
            outfile.write(f"❓Q.{i} {question}\n")

            # Write answer label
            outfile.write("📃Answer:\n")

            # Write answer text
            outfile.write(answer + "\n")

    # Final closing separator
    outfile.write("=" * 60)
