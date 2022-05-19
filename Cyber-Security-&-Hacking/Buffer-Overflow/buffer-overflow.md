
### Intro

- Anatomy of the Memory
- Anatomy of the Stack
- Buffer Overflow Walkthrought

### Anatomy of Memory

![image](https://user-images.githubusercontent.com/94720207/169180891-ba8923c4-2493-4ec7-b1b9-00f7d41c9e7c.png)

- We will be focusing on the stack

### Anatomy of the Stack

![image](https://user-images.githubusercontent.com/94720207/169181017-6f10103d-2a74-4fc3-8019-c58f75f6c460.png)

- Buffer characters

![image](https://user-images.githubusercontent.com/94720207/169181180-421ba203-1f62-43f9-b4f8-a3e3f447bcd5.png)

- Buffer Overflow

    - Reaching the EBP & EIP:
      
![image](https://user-images.githubusercontent.com/94720207/169181279-72b722a1-fb3f-4e3b-af8f-e06b649d71d2.png)



### Steps to conduct a buffer overflow

1. Spiking
2. Fuzzing
3. Finding the Offset
4. Overwhelming the EIP
5. Finding Bad Characters
6. Finding the Right Module
7. Generating Shellcode
8. Root!



### References

- https://www.youtube.com/watch?v=qSnPayW6F7U&list=PLLKT__MCUeix3O0DPbmuaRuR_4Hxo4m3G
