from Tkinter import Canvas


class View(Canvas):

    FUEL_ACTIVE = 0
    TERRAIN_ACTIVE = 1
    IGNITIONS_ACTIVE = 2
    SIMULATION_ACTIVE = 3

    DEFAULT_FUEL_COLOR_MAP = {
                              0: (0, 0, 0),
                              1: (0, 0, 0),
                              2: (0, 0, 0),
                              3: (0, 0, 0),
                              4: (0, 0, 0),
                              5: (0, 0, 0),
                              6: (0, 0, 0),
                              7: (0, 0, 0),
                              8: (0, 0, 0),
                              9: (0, 0, 0),
                              10: (0, 0, 0)
                            }

    def __init__(self, master, width, height,
                 fuel_color_map=DEFAULT_FUEL_COLOR_MAP):
        Canvas.__init__(self, master=master, width=width, height=height)
        self.height = height
        self.width = width
        self.fuel_color_map = fuel_color_map
        self.active_part = View.FUEL_ACTIVE
        self.is_view_changed = False
        self.fuel_model = None
        self.terrain_model = None
        self.ignition_model = None

    def add_fuel_model(self, fuel_model):
        self.fuel_model = fuel_model

    def add_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model

    def add_ignition_model(self, ignition_model):
        self.ignition_model = ignition_model

    def activate_fuel_view(self):
        self.active_part = View.FUEL_ACTIVE

    def activate_terrain_view(self):
        self.active_part = View.TERRAIN_ACTIVE

    def activate_ignition_view(self):
        self.active_part = View.IGNITIONS_ACTIVE

    def activate_simulation_view(self):
        self.active_part = View.SIMULATION_ACTIVE

    def refresh_canvas(self):
        if self.active_part == View.SIMULATION_ACTIVE:
            self.__draw_simulation()
        else:
            if self.is_view_changed:
                if self.active_part == View.FUEL_ACTIVE:
                    self.__draw_fuel_model()
                elif self.active_part == View.TERRAIN_ACTIVE:
                    self.__draw_terrain_model()
                else:
                    self.__draw_ignition_model()

    def __draw_simulation(self):
        pass

    def __draw_fuel_model(self):
        pass

    def __draw_terrain_model(self):
        pass

    def __draw_ignition_model(self):
        pass
