#include <stdio.h>
#include <cs50.h>
#include <math.h>

//
int main(void)
{
    float owed;
    do
    {
        owed = get_float("Changed owed : "); // ask how musch is owed
    }
    while (owed < 0);
    
    int cents = round(owed * 100); // convert imput into cents to avoid errors of calculation

    int n = 0; // minimum number of coins with which that change can be made
    
    int nquarter = 0; //counting cents
    int ndime = 0;
    int nnickel = 0;
    int npennie = 0;
    
    if (cents >= 25) // how many quarters ? quarters = 25c
    {
        nquarter = cents / 25;
        n += nquarter;
        cents -= nquarter * 25;
    }
    
    if (cents >= 10) // how many dimes ? dimes = 10c
    {
        ndime = cents / 10;
        n += ndime;
        cents -= ndime * 10;
    }
    
    if (cents >= 5) // how many nickels ? nickels = 5c
    {
        nnickel = cents / 5;
        n += nnickel;
        cents -= ndime * 5;
    }
    
    if (cents >= 1) // how many pennies ? pennies = 1c
    {
        npennie = cents / 1;
        n += npennie;
        cents -= npennie * 1;
    }
    
    printf("%i\n", n);
}