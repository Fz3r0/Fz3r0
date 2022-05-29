allá vamos!!!


## Python Intro

### Synthax

## Goodbye World

- Example

```py

    # This is a comment

print("I'm Fz3r0 and the sun no longer rises")

print("In the mist of the night...")     # This is a comment

"""
This is a comment
written in
more than just one line
"""

print("... you could see me come. ")
   
print()    # Print a blank new line "\n":    

```

## Python: Operators

### [Python Operators](https://www.w3schools.com/python/python_operators.asp)

- Python Arithmetic Operators
- Python Assignment Operators
- Python Comparison Operators
- Python Logical Operators
- Python Identity Operators
- Python Membership Operators
- Python Bitwise Operators

    - **Ejemplo:**

```py
    # Es importante hacer identación (4 espacios standard)
    
        # Ejemplo de un if donde la condición se cumple:

if 5 > 3:
    print('5 es mayor a 3')

        # Ejemplo de un if donde la condición NO se cumple:
        # (Debido a que no se cumple, no se imprime...)

if 5 < 3:
    print('5 es mayor a 3')
```

## Python: Variables

### [Python Variables](https://www.w3schools.com/python/python_variables.asp)

```py

# Variables do not need to be declared with any particular type, and can even change type after they have been set. 

x = 4           # x is of type "int"

x = "Sally"     # x is now of type "str"

print(x)

    # Casting:
    
    # If you want to specify the data type of a variable, this can be done with casting.
    
x = str(3)      # x will be '3'

y = int(3)      # y will be 3

z = float(3)    # z will be 3.0 

print(x)

print(y)

print(z)

    # Get the Type

    # You can get the data type of a variable with the type() function.

x = 5

y = "John"

print(x)

print(y)

print(type(x))

print(type(y))        

```

- ![image](https://user-images.githubusercontent.com/94720207/170892319-b32aa6a0-3a8f-4999-b7e1-25241330f119.png)

- Ejemplo 2:

```py

    # Imprimiendo más de una variable al mismo tiempo:

X = 100
Y = 200
Z = 'Fz3r0 is the King!'

print (X, Y, Z)

email = 'fz3r0@protonmail.com'

print (X, Y, Z, email)
```

- ![image](https://user-images.githubusercontent.com/94720207/170892331-fc951651-5e62-4b37-8380-1ccc6fb6d211.png)

    - **NOTA:** Las variables no pueden empezar con números (como en javascript u otros lenguajes)

### Múltiples variables en una sola línea

- También se pueden declarar variables utilizando una sola linea

    - Ejemplo:

```py

    # Declarando a, b y c en una misma linea
    
    # Las 3 variables resultarán con el mismo valor de "10"
    
a, b, c = 10 
    
    # Las 3 variables resultarán con el mismo valor de "fz3r0_string"
    
x, y, z = 'fz3r0_string'

print (a)
print (b)
print (c)

print()

print (x)
print (y)
print (z)

```

- ![image](https://user-images.githubusercontent.com/94720207/170892659-a4c9306f-b868-49c8-8852-45fa127526d1.png)



