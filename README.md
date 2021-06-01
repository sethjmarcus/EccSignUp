# DEPRECATED

## No longer needed as there is no more sign ups for minyanim at the ECC.

# What is this?

Script for the signup system at the YIWH ECC Minyan.

# What does this do?

1. Import the csv file

2. Discard rows that did not contain "ECC" in the Item column

3. Discard rows that had blanks / nulls in BOTH First name AND Last name

4. Discard Mincha and Maariv, keeping only Shacharit and Kabalat Shabbat

5. Added two columns - Display name (First Name & " " & Last Name), and Seats (Number Sitting Together + 1)

6. Selects the data

7. For the Friday night list:
   1. Select Display Name where SIgnup = Men and Item = Kabalat Shabbat Order By Last Name
   2. I don't care about number of seats for Friday night
8. For Saturday Men and Women:
   1. Select Display Name where SIgnup = Men and Item = Shacharit Order By Last Name
   2. Select Display Name where SIgnup = Women and Item = Shacharit Shabbat Order By Last Name
9. But now, you also need to get the counts of pods. That is left as an exercise to the reader, but I need something like this:
   1. In addition to the counts, I need the Display name where the seat size >= 4 (for either men or women, last week there were no women with large pods)

## Output

The output is a .xlsx file (as the user properly passed in) with 6 worksheets in the workbook. What you do with it, I really don't care.

# How to use this

Assuming you know how to run a python script:

- The first argument is the input file. Provide the absolute path.
- The second argument is the output file (.xlsx). You *must* include the file type (.xlsx)
