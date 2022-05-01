
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Boot from a Binary .bin or config.text & Recover from a System Crash like a Sir!

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Initial Settings` `Reset` `Flash`

---

### Index

- Part1: << **Boot** from a **.bin initial configuration** | `boot system` command >>
- Part2: << **Recovering from a System Crash** | Step by step recover >>

---

### The `boot system` Command 

- **Before anything!** 

    - **This technique DOES NOT reset the device to factory settings like new & shiny**
    - **This is used to tell the router/switch which IOS file to be used while booting, when there are multiple files in the flash... So, if you have only 1 file, it will be your same config!!! (not the factory or other startup config)**
    - **This can also be used when a device crash (_See the second section of this document_) 
    - **If you have a backup or another .bin with an init setup stored in you device, then you can boot from there tho ;) (but there are other better ways to init the device from factory, just click here!!!)
    - **Another good use for this crap, is to boot from another disk or service outside the device like FTP, ROM, TFTP...**

- **...OK moving on...** 

- The switch attempts to automatically boot by using information in the BOOT environment variable. 

    - If this variable is not set, the switch attempts to load and execute the first executable file it can find.

    - On Catalyst 2960 Series switches, **the image file is normally contained in a directory that has the same name as the image, but sometimes are directly in `/` **

- The IOS operating system then initializes the interfaces using the Cisco IOS commands found in the startup-config file. 
 
- **The `startup-config` file is called `config.text` and is located in `flash`.**

### Example:

- Notice that the IOS is located in root `/` (flash:/) folder, but sometimes another folder path is specified (flash:/folderabcs_122345/). 

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
Directory of flash:/      <<<---------| in this case is directly in /

    3  -rw-   505532849          <no date>  cat3k_caa-universalk9.16.03.02.SPA.bin  <<<-----| The IOS file name!!! :D

1539575808 bytes total (1034042959 bytes free)
Switch#

```

- Now that we know which IOS file we want to choose _(in this example there's just 1)_ we can select in and reboot from it!

- For example, if you load a new .bin and we want to reboot form that binary , just paste that file name and boot from there: 

    - **HINT: Check the path!** if there's a folder, Paste it twice :)!!! The first is the directory (without .bin) the second is the file name:
    
    - **`flash:/cat3k_caa-universalk9.16.03.02.SPA/cat3k_caa-universalk9.16.03.02.SPA.bin`**

- **HINT: But sometimes is directly in /**

    - **`flash:/cat3k_caa-universalk9.16.03.02.SPA.bin`**
        
- Shake your Boot it!:
    
    - **`boot system flash:/cat3k_caa-universalk9.16.03.02.SPA/cat3k_caa-universalk9.16.03.02.SPA.bin`** 

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

### Recovering from a System Crash | Step by step recover

- The `boot loader` provides access into the switch if the operating system cannot be used because of missing or damaged system files.
 
- The `boot loader` has a command-line/shell that provides access to the files stored in flash memory.

- The trick to access that shell is easy, _(it's similar like booting another shell or BIOS on smartphone or any other device hehe)_

1. Connect a PC by console cable to the switch console port.

![image](https://user-images.githubusercontent.com/94720207/166128307-dc7dbbb9-dfd9-40a6-97c9-bcaccc6c7436.png)

2. Unplug the switch power cord. _(not allowed in all packet tracer devices, but, for example:)_

![image](https://user-images.githubusercontent.com/94720207/166128212-a954d668-bc73-4e50-8124-535cc33eb93a.png)

3. Reconnect the power cord to the switch and press and hold **within 15 seconds**, the `Mode` button while the System LED is still flashing green.

![image](https://user-images.githubusercontent.com/94720207/166128365-b4357dea-e673-4b02-a544-4d3575dd2edc.png)

4. Continue pressing the Mode button until the System LED turns briefly amber and then solid green; then release the Mode button.

![image](https://user-images.githubusercontent.com/94720207/166128407-256baee4-c342-4ab0-84af-68e224ccba47.png)

5. The boot loader switch: prompt appears in the terminal emulation software on the PC.

```

Switch>
Switch>         <<<------------| Normal prompt or shell (Switch>)
Switch>
Switch>C2950 Boot Loader (C2950-HBOOT-M) Version 12.1(11r)EA1, RELEASE SOFTWARE (fc1)
Compiled Mon 22-Jul-02 18:57 by miwang
Cisco WS-C2950T-24 (RC32300) processor (revision C0) with 21039K bytes of memory.
2950T-24 starting...
Base ethernet MAC Address: 000D.BDB8.0A1C
Xmodem file system is available.
Initializing Flash...
flashfs[0]: 1 files, 0 directories
flashfs[0]: 0 orphaned files, 0 orphaned directories
flashfs[0]: Total bytes: 64016384
flashfs[0]: Bytes used: 3058048
flashfs[0]: Bytes available: 60958336
flashfs[0]: flashfs fsck took 1 seconds.
...done Initializing Flash.

Boot Sector Filesystem (bs:) installed, fsid: 3
Parameter Block Filesystem (pb:) installed, fsid: 4


Loading "flash:/c2950-i6q4l2-mz.121-22.EA4.bin"...
###############
Boot process terminated.
switch: 
switch:         <<<------------| Boot loader!! ;) (Switch:)
switch: 

```

- Type the `help` or `?` at the boot loader prompt to view a list of available commands.

```
switch: 
switch: help
           ? -- Present list of available commands
        boot -- Load and boot an executable image
      delete -- Delete file(s)
         dir -- List files in directories
  flash_init -- Initialize flash filesystem(s)
        help -- Present list of available commands
      rename -- Rename a file
       reset -- Reset the system
         set -- Set or display environment variables
       unset -- Unset one or more environment variables
switch: 

```

- By default, the switch attempts to automatically boot up by using information in the BOOT environment variable. 

- To view the path of the switch BOOT environment variable type the `set` command. Then, initialize the flash file system using the `flash_init` command to view the current files in flash, as shown in the output.

```
switch: 
switch: set

////  (no output in this switch but you could find also:)  ///

BOOT=flash:/c2960-lanbasek9-mz.122-55.SE7/c2960-lanbasek9-mz.122-55.SE7.bin
(output omitted)

switch: flash_init
Initializing Flash...
flashfs[0]: 1 files, 0 directories
flashfs[0]: 0 orphaned files, 0 orphaned directories
flashfs[0]: Total bytes: 64016384
flashfs[0]: Bytes used: 3058048
flashfs[0]: Bytes available: 60958336
flashfs[0]: flashfs fsck took 1 seconds.
...done Initializing Flash.

switch:

```

- After flash has finished initializing you can enter the `dir flash:` command to view the directories and files in flash, as shown in the output.

```

switch: dir flash:
Directory of flash:/

1    -rw-  3058048   <date>               c2950-i6q4l2-mz.121-22.EA4.bin
60958336 bytes available (3058048 bytes used)

switch: 

```

- Enter the `BOOT=flash` command to change the BOOT environment variable path the switch uses to load the new IOS in flash. 

- To verify the new BOOT environment variable path, issue the `set` command again. 

- Finally, to load the new IOS type the `boot` command without any arguments, as shown in the output.

```

switch: BOOT=flash:c2950-i6q4l2-mz.121-22.EA4.bin
switch: set
BOOT=flash:c2950-i6q4l2-mz.121-22.EA4.bin
switch: boot

C2950 Boot Loader (C2950-HBOOT-M) Version 12.1(11r)EA1, RELEASE SOFTWARE (fc1)
Compiled Mon 22-Jul-02 18:57 by miwang
Cisco WS-C2950T-24 (RC32300) processor (revision C0) with 21039K bytes of memory.
2950T-24 starting...
(bla bla bla bla...)

```

---

### References

- https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/cisco-ios-boot-system-image-
- https://www.cisco.com/en/US/docs/switches/lan/catalyst4000/7.5/configuration/guide/boot_support_TSD_Island_of_Content_Chapter.html
---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
