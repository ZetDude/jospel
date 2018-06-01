# Jospel

### Jospel is a simple math-oriented game played on a grid and some cards with numbers on them  

The cards are just the numbers from 1 to 10, twice over, resulting in 20 cards. The cards are shuffled and showed one by one. Every time a card is shown, the player must write the number down to a 4x4 grid. You may not see the next number until you have placed the last, and you cannot relocate numbers. Note that as the grid fits only 16 numbers, not all cards will be used up, therefore you may never know if some patterns are possible to achieve. The strategy part comes into play when we talk about the points system

### For each row and column, certain patterns give points

In Jospel, there are 5 types of patterns each row or column can give points for. Rows and columns are treated equally, so I'll just refer to both of them as "rows" from here on out. A row can give no points.

### The patterns of Jospel

A single row can only give points for one type of pattern.

#### Pair - 10 points
A pair consists of two consecutive identical numbers. A pair be located anywhere in the row.
Examples:

3, __4, 4__, 8 (4 and 4)   
__5, 5__, 8, 10 (5 and 5)    

#### Double pair - 20 points
A double pair consists of two pairs of consecutive identical numbers, or two alternating numbers.
Examples:

**6, 6**, *1, 1* (6 and 6, 1 and 1)    
**5**, *3*, **5**, *3* (5 and 5, 3 and 3)     

#### Short streak - 30 points
A short streak consists of three consecutive numbers that are descending or ascending one by one.
Examples:

4, __8, 7, 6__ (8>7>6)    
10, __2, 3, 4__ (2<3<4)    

#### Long streak - 40 points
A long streak consists of four consecutive numbers that are descending or ascending one by one
Examples:

5, 6, 7, 8 (5<6<7<8)    
10, 9, 8, 7 (10>9>8>7)    

#### The Jospel - 50 points
The Jospel is a pattern similar to the double pair, however the only numbers that can be involved are 1 and 10.
Examples:

1, 1, 10, 10     
1, 10, 1, 10    
**No other possibilites to get the Jospel exist!**
