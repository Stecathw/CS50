#include <stdio.h>
#include <cs50.h>
#include <math.h>

int digits(long long credit) // Define function to calculate number of digits
{
    int count = 0;
    while (credit != 0)
    {
        credit = credit / 10;
        count++;
    }
    return count; //give back the result of the function
}

int main(void)
{
    string type = "INVALID";
    
    long long credit = get_long("Number : ");

    //printf("Number of digits : %d\n", digits(credit));

    int n = digits(credit);

    int bothdigits = credit / pow(10, (n - 2));
    int firstdigit = round(bothdigits / 10); // Visa only have 1 digits for check
    
    //printf("Twodigit : %i\n", bothdigits);
    //printf("First digit : %i\n", firstdigit);
    
    // Converting long imput to a list of int digits
    int digit = 0;
    int multidigit = 0;
    int d1 = 0;
    int d2 = 0;
    int sum1 = 0;
    int sum2 = 0;
    
    for (int i = 0 ; i < n; i++) 
    {
        long factor = pow(10, i);
        
        // Second to last digits
        if (i % 2 != 0)
        {
            digit = (credit / factor) % 10;
            multidigit = digit * 2;
            
            if (multidigit > 9)
            {
                d1 = multidigit % 10;
                d2 = multidigit / 10;
                multidigit = d1 + d2;
            }
            sum1 += multidigit;
        }
        
        // Other digits
        else
        {
            digit = (credit / factor) % 10;
            sum2 += digit;
        }
    }
    
    //printf("SUM1 = %i\n", sum1);
    //printf("SUM2 = %i\n", sum2);
    
    int SUM = sum1 + sum2;
    
    //printf("total = %i\n", SUM); 
    
    int validity = SUM % 10;
    
    //printf("validity = %i\n", validity);
    

    if (n == 15 && validity == 0) //AMEX type
    {
        if (bothdigits == 34 || bothdigits == 37)
        {
            type = "AMEX";
        }
    }
    
    else if (n == 13 && validity == 0) // VISA type
    {
        if (firstdigit == 4) // add condition "AND" luhn's algorythm = true
        {
            type = "VISA";
        }
    }

    else if (n == 16 && validity == 0) // VISA & MASTERCARD type
    {
        if (firstdigit == 4)
        {
            type = "VISA";
        }
        else if (bothdigits == 51 || bothdigits == 52 || bothdigits == 53 || bothdigits == 54 || bothdigits == 55)
        {
            type = "MASTERCARD";
        }
    }
    
    printf("%s\n", type);
    
}