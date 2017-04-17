from Tkinter import *
import tkFileDialog
import views


class SimulationController(Frame):

    ADD_FUEL_MODEL_TEXT = 'add fuel model'
    ADD_TERRAIN_MODEL_TEXT = 'add terrain model'
    ADD_IGNITION_MODEL_TEXT = 'add ignition model'

    def __init__(self, master, canvas_height, canvas_width,
                 legend_height, legend_width):
        Frame.__init__(self, master)
        self.grid()
        self.map_view = views.MapView(self, canvas_width, canvas_height,
                                      500, 500)
        self.legend_view = views.LegendView(self, legend_width, legend_height)
        self.map_view.grid(row=0, column=1, rowspan=3)
        self.legend_view.grid(row=0, column=2, rowspan=3)
        self.add_fuel_model_button = Button(self, text=SimulationController.ADD_FUEL_MODEL_TEXT,
                                            command=self.__add_fuel_model)
        self.add_fuel_model_button.grid(row=0, column=0)
        self.add_terrain_model_button = Button(self, text=SimulationController.ADD_TERRAIN_MODEL_TEXT,
                                               command=self.__add_terrain_model)
        self.add_terrain_model_button.grid(row=1, column=0)
        self.add_ignition_model_button = Button(self, text=SimulationController.ADD_IGNITION_MODEL_TEXT,
                                                command=self.__add_ignition_model)
        self.add_ignition_model_button.grid(row=2, column=0)

    def __add_fuel_model(self):
        filename = tkFileDialog.askopenfilename()
        print 'fuel model: ' + filename + '  added...'

    def __add_terrain_model(self):
        filename = tkFileDialog.askopenfilename()
        print 'terrain model: ' + filename + '  added...'

    def __add_ignition_model(self):
        filename = tkFileDialog.askopenfilename()
        print 'ignition model: ' + filename + '  added...'

root = Tk()
main = SimulationController(root, 100, 100, 20, 100)
root.mainloop()




