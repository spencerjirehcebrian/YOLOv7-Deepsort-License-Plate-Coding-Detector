def first_function():
    print("This is the first function")

    def inner_function():
        print("This is the inner function of the first function")

    return inner_function  # Return the inner function

def second_function():
    print("This is the second function")
    
    # Call the inner function of the first function
    inner_func = first_function()
    inner_func()  # Call the returned inner function

# Call the second function
second_function()
