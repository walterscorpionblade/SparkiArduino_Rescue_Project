import tkinter as tk

window = tk.Tk()
window.title('Sparki Arduino Visual Interface')
window.geometry('400x600')

#This is the direction control part
tk.Label(window, text='This is the sparki arduino direction control').place(x=5, y= 5)

left_control = tk.Button(window, text='Turn left') #, command=usr_login)
left_control.place(x=10, y=100)
right_control = tk.Button(window, text='Turn Right') #, command=usr_sign_up)
right_control.place(x=300, y=100)
forward_control = tk.Button(window, text='Move Forward') #, command=usr_login)
forward_control.place(x=145, y=70)
back_control = tk.Button(window, text='Move Back') #, command=usr_login)
back_control.place(x=145, y=140)

window.mainloop()