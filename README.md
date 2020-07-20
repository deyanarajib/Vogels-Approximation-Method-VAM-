# Vogels-Approximation-Method--VAM-
 A method for solving Transportation Problem

Vogel's Approximation Method (VAM) or penalty method
This method is preferred over the NWCM and VAM, because the initial basic feasible solution obtained by this method is either optimal solution or very nearer to the optimal solution.
Vogel's Approximation Method (VAM) Steps (Rule)
Step-1:	Find the cells having smallest and next to smallest cost in each row and write the difference (called penalty) along the side of the table in row penalty.
Step-2:	Find the cells having smallest and next to smallest cost in each column and write the difference (called penalty) along the side of the table in each column penalty.
Step-3:	Select the row or column with the maximum penalty and find cell that has least cost in selected row or column. Allocate as much as possible in this cell.
If there is a tie in the values of penalties then select the cell where maximum allocation can be possible
Step-4:	Adjust the supply & demand and cross out (strike out) the satisfied row or column.
Step-5:	Repeact this steps until all supply and demand values are 0.

Source: https://cbom.atozmath.com/example/CBOM/Transportation.aspx?he=e&q=vam
