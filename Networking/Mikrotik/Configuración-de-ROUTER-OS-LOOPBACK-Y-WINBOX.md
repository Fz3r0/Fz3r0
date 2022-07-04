# Mikrotik - Mikrotik y Winbox en GNS3

## Start from 0

- Agregar el Mikrotik

![image](https://user-images.githubusercontent.com/94720207/177077961-1ad29cb1-3be1-4ad0-be86-74212e0bb248.png)

- Para lograr entrar a Mikro con Winbox lo que se debe hacer antes que nada es hacer una **Interfaz Loopback** en la máquina física, es decir, una interfaz virtual en nuestro Mikro (igual que cualquier loopback en router Cisco)

- Ingresar **COMO ADMIN** al `Loopback Manager`de Windows: 

- ![image](https://user-images.githubusercontent.com/94720207/177078845-be4220c2-228a-4511-bb8a-2922ca4bc8d6.png)

- ![image](https://user-images.githubusercontent.com/94720207/177078921-e2cd5cf6-819b-4022-a57e-96b94d5b51e4.png)

- ![image](https://user-images.githubusercontent.com/94720207/177079041-22c2f88c-6e7b-480d-8302-639d7b058012.png)

    - Se abrirá la siguiente pantalla:

- ![image](https://user-images.githubusercontent.com/94720207/177079083-b1c9ee84-4bdd-471d-822a-245241e2c001.png)

   - Elegir opción 2 "Install a new loopback interface"

- ![image](https://user-images.githubusercontent.com/94720207/177079250-37a47619-7f64-4cfa-beca-efe7dd1336c8.png)

- Asegurarnos que se creó el Loopback:

- Ir a Panel de Control > Redes de Internet > Centro de Redes y Recursos COmpartidos

    - ![image](https://user-images.githubusercontent.com/94720207/177083201-ae71248d-8ab9-4229-aeb0-6cab8b095c51.png)

- cambiar configuración del adaptador

    - ![image](https://user-images.githubusercontent.com/94720207/177083260-8e89da65-1815-41c2-bef9-a458dae38e52.png)

- Encontrar el Loopback creado:

    - ![image](https://user-images.githubusercontent.com/94720207/177083432-93b42bae-8a19-461f-9fa9-3fcdf9eba4dd.png)

- **Reiniciar computadora**

---

- Regresar al proyecto:

    - ![image](https://user-images.githubusercontent.com/94720207/177082980-6fd5eb37-24f2-4693-91fe-528dab680c57.png)

- Asignar una dirección a la Interfaz de Loopback

    - Seleccionar WiFi o Ethernet (Lo que estés usando en tu conexión en este momento, en mi caso es Ethernet1 mi salida a Internet)

    - ![image](https://user-images.githubusercontent.com/94720207/177083923-24b78a3a-3a08-45ab-8b4e-1d378d8f3f7d.png)

    - 








