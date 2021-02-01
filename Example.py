from MSLLib.MSL import run
run("""
COM This is a simple calculator

COM Take user input for the math
GET math Type the math equasion you want to solve: 

COM Calculate the equasion and store it in the "$&maths" variable
CAL outmath $&math

COM Print the equasion and the answer
PRL $&math = $&outmath!
""")