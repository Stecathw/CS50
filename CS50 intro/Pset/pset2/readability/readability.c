#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

int number_of_letters(string TEXT);
int number_of_words(string TEXT);
int number_of_sentences(string TEXT);
float average_letters_per_100_words(string TEXT);
float average_sentences_per_100_words(string TEXT);
int coleman_liau_index(string TEXT);

int main(void)
{
    string TEXT = get_string("Text: ");
    int letters = number_of_letters(TEXT);
    int words = number_of_words(TEXT);
    int sentences = number_of_sentences(TEXT);
    float L = average_letters_per_100_words(TEXT);
    float S = average_sentences_per_100_words(TEXT);
    int index = coleman_liau_index(TEXT);
    //printf("%i letter(s)\n", letters);
    //printf("%i word(s)\n", words);
    //printf("%i sentence(s)\n", sentences);
    //printf("L = %f\n", L);
    //printf("S = %f\n", S);
    
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }  
}

//Count letters
int number_of_letters(string TEXT)
{
    int number = 0;
    for (int i = 0, n = strlen(TEXT); i < n; i++)
    {
        char symbol = TEXT[i];
        
        if (islower(symbol) || isupper(symbol))
        {
            number += 1;
        }
    }
    return number;
}

//count words
int number_of_words(string TEXT) // SPACE = 32 
{
    int number = 1; //as a sentence = min 1 word before a space
    for (int i = 0, n = strlen(TEXT); i < n; i++)
    {
        int symbol = TEXT[i];
        
        if (symbol == 32)
        {
            number += 1;
        }
    }
    return number;
}

//count sentence
int number_of_sentences(string TEXT) // . = 46  ? = 63  ! = 33
{
    int number = 0;
    for (int i = 0, n = strlen(TEXT); i < n; i++)
    {
        int symbol = TEXT[i];
        
        if (symbol == 46 || symbol == 63 || symbol == 33)
        {
            number += 1;
        }
    }
    return number;
}

// L is the average number of letters per 100 words in the text
float average_letters_per_100_words(string TEXT)
{
    float letters = number_of_letters(TEXT);
    float words = number_of_words(TEXT);
    float average = (letters / words) * 100;
    return average;
}

// S is the average number of sentences per 100 words in the text
float average_sentences_per_100_words(string TEXT)
{
    float sentences = number_of_sentences(TEXT);
    float words = number_of_words(TEXT);
    float average = (sentences / words) * 100;
    return average;
}

// Coleman-Liau index
int coleman_liau_index(string TEXT)
{
    int index = round(0.0588 * average_letters_per_100_words(TEXT) - 0.296 * average_sentences_per_100_words(TEXT) - 15.8);
    return index;
}
