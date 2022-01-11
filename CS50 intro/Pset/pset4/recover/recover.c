#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
#define BLOCKSIZE 512
#define FILENAMESIZE 8
 
int main(int argc, char *argv[])
{
    // Check for one argument : image as input
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    
    // read file and check if readable
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open file : %s\n", argv[1]);
        return 1;
    }
    
    BYTE buffer[BLOCKSIZE];
    FILE *output = NULL;
    char filename[FILENAMESIZE];
    int counter = 0;
    
    //read file and look for beginning of a JPEG
    while (fread(&buffer, BLOCKSIZE, 1, file))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (output != NULL)
            {
                fclose(output);
            }
            // Open a new JPG file
            sprintf(filename, "%03i.jpg", counter);
            output = fopen(filename, "w");
            counter ++;
            
            if (output == NULL)
            {
                return 1;
            }
        }
        //Write 512 Bytes until a new JPG is found
        if (output != NULL)
        {
            fwrite(&buffer, BLOCKSIZE, 1, output);
        }
    }
    
    //Close files and stop
    fclose(file);
    fclose(output);
    return 0;
}