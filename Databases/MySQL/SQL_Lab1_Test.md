
---

## Crear y eliminar `DB`

- Crear una `database` llamada `fz3r0_test01`_

    - `create database fz3r0_test01;`
    
    - ![image](https://user-images.githubusercontent.com/94720207/171761907-50f7878d-f19c-4a2d-bfd3-52a91308f4d5.png)

    - ![image](https://user-images.githubusercontent.com/94720207/171762049-837d103b-b298-4880-ae18-4f58eaf2c17f.png)

- Elimina `database` llamada `test`

    - `drop database fz3r0_test01`

- Nota: Meq uedaré al final con una DB llamada `fz3r0_db666`

## Crear y eliminar `Tablas`

1. Lo primero que se debe hacer es indicar la DB que se está utilizando:

    - `use fz3r0_test01;`

2. Después ya puedo crear una tabla (dentro de los paréntesis irán los nombres de los `campos` y `tipo de dato`):

    - [MySQL Datatypes](https://www.w3schools.com/mysql/mysql_datatypes.asp)

    - HINT: `id` siempre será `integer`

        - `create table Usuario(id int, email varchar(255), username varchar(50));`

    - Ejecutar y refrescar:
    
        - ![image](https://user-images.githubusercontent.com/94720207/171762888-df585a5b-86d9-46e6-a57d-3bf6e61db093.png)
        - ![image](https://user-images.githubusercontent.com/94720207/171762950-2af9c67b-ad87-4cf0-b3c9-cc81405f4c8c.png)

    - Ejemplo de selección de campo:
    
        - ![image](https://user-images.githubusercontent.com/94720207/171763105-f86db80b-4854-4521-9e56-b4427ecbaae4.png)

    - Ejemplo 2, utilizando Table inspector:
    
        - ![image](https://user-images.githubusercontent.com/94720207/171763337-7ecc5feb-7afe-43a1-8b98-e57ed6aba23a.png)
        - ![image](https://user-images.githubusercontent.com/94720207/171763390-c79043d0-6be8-4f32-976e-c427c18d325e.png)
        
- Para borrar la tabla solo se utiliza `drop` justo como con la `db`

    - `drop table Usuario`

## Alter Table

- Se utiliza para actualizar los `campos` de las tablas, agregarlos o quitarlos

- Agregar un campo `edad` a la tabla `usuario`:

    - `alter table Usuario add edad int;`

    - `alterar > tabla > Usuario > Agregar > Campo(edad) {tipo entero}`
    
    - ![image](https://user-images.githubusercontent.com/94720207/171767890-6fb80d4e-bb70-4513-88a7-c0e2ffc624ea.png)

- Quitar un campo

    - `alter table Usuario drop column edad;`
    
    - `alterar > tabla > Usuario > Quitar > Columna(edad)

- Modificar tipo de dato en una columna

    - `alter table Usuario modify column email varchar(50);` 
    
    - ![image](https://user-images.githubusercontent.com/94720207/171768256-be494e2a-8cf2-479a-abe8-b98393bcf60e.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/171768299-502d0d8c-b196-4ddc-81c9-726153e9c2fe.png)

## Instrucción `Insert` 

- Insertar `valores` dentro de los `campos` correspondientes en una `tabla`

    - `insert into usuario (email, username) values ('fz3r0@protonmail.com', 'fz3r0');`
    
    - insertar > dentro de > tabla(usuario) > en los campos(email, username) > los valores(fz3r0@protonmail.com, fz3r0)

- Modo alterno:

```sql
insert into usuario (email, username) 
values ('fz3r0@protonmail.com', 'fz3r0');
```

- ![image](https://user-images.githubusercontent.com/94720207/171960070-12de0359-7423-48f3-8d40-277c57202594.png)

- ![image](https://user-images.githubusercontent.com/94720207/171960215-855653d0-bcb0-453a-b55c-893af66769cb.png)

    - OJO!!! Recordar el ID!!! Para eso, podemos usar el `update` ;) Pero antes...
    
    - Así es como se borraría un campo donde específicamente se le proporciona una condición con `where`

```sql
delete from usuario where email = 'fz3r0@protonmail.com';
```
- borrar > (cualquier campo) de usuario(tabla) > donde el email(valor) sea > fz3r0@protonmail.com

- ![image](https://user-images.githubusercontent.com/94720207/171966434-aab2da75-ad7f-4876-8153-9fbc87f99087.png)

    - , habría una paradoja en el campo incremental, así que para poderlo borrar hay que usar `limit 1`:

```sql
delete from usuario where email = 'fz3r0@protonmail.com' limit 1;
```

- Ahora si dejaría crear una `primary key`:

    - ![image](https://user-images.githubusercontent.com/94720207/171967263-bac8e5a5-c979-4169-8df0-3e63f4eabc32.png) 

## Crear ID o `Primary Key`

- Para agregar la `primary key` igual se puede utilizar el comando `alter` de la siguiente manera:

```sql
alter table usuario add primary key (id);
```
- `alterar > tabla(usuario) > agregar > llave primaria(nombre: id)`

- ![image](https://user-images.githubusercontent.com/94720207/171966854-50aaf52c-3701-4620-b160-d1023a708ca9.png)

    - OJO! En caso de ver ese error, leer de nuevo arriba, es porque la tabla aún tiene algún campo con el id en null, en caso contrario ya la dejaría crear y se vería así:

    - ![image](https://user-images.githubusercontent.com/94720207/171967263-bac8e5a5-c979-4169-8df0-3e63f4eabc32.png) 

- Ahora ya también se puede modificar este campo para que sea autoincremental automaticamente. 

```sql
alter table usuario modify column id int AUTO_INCREMENT;
```  
- `alterar > tabla(usuario) > modificar > columna(id) con > Tipo de Dato(Entero) > Autoincremental`

- Antes del comando:

    - ![image](https://user-images.githubusercontent.com/94720207/171966772-e5fb9189-1ca3-418f-8b91-18979ccf25c8.png)

- Después del comando: 

    - ![image](https://user-images.githubusercontent.com/94720207/171967529-7b91bde4-61ee-4ddc-8f43-484a3e41fe98.png)
 
- Listo! Tengo la `primary key` establecida de porfa `autoincremental`, ahora ya podría ir agregando campos y que el `id` se genere automaticamente.

- Ahora si yo agrego campos, no importa que me falte alguno (como edad), lo importante es que ya todos llevarán su `id` o `primary key` automáticmanete de manera incremental, fácil, rápido y así nunca se repetirá:

    - ![image](https://user-images.githubusercontent.com/94720207/171967910-de1e37da-37fa-4ac0-80ff-1adb051b4341.png)

- Por ejemplo, un comando donde si llene todos los campos:

```sql
insert into usuario (email, username, edad) 
values ('anon@protonmail.com', 'An0n', 88);
```

- ![image](https://user-images.githubusercontent.com/94720207/171968138-41462e1f-e703-420b-9303-88a86d8b9ad5.png)

- Pero quedó una edad vacía, hay manera de agregar esa edad faltante con `update:`

## Instrucción `update`

- Si yo quisiera actualizar un campo o una tabla (por ejemplo `edad`) se puede utilizar `update` por ejemplo:

    - ![image](https://user-images.githubusercontent.com/94720207/171969861-c414fb4d-1317-4f0f-92a9-1f34328c3cdd.png)

```sql
update fz3r0_test01.usuario set edad = 18 where (id = '1');
update fz3r0_test01.usuario set edad = 88 where (id = '2');
```

- Tip: Esto también se puede hacer desde el workbench:

    - ![image](https://user-images.githubusercontent.com/94720207/171970002-00c07aa6-796e-4a31-bb02-6d6983891b45.png)

    - ![image](https://user-images.githubusercontent.com/94720207/171970021-ba9c777f-b2a9-4d95-925e-eb9665a69616.png)

- Otro ejemplo de `update` con la tabla mas grande:

    - ![image](https://user-images.githubusercontent.com/94720207/171971564-3e9ad444-01a6-47fc-8f85-e780420318eb.png)
    
    - En este ejemplo usaré el nombre + id, esto debido al candado de seguridad donde forzosamente debería ingresar un campo único, por ejemplo la `primary key` que sería lo mejor para actualizar `registros`

```sql
update usuario set edad = 32 where username = 'Neo' and id = '4';
```
- ![image](https://user-images.githubusercontent.com/94720207/171971805-bc2021d9-25f3-4240-87ff-40a42e3c263a.png)

- :bulb: **NOTA CRÍTICA: LA INSTRUCCIÓN `UPDATE` >> SIEMPRE << DEBE TENER UN `WHERE` PARA NO GENERAR ERRORES**

## Instrucción `where`

- Sirve para filtrar cuando queremos buscar algo con ciertas condiciones.

    - `*` = todo

    Ejemplos:

```sql
select * from usuario;
```
- `seleccionar > todo(*) > de > tabla(usuario)`

    - ![image](https://user-images.githubusercontent.com/94720207/171970132-5f291e39-56e9-457e-a7e8-eb93ab24dae0.png)

- En este caso me regresó TODO, pero que pasaría si yo quiero filtrar?:

```sql
select * from usuario where email = 'anon@protonmail.com';
```

- ![image](https://user-images.githubusercontent.com/94720207/171968264-48f00a70-f4d9-4a88-b023-85886ab14473.png)

- Otro filtro muy útil es agregar `where` donde se especifiquen 2 campos diferentes (o más), 

    - Por ejemplo:

```sql
select * from usuario where edad < 100 and edad > 18;
```

- ![image](https://user-images.githubusercontent.com/94720207/171971498-e9d94ba1-8859-46b5-a679-639b9d8bef07.png)

## Instrucción `delete`

- Ya sabemos hasta el momento como crear, modificar o actualizar `registros` dentro de los `campos` 

- Ahora solo falta aprender a borrarlos con el comando `delete` 

```sql
delete from usuarios where id = '1'
```
- ![image](https://user-images.githubusercontent.com/94720207/171972040-6963587f-fb8d-4116-bc03-3ec09bcab4cb.png)

- :bulb: **NOTA CRÍTICA: LA INSTRUCCIÓN `DELETE FROM` >> SIEMPRE << DEBE TENER UN `WHERE` PARA NO DESTRUIR LA DB!!!**

---

- Y básicamente eso es lo básico de lo basic, ahora ya sabes MySQL, que fácil! :D













 

 


     
