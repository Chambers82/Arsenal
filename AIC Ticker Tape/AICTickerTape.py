import Tkinter as tk

root = tk.Tk()
root.geometry("420x40+30+90")
deli = 100           # milliseconds of delay per character
svar = tk.StringVar()
labl = tk.Label(root, textvariable=svar, height=2, fg="green", bg="black", font=("Helvetica", 16))

def shif():
    shif.msg = shif.msg[1:] + shif.msg[0]
    svar.set(shif.msg)
    root.after(deli, shif)

shif.msg = ' Is this an alert or what?'
shif()
labl.grid(column=1, row=1, sticky='E'+'W')
root.mainloop()
