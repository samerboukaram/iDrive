import os

a= """
print("hello world")
"""

os.system("""python3 -c '"""+ a + """'""")
os.system("""python3 -c 'print("hello world")'""")