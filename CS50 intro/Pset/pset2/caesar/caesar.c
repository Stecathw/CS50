#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

//Call the functions written below
int check_digits(string key);
string cipher_text(int K, string plaintext);

// START with command "./caesar X" where X is digit key
int main(int argc, string argv[])
{
    //Before doing anything, key validity is checked (only digits)
    if (argc == 2)
    {
        string key = argv[1];
        int check = check_digits(key);
        if (check == 0)
        {
            //printf("Success\n");
            //printf("%s\n", argv[1]);
            string plaintext = get_string("plaintext: ");
            int K = atoi(key);
            cipher_text(K, plaintext);
            return 0;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

// check that all char are only digits
int check_digits(string key)
{
    int digit = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        int symbol = key[i];
        
        if (symbol > 47 && symbol < 58)
        {
            digit += 1;
        }
    }
    if (digit == strlen(key))
    {
        return 0;
    }
    else
    {
        return 1;
    }
}

// cypher plaintext with the key
string cipher_text(int K, string plaintext)
{

    printf("ciphertext: ");
    
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char C = plaintext[i];
        
        if (islower(C)) // abcde...
        {
            if ((C + K) > 122)
            {
                int wraparoundC = 97 + (C + K - 97) % 26; // to wrapround z to a
                printf("%c", wraparoundC);
            }
            else
            {
                printf("%c", C + K);
            }
        }
        else if (isupper(C)) // ABCDE...
        {
            if ((C + K) > 90)
            {
                int wraparoundC = 65 + (C + K - 65) % 26; // to wrapround Z to A
                printf("%c", wraparoundC);
            }
            else
            {
                printf("%c", C + K);
            }
        }
        else
        {
            printf("%c", C);
        }
    }
    printf("\n");
    return 0;
}
