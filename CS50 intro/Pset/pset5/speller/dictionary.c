// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <cs50.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 5500;

// Hash table
node *table[N];

// Total words loaded in dictionary
int total_words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // Hash word to obtain a value
    int index = hash(word);
    // Access linked list at that index in the hash table
    // traverse linked list, looking for the word (strcasecmp)
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor -> word, word) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return (sum % N);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // Read strings from file one at a time until the end
    char word[LENGTH + 1];
    while (fscanf(file, "%s\n", word) != EOF)
    {
        // Create a new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        }

        // Hash word to obtain a new value (key or index)
        int index = hash(word);
        // Copy word into new node
        strcpy(new_node -> word, word);
        
        // Insert node into hash table at that location
        if (table[index] == NULL)
        {
            new_node -> next = NULL;
            table[index] = new_node;
        }
        else
        {
            new_node -> next = table[index];
            table[index] = new_node;
        }
        total_words ++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return total_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // Freeing linked list
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        
        while (cursor != NULL)
        {
            node *temp = cursor -> next;
            free(cursor);
            cursor = temp;
        }
    }
    return true;
}
