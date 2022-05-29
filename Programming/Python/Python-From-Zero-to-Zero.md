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

### [<<< Python Operators >>>](https://www.w3schools.com/python/python_operators.asp)

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

### [<<< Python Variables >>>](https://www.w3schools.com/python/python_variables.asp)

- Variables are containers for storing data values.

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
    
    # # Las 3 variables resultarán con su respectivo valor según el orden (1º, 2º y 3º)
    
a, b, c = 10, 20, 30 
    
    # Las 3 variables resultarán con su respectivo valor según el orden (1º, 2º y 3º)
    
x, y, z = 'fz3r0_string_1', 'fz3r0_string_2', 'fz3r0_string_3', 

print (a)
print (b)
print (c)

print (a, b, c)

print()

print (x)
print (y)
print (z)

print (x, y, z)

```

- ![image](https://user-images.githubusercontent.com/94720207/170892659-a4c9306f-b868-49c8-8852-45fa127526d1.png)

- En caso de querer que las variables declaradas al mismo tiempo también tengan el mismo valor:

    - Ejemplo: 

```py

    # Declarando valor_1, valor_2 y valor_3 en una misma linea
    
    # # Las 3 variables resultarán con el mismo valor:
    
valor_1 = valor_2 = valor_3 = '<< Triforce - 3 variables tendrán este valor >>'  
    
    # Las 3 variables resultarán con el mismo valor (en este caso el string)
    
print (valor_1)
print (valor_2)
print (valor_3)

print (valor_1, valor_2)

```

- ![image](https://user-images.githubusercontent.com/94720207/170892834-42d96368-50f4-40c1-94b3-81342a06331c.png)

## Python String Concatenation 

### [<<< Python String Concatenation >>>](https://www.w3schools.com/python/gloss_python_string_concatenation.asp)

- String concatenation means add strings together.

    - Use the `+` character to **add a variable to another variable:**

```py
    # Sumare los strings "x" + "y"

x = "I am "
y = "Fz3r0"

z_f0 =  x + y

print(z_f0)

    # Creando espacios entre strings: 

    # Solo hay que sumar un blank: " "

a = "Soy"

b = "Fz3r0"

c_f0 = a + " " + b

print(c_f0) 
```

- ![image](https://user-images.githubusercontent.com/94720207/170893059-ca28988e-0f29-4bf9-bba3-31637c93b8fa.png)

## Python: Datatypes

### [<<< Python Datatypes >>>](https://www.w3schools.com/python/python_datatypes.asp)

- In programming, data type is an important concept.

- **Variables can store data of different types, and different types can do different things.**

    - **You can get the data type of any object by using the `type()` function:** 

```py

    # a = número entero
    
    # b = string
    
a = 5

b = 'fz3r0_string'

print(type(a))

print(type(b))

print()

    # Declarando tipo de dato e imprimiendo después:
    
x = str(3)      # x will be '3'

y = int(3)      # y will be 3

z = float(3)    # z will be 3.0   

print(type(x))

print(type(y))

print(type(z))
    
```

- ![image](https://user-images.githubusercontent.com/94720207/170893390-ac86c2ce-b5f0-4980-a706-2a23361eed10.png)

## Python Lists

### [<<< Python Lists >>>](https://www.w3schools.com/python/python_lists.asp)

- Lists are used to store multiple items in a single variable.

- Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are: 

    - **Tuple** 
    - **Set**
    - **Dictionary**

- _*all with different qualities and usage._

- **Lists are created using square brackets: `[]`**

```py

    # lista vacía:

lista_vacia = []

    # Creando una lista:

f0_lista = ["manzana", "banana", "mango"]

    # Imprimiendo la lista:

print(f0_lista)
```

- ![image](https://user-images.githubusercontent.com/94720207/170893706-6d0160d4-feec-410c-9974-c19bf3eeffa8.png)

- También se pueden manipular las listas utilizando los siguientes `métodos`:

1. **método** `.append` - Agregar datos a la lista

2. **método** `.clear` - Elimina TODOS los elementos la lista

3. **método** `.copy` - Copia los elementos DESDE una lista HACIA OTRA lista


```py

    # Creando una lista:

f0_lista_1 = [1, 2, 3]

f0_lista_2 = ['abc', 'string', 'Fz3r0']

    # Imprimiendo la lista creada:

print(f0_lista_1)
print(f0_lista_2)
print()

    # Agregando elementos a la lista usando "append":

f0_lista_1.append(4)

print(f0_lista_1)

f0_lista_2.append('Agregando strings eh?!')

print(f0_lista_2)
print()

    # Copiando lista 1 y lista 2 a nuevas variables:
    
666_lista_copia1 = f0_lista_1.copy
666_lista_copia2 = f0_lista_2.copy

print(f0_lista_1)
print(666_lista_copia1)

print(f0_lista_2)
print(666_lista_copia2)

    # Eliminando los datos de las primeras 2: (No se verán 4 en consola, sino solo 2)
    
f0_lista_1.clear
f0_lista_2.clear

print(f0_lista_1)
print(f0_lista_2)

print(f0_lista_2)
print(666_lista_copia2)

```

- ![image](https://user-images.githubusercontent.com/94720207/170893904-58552958-dca9-47b9-b9f1-c5c37b962cb4.png)





