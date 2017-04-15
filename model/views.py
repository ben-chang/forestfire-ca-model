from Tkinter import Canvas
import abc


class View(Canvas):

    __metaclass__ = abc.ABCMeta

    _FUEL_ACTIVE = 0
    _TERRAIN_ACTIVE = 1
    _IGNITIONS_ACTIVE = 2
    _SIMULATION_ACTIVE = 3

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
        self.active_part = MapView._FUEL_ACTIVE
        self.is_view_changed = False
        self.fuel_model = None
        self.terrain_model = None
        self.ignition_model = None

    @abc.abstractmethod
    def add_fuel_model(self, fuel_model):
        pass

    @abc.abstractmethod
    def add_terrain_model(self, terrain_model):
        pass

    @abc.abstractmethod
    def add_ignition_model(self, ignition_model):
        pass

    @abc.abstractmethod
    def activate_fuel_view(self):
        pass

    @abc.abstractmethod
    def activate_terrain_view(self):
        pass

    @abc.abstractmethod
    def activate_ignition_view(self):
        pass

    @abc.abstractmethod
    def refresh_canvas(self):
        pass

    @abc.abstractmethod
    def _draw_fuel_view(self):
        pass

    @abc.abstractmethod
    def _draw_terrain_view(self):
        pass

    @abc.abstractmethod
    def _draw_ignition_view(self):
        pass


class MapView(View):

    def __init__(self, master, width, height, legend_view,
                 fuel_color_map=View.DEFAULT_FUEL_COLOR_MAP,):
        View.__init__(self, master=master, width=width, height=height,
                      fuel_color_map=fuel_color_map)
        self.legend_view = legend_view

    @override
    def add_fuel_model(self, fuel_model):
        self.fuel_model = fuel_model
        self.legend_view.add_fuel_model(fuel_model)

    @override
    def add_terrain_model(self, terrain_model):
        self.terrain_model = terrain_model
        self.legend_view.add_terrain_model(terrain_model)

    @override
    def add_ignition_model(self, ignition_model):
        self.ignition_model = ignition_model
        self.legend_view.add_ignition_model(ignition_model)

    @override
    def activate_fuel_view(self):
        self.active_part = MapView._FUEL_ACTIVE
        self.legend_view.activate_fuel_view()

    @override
    def activate_terrain_view(self):
        self.active_part = MapView._TERRAIN_ACTIVE
        self.legend_view.activate_terrain_view()

    @override
    def activate_ignition_view(self):
        self.active_part = MapView._IGNITIONS_ACTIVE
        self.legend_view.activate_ignition_view()

    def activate_simulation_view(self):
        self.active_part = MapView._SIMULATION_ACTIVE

    @override
    def refresh_canvas(self):
        if self.active_part == MapView._SIMULATION_ACTIVE:
            self.__draw_simulation_view()
        else:
            if self.is_view_changed:
                if self.active_part == View._FUEL_ACTIVE:
                    self._draw_fuel_view()
                elif self.active_part == View._TERRAIN_ACTIVE:
                    self._draw_terrain_view()
                else:
                    self._draw_ignition_view()
        self.is_view_changed = False

    def __draw_simulation_view(self):
        pass

    @override
    def _draw_fuel_view(self):
        pass

    @override
    def _draw_terrain_view(self):
        pass

    @override
    def _draw_ignition_view(self):
        pass


class LegendView(View):

    def __init__(self, master, width, height,
                 fuel_color_map=View.DEFAULT_FUEL_COLOR_MAP):
        View.__init__(self, master=master, width=width, height=height,
                      fuel_color_map=fuel_color_map)

    @override
    def add_fuel_model(self, fuel_model):
        pass

    @override
    def add_terrain_model(self, terrain_model):
        pass

    @override
    def add_ignition_model(self, ignition_model):
        pass

    @override
    def activate_fuel_view(self):
        self.active_part = View._FUEL_ACTIVE

    @override
    def activate_terrain_view(self):
        self.active_part = View._TERRAIN_ACTIVE

    @override
    def activate_ignition_view(self):
        self.active_part = View._IGNITIONS_ACTIVE

    @override
    def refresh_canvas(self):
        if self.is_view_changed:
            if self.active_part == View._FUEL_ACTIVE:
                self._draw_fuel_view()
            elif self.active_part == View._TERRAIN_ACTIVE:
                self._draw_terrain_view()
            else:
                self._draw_ignition_view()
        self.is_view_changed = False

    @override
    def _draw_fuel_view(self):
        pass

    @override
    def _draw_terrain_view(self):
        pass

    @override
    def _draw_ignition_view(self):
        pass


def override(f): return f
