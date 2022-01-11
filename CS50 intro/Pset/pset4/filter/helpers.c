#include "helpers.h"
#include <math.h>
#include <cs50.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
int capped(int color)
{
    if (color > 255)
    {
        color = 255;
    }
    return color;
}

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;
            
            int SepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);
            int SepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int SepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            
            image[i][j].rgbtBlue = capped(SepiaBlue);
            image[i][j].rgbtGreen = capped(SepiaGreen);
            image[i][j].rgbtRed = capped(SepiaRed);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    
    for (int i = 0; i < height; i++)
    {
        int k = width - 1;
        for (int j = 0; j < (width / 2); j++)
        {
            temp[i][k] = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = temp[i][k];
            k--;
        }
    }
    return;
}

// Blur image

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float pixelnumber = 0;
            for (int row = -1; row < 2; row++)
            {
                for (int col = -1; col < 2; col++)
                {
                    if (i + row < 0 || i + row > height - 1 || j + col < 0 || j + col > width - 1)  
                    {
                        continue;
                    }
                    red += image[i + row][j + col].rgbtRed;
                    green += image[i + row][j + col].rgbtGreen;
                    blue += image[i + row][j + col].rgbtBlue;
                    pixelnumber += 1;
                }
            }
            temp[i][j].rgbtRed = round(red / pixelnumber);
            temp[i][j].rgbtGreen = round(green / pixelnumber);
            temp[i][j].rgbtBlue = round(blue / pixelnumber);
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
        }
    }
    
    return;
}

