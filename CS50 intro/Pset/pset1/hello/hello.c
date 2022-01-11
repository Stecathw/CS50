#include <stdio.h>
#include <cs50.h>

int main(void)
{   
    // Ask for names :
    string name1 = get_string("What is your name ?");
    
    // Answer "Hello, so and so" :
    printf("Hello, %s\n", name1);
}