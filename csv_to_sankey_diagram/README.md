# CSV Account Transactions to Sankey Diagram

This script takes in a csv file and allows the generation of a Sankey diagram.

First read in bank csv file for (yearly) transactions.

You will need to manually add 1. your starting balance to the CSV with the category "Initial Year Balance", and your line-by-line committed funds with negative dollar values with the category "Committed Expense". All other categories and values are automatically sorted into expense and revenue.


An example csv file is provided for demonstration.
