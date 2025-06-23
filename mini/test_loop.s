.text
.global _start

main:
    stp fp, lr, [sp, #-16]!
    mov fp, sp

    mov sp, fp
    ldp fp, lr, [sp], #-16
    ret

_start:
    bl main
    ldr w8, =93
    svc #0
