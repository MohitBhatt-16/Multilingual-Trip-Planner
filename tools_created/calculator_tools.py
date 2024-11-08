from langchain.tools import tool

class CalculatorTools():

   @tool("Make a Mathematical Calculation")  # Anytime you want to make a function accessible to the crew 
   ## what you need to do is go of and add the tool decorator 
   def calculate(operation):
        """Useful to perform any mathematical calculations,
        like addition, subtraction, multiplication, division, etc.
        The input to this tool should be a mathematical
        expression, a couple of examples are '200*7' or '5000/2*5
        """

        try:
            return eval(operation)
        except SyntaxError:
            return "Error: Invalid syntax in mathematcal expression"

# The above way is very simple and not robust we can make a more robust tool using pydantic
# from pydantic import BaseModel, Field
# from langchain.tools import tool

# # Define a Pydantic model for the tool's input parameters
# class CalculationInput(BaseModel):
#     operation: str = Field(..., description="The mathematical operation to perform")
#     factor: float = Field(..., description="A factor by which to multiply the result of the operation")

# # Use the tool decorator with args_schema parameter pointing to the pydantic model
# @tool("perform_calculation",args_schema=CalculationInput,return_direct=True)
# def perform_calculation(operation: str, factor: float) -> str:
#     """
#     Performs a specified mathematical operation and multiples the result by a given factor.
    
#     Parameters:
#     - operation (str): A string representing a mathematical operation (eg, "10+5")
#     - factor (float): A factor by which to multiply the result of the operation.
    
#     Returns:
#     - A string representation of the calculation result.
#     """
#     # Perform the Calculation
#     result = eval(operation) * factor

#     # Return the result as a string
#     return f"The result of '{operation}' multiplied by {factor} is {result}"