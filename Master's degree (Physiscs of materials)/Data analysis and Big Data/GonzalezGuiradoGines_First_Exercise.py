"""
Objective: Create a matrix with a list comprehension and do some operations with rows and columns

Author: Ginés González Guirado

Date: 05/10/2021

"""

import random  # To introduce random values in the matrix

while True:  # Infinite loop that will keep running until the number of elements produces a square matrix
    # Get the number of elements from the user
    while True:  # Infinite loop that will keep running until the break
        try:  # The try block attempts to read and validate the user's input
            num_elements = int(input("Enter a positive number of elements to generate a matrix: ")) # the value introduced by the user is converted into an integer
            if num_elements > 0:
                break   # If the number of elements is more than zero, it gets out of the while loop
            else:  # If the number of elements is less than zero, it raises an error
                print("Please enter a positive integer for the number of elements.")
        except ValueError:  # If the user introduce something that can't be converted to an integer, it raise an error
            print("Invalid input. Please enter a valid integer for the number of elements.")

    # Calculate the size of the square matrix (the range of the matrix)
    matrix_size = int(num_elements ** 0.5)  # It converts the square root of the number of elements into a integer

    # Check if it's a square matrix
    if matrix_size * matrix_size == num_elements:
        # Create a 2D List (square matrix) with random values with a list comprehension
        matrix = [[random.randint(1, 100) for _ in range(matrix_size)] for _ in range(matrix_size)]  # I have used this _ because the index of the loop is not going to be used

        # Print the matrix
        print("Square Matrix:")
        for row in matrix:  # Loop to print the 2D list with the form of a matrix
            print(row)

        # Function to sum all the elements of a given row
        def sum_row_elements(matrix, row):
            if row < 0 or row >= matrix_size:  # An error raise if the row chosen by the user is not in the matrix
                return print("Invalid row. Please enter a number of row that is in the matrix.")
            return print("Sum of row {} is: {}".format(row, sum(matrix[row])))  # It gives the sum of a row of the matrix

        # Get the row from the user
        while True:  # Infinite loop that will keep running until the row will be in the matrix range
            try:  # The try block attempts to read and validate the user's input
                row = int(input("Enter the row to sum (0 to {}):".format(matrix_size - 1))) # the value introduced by the user is converted into an integer
                if 0 <= row < matrix_size:  # If the row is in the range of the matrix the loop while finish
                    break
                else:  # If the row is not in the range of the matrix, it raises an error
                    print("Invalid row. Please enter a valid row.")
            except ValueError:  # If the user introduce something that can't be converted to an integer, it raise an error
                print("Invalid input. Please enter a valid integer for the row.")

        sum_row_elements(matrix, row)  # Calling the function for the solution

        # Function to sum all the elements of a given column
        def sum_column_elements(matrix, column):
            if column < 0 or column >= matrix_size:   # An error raise if the column chosen by the user is not in the matrix
                return print("Invalid column. Please enter a number of column that is in the matrix.")
            else:  # Result if the column introduced is valid
                column_sum = []  # List to store the elements of the column that the user wants to sum
                for i in range(matrix_size):  # Loop to obtain the elements of the column that the user wants to sum
                    column_sum.append(matrix[i][column])  # An element of the column is added in the list column_sum every iteration
                return print("Sum of column {} is: {}".format(column, sum(column_sum)))  # It printsthe index of the column that is sumed and the sum

        # Get the column from the user
        while True:  # Infinite loop that will keep running until the column will be in the matrix range
            try:  # The try block attempts to read and validate the user's input
                column = int(input("Enter the column to sum (0 to {}):".format(matrix_size - 1)))  # the value introduced by the user is converted into an integer
                if 0 <= column < matrix_size:  # If the column is in the range of the matrix the loop while finish
                    break
                else:  # If the column is not in the range of the matrix, it raises an error
                    print("Invalid column. Please enter a valid column.")
            except ValueError:  # If the user introduce something that can't be converted to an integer, it raise an error
                print("Invalid input. Please enter a valid integer for the column.")

        sum_column_elements(matrix, column)  # Calling the function for the solution

        # Sum one by one all the elements of the fifth row with all the elements of the fifth column
        if matrix_size >= 5:  # To do this we need the matrix to have a range greater or equal to 5
            s5 = []  # Empty List in which the results of the sum will be saved
            for i in range(matrix_size):  # Loop to do the sum of the element of the row with the element of the column
                s5.append(matrix[4][i] + matrix[i][4])
            print("Sum one by one all the elements of the fifth row with all the elements of the fifth column:", s5)
        else:
            print("The matrix does not have enough rows and columns to perform this operation.")

        # Function that calculates the median of all the elements of a row of the matrix
        def median_row_elements(matrix, row):
            if row < 0 or row >= matrix_size:  # An error raise if the row chosen by the user is not in the matrix
                return print("Invalid row. Please enter a number of row that is in the matrix.")
            
            row_elements = matrix[row]  # Get the elements of the row
            sorted_row_elements = sorted(row_elements)  # Sort the elements in ascending order

            # Calculate the median based on the sorted elements
            length = len(sorted_row_elements)  # Length of the row, which is equal to the range of the matrix
            if length % 2 == 1:
                # If the number of elements is odd, return the middle element
                median = sorted_row_elements[length // 2]  # // integer division
            else:
                # If the number of elements is even, return the average of the two middle elements
                median = (sorted_row_elements[length // 2 - 1] + sorted_row_elements[length // 2]) / 2

            return median  #return the solution

        # Get the row from the user
        while True:  # Infinite loop that will keep running until the row will be in the matrix range
            try:  # The try block attempts to read and validate the user's input
                row = int(input("Enter the row to obtain its median (0 to {}):".format(matrix_size - 1)))  # the value introduced by the user is converted into an integer
                if 0 <= row < matrix_size:  # If the row is in the range of the matrix the loop while finish
                    break
                else:  # If the row is not in the range of the matrix, it raises an error
                    print("Invalid row. Please enter a valid row.")
            except ValueError:  # If the user introduce something that can't be converted to an integer, it raise an error
                print("Invalid input. Please enter a valid integer for the row.")

        # Calling the function for the solution
        result = median_row_elements(matrix, row)
        
        # Print the result
        print("Median of row {} is: {}".format(row, result))

        # Ask the user if they want to restart or exit the program
        restart = input("Do you want to restart the program? (yes/no): ").strip().lower()
        if restart != "yes":
            break  # Exit the loop if the user enters anything other than "yes"

    else:   # If number of elements does not form a square matrix,, it raises an error
        print("The provided number of elements does not form a square matrix. Please try again.")

