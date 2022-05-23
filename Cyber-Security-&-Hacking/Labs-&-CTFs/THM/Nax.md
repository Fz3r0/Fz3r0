
---

### Intro 

- Identify the critical security flaw in the most powerful and trusted network monitoring software on the market, that allows an user authenticated execute remote code execution.


---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169726245-930ee2ff-9fd8-4430-8dbf-2a084d88db97.png)

- `furious -s connect -p 1-65535 $ip_target | tee 1___recon_furious_allports_Nax.txt`

    - ![image](https://user-images.githubusercontent.com/94720207/169726524-ad585a9f-af3a-43ae-976d-a1d9c54943c1.png)

- `nmap -sV -sC --min-rate 5000 --max-rtt-timeout 1500ms $ip_target -o 1___enum_nmap_ALLPORTS.txt`

    - ![image](https://user-images.githubusercontent.com/94720207/169726635-5a8016e4-d7dd-41a6-bc96-888f73bf7973.png)

---

### Services Enummeration

- 

---


---

### References

- https://tryhackme.com/room/nax
