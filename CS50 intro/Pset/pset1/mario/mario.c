#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Height of pyramid
    
    int height;
    do
    {
        height = get_int("Height : ");
    }
    while (height < 1 || height > 8);
    
    //Print righ aligned pyramid
    
    int row = height - 1;
    int space = height - 1;
    
    for (int i = 0; i < height; i++)  
    {
        for (int k = space; k > 0; k--) // Loop to right align pyramid
        {    
            printf(" ");
        }
        for (int j = row; j < height; j++) // Loop to create block #
        {
            printf("#");
        }
        printf("  ");
        
        for (int l = row; l < height; l++)
        {
            printf("#");
        }
        printf("\n");
        row --;
        space--;
    }
}
