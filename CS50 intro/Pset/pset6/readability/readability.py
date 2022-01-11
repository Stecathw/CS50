from cs50 import get_string
import math


# Computes the approximate grade level needed to comprehend some text and give a grade
def main():
    TEXT = get_string("Text: ")
    letters = number_of_letters(TEXT)
    words = number_of_words(TEXT)
    sentences = number_of_sentences(TEXT)
    L = average_letters_per_100_words(TEXT)
    S = average_sentences_per_100_words(TEXT)
    index = coleman_liau_index(TEXT)
    
    # Give grade based on computed index   
    if index > 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


# Count letters
def number_of_letters(TEXT):
    # is the char alphabetic ?
    number = 0
    for i in range(len(TEXT)):
        char = TEXT[i]
        if char.isalpha():
            number += 1
    return number


# Count words
def number_of_words(TEXT):
    # At least 1 word, and then count spaces.
    number = 1
    for i in range(len(TEXT)):
        char = TEXT[i]
        if char == ' ':
            number += 1
    return number

    
# Count sentences
def number_of_sentences(TEXT):
    # punctuation ! . ?
    number = 0
    for i in range(len(TEXT)):
        char = TEXT[i]
        if char == "." or char == "!" or char == "?":
            number += 1
    return number


# L is the average number of letters per 100 words in the text
def average_letters_per_100_words(TEXT):
    
    letters = number_of_letters(TEXT)
    words = number_of_words(TEXT)
    average = (letters / words) * 100
    return average


# S is the average number of sentences per 100 words in the text
def average_sentences_per_100_words(TEXT):
    
    sentences = number_of_sentences(TEXT)
    words = number_of_words(TEXT)
    average = (sentences / words) * 100
    return average

    
# Coleman-Liau index
def coleman_liau_index(TEXT):
    
    i = round(0.0588 * average_letters_per_100_words(TEXT) - 0.296 * average_sentences_per_100_words(TEXT) - 15.8)
    return i
    

main()