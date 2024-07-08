# Find The Easy Pass
Date: 2024-07-08

## Static Analysis
First, I gathered some basic information about the executable using the file command:

```bash
└─# file EasyPass.exe 
EasyPass.exe: PE32 executable (GUI) Intel 80386, for MS Windows, 8 sections
```

This output indicated that EasyPass.exe is a 32-bit executable for Windows.

Next, I used the strings command to extract readable text strings from the executable:

```bash
└─# strings -a EasyPass.exe
```

Among the extracted strings, I found the following significant keywords:

```plaintext
...
Button1Click
...
Good Job. Congratulations
Wrong Password!
...
```

However, no additional useful information was found through static analysis alone.

## Dynamic Analysis
I then proceeded with dynamic analysis using **OllyDbg**. My goal was to locate the password validation logic. Here's a step-by-step summary of my process:

1. Initial Search:

    * I searched for the keyword **Password** within OllyDbg, which helped me quickly locate the relevant function responsible for password verification.
2. First Method: **NOP Assembly Code**:

    * I identified a conditional jump (JNZ) instruction before the success message ("Good Job. Congratulations."). The JNZ instruction would jump to the address 00454144, which contains the "Wrong Password!" message.
    * By replacing the JNZ instruction with NOP (No Operation) instructions, the program would no longer jump to the failure message, thus always displaying the success message.
    * After modifying the code, running the executable confirmed that the success message was shown regardless of the entered password.
3. Second Method: Breakpoint and Register Analysis:

    * I set a breakpoint at the address 00454131, where a function call was made.
    * Running the executable and stepping into the function, I observed the value of the EDX register, which was set to fortran!.
    * The program then compared the value in the EAX register (the password entered by the user) with the value in the EDX register (the hardcoded password).
    * Entering **fortran!** as the password resulted in the success message being displayed.

I successfully obtained the flag.

