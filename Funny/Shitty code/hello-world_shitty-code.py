# Easter egg: Can you find the hidden message?
# ( Hint: Look for the comments that are not really comments )

this_is_a_variable_that_does_nothing = None  # Not used anywhere, but
looks important

def a_function_with_a_very_long_name_that_does_something_simple():
    """
    This function does something very complex... or does it?
    """
    # Comment that says nothing
    pass  # Do nothing, but take up space
    
    try:
        # Attempt to do something, but fail
        exec("print('Hello World!')")
        
    except Exception as e:
        # Catch the exception, but ignore it
        this_is_another_variable_that_does_nothing = str(e)  # Unused
variable
        
    finally:
        # Do something regardless of what happened
        __this_is_a_hidden_variable__ = "You will never find me!"  #
Hidden message
        
    if False:  # Never true, but looks like it might be
        # Code that is never executed, but takes up space
        print("This will never happen")
        
    elif True:  # Always true, but unnecessary
        # Do something, but in a very convoluted way
        lambda x: print(x) if x == "hello world!" else None  # Unused
lambda function
        
    else:
        # Code that is never executed, but looks important
        this_is_yet_another_variable_that_does_nothing = "Meaningless 
string"  # Unused variable

# Call the function, but with unnecessary complexity
a_function_with_a_very_long_name_that_does_something_simple.__getattribute_complexitya_function_with_a_very_long_name_that_does_something_simple.__getattribute__("__call__")()

# Easter egg: Can you find the hidden message?
# ( Hint: Look for the comments that are not really comments )
