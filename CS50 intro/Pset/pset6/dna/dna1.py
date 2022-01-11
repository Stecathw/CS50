# open as argument 1 : csv file / STR count for individual
# open as argument 2 : text file / containing DNA sequence to identify


# open and read csv file (STR)
# open and read text file (DNA saquence)

# for each of STRs (1st line of csv file),
# compute the longest run of consecutive repeats int he DNA sequence

# if STR counts = individual STRs print name
# else "no match"
import sys
import csv


def main():

    # if incorrect number of argument, exit and print error message
    if len(sys.argv) != 3:
        print("Missing 1 or more command-line argument")
        sys.exit(1)

    # open and read csv file (STR)
    file_1 = open(sys.argv[1], "r")
    database = csv.DictReader(file_1)

    # open and read text file (DNA)
    with open(sys.argv[2], "r") as file_2:
        DNA = file_2.read()
    
    # Compute the counts for each STR
    counts = {}
    for STR in database.fieldnames[1:]:
        counts[STR] = maximum_consecutive_repeats(DNA, STR)
    print(counts)
    
    # Check each row for a matching profile
    for row in database:
        if all(counts[STR] == int(row[STR]) for STR in counts):
            print(row["name"])
            file_1.close()
            return
    print("No match")
    
    file_1.close()
    
    
def maximum_consecutive_repeats(DNA, STR):
    
    longest = 0
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
        longest = max(longest, count)
    return longest
    

main()
