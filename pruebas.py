import re
linea = "def foo(i:int):"
partes = re.findall(r'\b\w+\b|[^\w\s]|\s+', linea)
print(partes)