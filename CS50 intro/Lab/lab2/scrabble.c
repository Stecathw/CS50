#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 == score2)
    {
        printf("Tie!\n");
    }
    else if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else
    {
        printf("Player 2 wins!\n");    
    }
    //printf("%i\n", score1);
    //printf("%i\n", score2);
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    
    int score = 0;
    
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        char letter = word[i];
        int j = 0;
        
        if (islower(letter))
        {
            j = letter - 97;
            score += POINTS[j];
        }
        
        else if (isupper(letter))
        {
            j = letter - 65;
            score += POINTS[j];
        }
    }
    return score;
}
