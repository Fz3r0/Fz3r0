
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Configure IOS Initial Settings & Restore to Factory Defaults like a Sir! 

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Initial Settings` `Reset` `Flash`

---

### Recovering from System Crash, Reboot Init setup, etc


---

### The boot system Command 

- The switch attempts to automatically boot by using information in the BOOT environment variable. 

    - If this variable is not set, the switch attempts to load and execute the first executable file it can find.

    - On Catalyst 2960 Series switches, **the image file is normally contained in a directory that has the same name as the image** file _(excluding the .bin file extension)_.

- The IOS operating system then initializes the interfaces using the Cisco IOS commands found in the startup-config file. 
 
- **The `startup-config` file is called `config.text` and is located in `flash`.**

### Example:

- Notice that the IOS is located in a distinct folder and the folder path is specified. 

- Use the command **`show boot`** to see what the current IOS boot file is set to:

```

Switch> enable
Switch#
Switch# show boot
BOOT path-list      : 
Config file         : flash:/config.text    <<<-------| HERE!!!!! ;) 
Private Config file : flash:/private-config.text
Enable Break        : no
Manual Boot         : no
HELPER path-list    : 
Auto upgrade        : yes
NVRAM/Config file
      buffer size:   65536
Switch#

```

- Use **`dir flash:`** to do a ls/dir on the flash 

```

Switch#dir flash:
Directory of flash:/

    3  -rw-   505532849          <no date>  cat3k_caa-universalk9.16.03.02.SPA.bin  <<<-----| The IOS file name!!! :D

1539575808 bytes total (1034042959 bytes free)
Switch#

```

- Now that we know which IOS file we want to choose _(in this example there's just 1)_ we can select in and reboot from it!

- For example, if you load a new .bin and we want to reboot form that binary , just paste that file name and boot from there: 

**- HINT: Paste it twice :)!!!** The first is the directory (without .bin) the second is the file name:
        - `**cat3k_caa-universalk9.16.03.02.SPA/cat3k_caa-universalk9.16.03.02.SPA.bin**`

- Shake your Boot it!:

```

Switch(config)# boot system flash:/cat3k_caa-universalk9.16.03.02.SPA/cat3k_caa-universalk9.16.03.02.SPA.bin

```

| **Command**                      | **Definition**               |
|:--------------------------------:|:----------------------------:|
| boot system                      | The main command             |
| flash:                           | The storage device           |
| c2960-lanbasek9-mz.150-2.SE/     | The path to the file system  |
| c2960-lanbasek9-mz.150-2.SE.bin  | The IOS file name            |


---

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
