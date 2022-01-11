# open as argument 1 : csv file / STR count for individual
# open as argument 2 : text file / containing DNA sequence to identify
# if incorrect number of argument, exit and print error message

# open and read csv file (STR)
# open and read text file (DNA saquence)

# for each of STRs (1st line of csv file),
# compute the longest run of consecutive repeats int he DNA sequence

# if STR counts = individual STRs print name
# else "no match"

import csv
import sys


def main():

    if len(sys.argv) != 3:
        print("Missing 1 or more command-line argument")
        sys.exit(1)
    
    # Open as dictionary the csv file database.
    csv_file = open(sys.argv[1], "r")
    database = csv.DictReader(csv_file)
    
    # Open and close the text file. Store DNA sequence in a list.
    with open(sys.argv[2], "r") as txt_file:
        DNA = txt_file.read()
        
    # Create a dict to store each amount of STRs counted in the DNA sequence.
    counts = {}
    # Retrieve STRs in database (carefull, begin at second col)
    for STR in database.fieldnames[1:]:
        counts[STR] = maximum_consecutive_repeat(DNA, STR)
        
    # Check each row of databse and each STR in the row for match with counts
    print(search_match(database, STR, counts))
    
    # When done, close csv file    
    csv_file.close()
    

def search_match(database, STR, counts):
    
    match = "No match"
    for row in database:
        if all(counts[STR] == int(row[STR]) for STR in counts):
            match = row["name"]
    return match


# compute the longest run of consecutive repeats int he DNA sequence
def maximum_consecutive_repeat(DNA, STR):
    
    consecutive = 0
    lenght = len(STR)
    for i in range(len(DNA)):
        count = 0
        while True:
            start = i + lenght * count
            end = start + lenght
            if DNA[start:end] == STR:
                count += 1
            else:
                break
        consecutive = max(consecutive, count)
    return consecutive

    
main()