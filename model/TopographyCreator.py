from Tkinter import *
import tkFileDialog


class TopographyCreator(Frame):

    WIDTH_TEXT = 'width: '
    HEIGHT_TEXT = 'height: '
    BRUSH_SIZE_SLIDE_TEXT = 'brush size (1-200): '
    BRUSH_INTENSITY_TEXT = 'brush intensity (1-200)'
    MAX_TEXT = 'max value'
    MIN_TEXT = 'min value'
    BRUSH_SHAPE_CHOOSER_TEXT = 'Choose brush shape (circular or square): '
    CIRCULAR_SHAPE_TEXT = 'circular'
    SQUARE_SHAPE_TEXT = 'square'

    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.fake_label0 = Label(self, text='').grid(row=0, column=0)
        self.width_label = Label(self, text=TopographyCreator.WIDTH_TEXT)
        self.height_label = Label(self, text=TopographyCreator.HEIGHT_TEXT)
        self.width_label.grid(row=1, column=0)
        self.height_label.grid(row=2, column=0)
        self.width_entry = Entry(self)
        self.height_entry = Entry(self)
        self.width_entry.grid(row=1, column=1)
        self.height_entry.grid(row=2, column=1)
        self.fake_label1 = Label(self, text='').grid(row=3, column=0)
        self.brush_slider_label = Label(self, text=TopographyCreator.BRUSH_SIZE_SLIDE_TEXT)
        self.brush_size_scale = Scale(self, from_=1, to=200, orient=HORIZONTAL)
        self.brush_slider_label.grid(row=4, column=0, columnspan=2)
        self.brush_size_scale.grid(row=5, column=0, columnspan=2)
        self.fake_label2 = Label(self, text='').grid(row=6, column=0)
        self.brush_intensity_label = Label(self, text=TopographyCreator.BRUSH_INTENSITY_TEXT)
        self.brush_intensity_scale = Scale(self, from_=1, to=200, orient=HORIZONTAL)
        self.brush_intensity_label.grid(row=7, column=0, columnspan=2)
        self.brush_intensity_scale.grid(row=8, column=0, columnspan=2)
        self.fake_label3 = Label(self, text='').grid(row=9, column=0)
        self.max_label = Label(self, text=TopographyCreator.MIN_TEXT)
        self.min_label = Label(self, text=TopographyCreator.MAX_TEXT)
        self.min_label.grid(row=10, column=0)
        self.max_label.grid(row=11, column=0)
        self.min_entry = Entry(self)
        self.max_entry = Entry(self)
        self.min_entry.grid(row=10, column=1)
        self.max_entry.grid(row=11, column=1)
        self.fake_label4 = Label(self, text='').grid(row=12, column=0)
        self.max_label = Label(self, text=TopographyCreator.MIN_TEXT)
        self.max_label = Label(self, text=TopographyCreator.MIN_TEXT)
        self.min_label = Label(self, text=TopographyCreator.MAX_TEXT)
        self.min_label.grid(row=13, column=0)
        self.max_label.grid(row=14, column=0)
        self.max_label.grid(row=15, column=0)

root = Tk()
main = TopographyCreator(root)
root.mainloop()









'''
root = Tk()

root.title("Simple Graph")

root.resizable(0, 0)

points = []

spline = 0

tag1 = "theline"


def point(event):
    c.create_oval(event.x, event.y, event.x + 1, event.y + 1, fill="black")
    points.append(event.x)
    points.append(event.y)
    return points


def canxy(event):
    print event.x, event.y


def graph(event):
    global theline
    c.create_line(points, tags="theline")


def toggle(event):
    global spline
    if spline == 0:
        c.itemconfigure(tag1, smooth=1)
        spline = 1
    elif spline == 1:
        c.itemconfigure(tag1, smooth=0)
        spline = 0
    return spline


c = Canvas(root, bg="white", width=300, height=300)

c.configure(cursor="crosshair")

c.pack()

c.bind("<Button-1>", point)

c.bind("<Button-3>", graph)

c.bind("<Button-2>", toggle)

root.mainloop()
'''
