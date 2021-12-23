import numpy as np, tkinter.ttk as ttk

def ndarray_image(arr):
    y, x = arr.shape
    data = f'P5 {x} {y} 1 '.encode() + arr.astype(np.uint8).tobytes()
    return ttk.tkinter.PhotoImage(width=x, height=y, data=data, format='PPM')

class ArrayView:

    def __init__(self, master, arr, zoom):
        self.array = arr
        self.zoom = zoom
        self.canvas = ttk.tkinter.Canvas(
            master, bg='#272822',
            width=arr.shape[1]*zoom,
            height=arr.shape[0]*zoom)
        self.img = ndarray_image(arr).zoom(zoom)
        self.cvimg = self.canvas.create_image(
            0, 0, anchor='nw', image=self.img)

    def update(self):
        self.img = ndarray_image(self.array).zoom(self.zoom)
        self.canvas.itemconfig(self.cvimg, image=self.img)

def default_style(master):
    style = ttk.Style(master)
    style.configure('TButton', foreground='black', font=('Helvetica', 15, 'bold'))
    style.configure('TRadiobutton', foreground='white', background='#272822')
    style.configure('TCheckbutton', foreground='white', background='#272822')
    style.configure('TLabel', anchor='center', justify='center')
    style.configure('A.TFrame', background='#272822')
    style.configure('B.TFrame')
    style.configure('.', font=('Helvetica', 13))
    return style
