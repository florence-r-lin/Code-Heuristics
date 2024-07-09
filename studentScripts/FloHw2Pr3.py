# CS 5 Gold, hw2pr3
# filename: hw2pr3.py
# Name: Florence Lin
# problem description: List comprehensions



# this gives us functions like sin and cos...
from math import *



# two more functions (not in the math library above)

def dbl(x):
    """Doubler!  argument: x, a number"""
    return 2*x

def sq(x):
    """Squarer!  argument: x, a number"""
    return x**2



# examples for getting used to list comprehensions...

def lc_mult(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each multiplied by 2**
    """
    return [2*x for x in range(N)]

def lc_idiv(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each divided by 2**
       WARNING: this is INTEGER division...!
    """
    return [x//2 for x in range(N)]

def lc_fdiv(N):
    """This example accepts an integer N
       and returns a list of integers
       from 0 to N-1, **each divided by 2**
       NOTE: this is floating-point division...!
    """
    return [x/2 for x in range(N)]

# printing tests
print( "lc_mult(4)   should be [0, 2, 4, 6] :", lc_mult(4) )   
print( "lc_idiv(4)   should be [0, 0, 1, 1] :", lc_idiv(4) ) 
print( "lc_fdiv(4)   should be [0.0, 0.5, 1.0, 1.5] :", lc_fdiv(4) ) 

# assertion tests
assert lc_mult(4) == [0, 2, 4, 6]
assert lc_idiv(4) == [0, 0, 1, 1]
assert lc_fdiv(4) == [0.0, 0.5, 1.0, 1.5]

# Here is where your functions start for the lab:

# Step 1, part 1
def unitfracs(N):
    """returns a list of evenly-spaced left-hand endpoints (fractions) in the unit interval [0, 1)
    """
    return [x/N for x in range(N)]

# Step 1, part 2
def scaledfracs(low, high, N):
    """returns N left endpoints uniformly through the interval [low, high).
       basically the scaled fraction of low high N 
    """
    return [x*(high-low)+low for x in unitfracs(N)]

# Step 2, part 1
def sqfracs(low, high, N):
    """returns scaledfracs(low, high, N) but each value returned in scaledfracs is squared
       basically takes three numbers and returns the square of its scaled fraction created in scaled fracs
    """
    return [x**2 for x in scaledfracs(low,high,N)]

# Step2, pt 2
def f_of_fracs(f, low, high, N):
    """returns f of N numbers in scaled fraction by using four values (f, low, high, N) where f is the function, low is the bottom limit
       high is the top limit, and N is the number of scaled fraction
    """
    return [f(x) for x in scaledfracs(low,high,N)]


#Step 3
def integrate(f, low, high, N):
    """Integrate returns an estimate of the definite integral
       of the function f (the first argument)
       with lower limit low (the second argument)
       and upper limit high (the third argument)
       where N steps are taken (the fourth argument)

       integrate simply returns the sum of the areas of rectangles
       under f, drawn at the left endpoints of N uniform steps
       from low to high
    """
    return sum(f_of_fracs(f, low, high, N)) * (high-low)/N

#Q 2
def c(x):
    """c is a semicircular function of radius two"""
    return (4 - x**2)**0.5


print( "integrate(dbl, 0, 10, 4) should be 75 :", integrate(dbl, 0, 10, 4) )
print( "integrate(sq, 0, 10, 4) should be 218.75 :", integrate(sq, 0, 10, 4) )


