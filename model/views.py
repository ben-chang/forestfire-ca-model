from Tkinter import Canvas
from abc import ABCMeta, abstractmethod


class View(Canvas):

    __metaclass__ = ABCMeta

    _FUEL_ACTIVE = 0
    _TERRAIN_ACTIVE = 1
    _IGNITIONS_ACTIVE = 2
    _SIMULATION_ACTIVE = 3

    _N_CLASSES = 10

    RED_SCHEME = 'red'
    BLACK_SCHEME = 'black'
    GREEN_SCHEME = 'green'
    BLUE_SCHEME = 'blue'
    YELLOW_SCHEME = 'yellow'
    YELLOW_RED_SCHEME = 'yellow_red'

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

    DEFAULT_GRADIENT_COLOR_SCHEMES = {
                                      YELLOW_RED_SCHEME: ((255, 255, 0), (255, 0, 0)),
                                      BLACK_SCHEME: ((0, 0, 0), (255, 255, 255)),
                                      GREEN_SCHEME: ((255, 255, 255), (0, 255, 0)),
                                      BLUE_SCHEME: ((255, 255, 255), (0, 0, 255)),
                                      YELLOW_SCHEME: ((255, 255, 255), (255, 255, 0)),
                                      RED_SCHEME: ((255, 255, 255), (255, 0, 0)),
                                      }

    def __init__(self, master, width, height, n_classes=_N_CLASSES,
                 fuel_color_map=DEFAULT_FUEL_COLOR_MAP, color_scheme=BLACK_SCHEME):
        Canvas.__init__(self, master=master, width=width, height=height)
        self._height = height
        self._width = width
        self._n_classes = n_classes
        self._fuel_color_map = fuel_color_map
        self._color_scheme = color_scheme
        self._elev_min, self._elev_max = None, None
        self._ign_min, self._ign_max = None, None
        self._active_part = View._FUEL_ACTIVE
        self._is_view_changed = False

    def add_fuel_model(self, fuel_model):
        self._is_view_changed = True
        self._active_part = View._FUEL_ACTIVE

    def add_terrain_model(self, terrain_model):
        self._is_view_changed = True
        self._active_part = View._TERRAIN_ACTIVE
        self._elev_min, self._elev_max = View.find_min_and_max(terrain_model)

    def add_ignition_model(self, ignition_model):
        self._is_view_changed = True
        self._active_part = View._IGNITIONS_ACTIVE
        self._ign_min, self._ign_max = View.find_min_and_max(ignition_model)

    def activate_fuel_view(self):
        if self._active_part != View._FUEL_ACTIVE:
            self._active_part = View._FUEL_ACTIVE
            self._is_view_changed = True

    def activate_terrain_view(self):
        if self._active_part != View._TERRAIN_ACTIVE:
            self._active_part = View._TERRAIN_ACTIVE
            self._is_view_changed = True

    def activate_ignition_view(self):
        if self._active_part != View._IGNITIONS_ACTIVE:
            self._active_part = View._IGNITIONS_ACTIVE
            self._is_view_changed = True

    def activate_simulation_view(self):
        if self._active_part != View._SIMULATION_ACTIVE:
            self._active_part = View._SIMULATION_ACTIVE
            self._is_view_changed = True

    def refresh(self):
        if self._is_view_changed:
            if self._active_part == View._FUEL_ACTIVE:
                self._draw_fuel_view()
            elif self._active_part == View._TERRAIN_ACTIVE:
                self._draw_terrain_view()
            elif self._active_part == View._IGNITIONS_ACTIVE:
                self._draw_ignition_view()
            else:
                self._draw_simulation_view()
            self._is_view_changed = False
            return True
        return False

    @abstractmethod
    def _draw_fuel_view(self):
        pass

    @abstractmethod
    def _draw_terrain_view(self):
        pass

    @abstractmethod
    def _draw_ignition_view(self):
        pass

    @abstractmethod
    def _draw_simulation_view(self):
        pass

    @staticmethod
    def find_min_and_max(matrix):
        temp_min, temp_max = matrix[0][0], matrix[0][0]
        for row in matrix:
            for val in row:
                if val > temp_max:
                    temp_max = val
                if val < temp_min:
                    temp_min = val
        return temp_min, temp_max

    @staticmethod
    def find_unique_elements(matrix):
        uniques = []
        for row in matrix:
            for val in row:
                if val not in uniques:
                    uniques.append(val)
        return uniques

    @staticmethod
    def calculate_color(min_val, max_val, classes, val, color_scheme):
        if val < 0:
            return View.convert_rbg_triplet_hexadecimal((255, 255, 255))
        gradient = (max_val - min_val) / float(classes)
        color_class = int((val - min_val) / gradient)
        red_start, red_end = color_scheme[0][0], color_scheme[1][0]
        green_start, green_end = color_scheme[0][1], color_scheme[1][1]
        blue_start, blue_end = color_scheme[0][2], color_scheme[1][2]
        color = (red_start - (color_class * ((red_start - red_end) / classes)),
                 green_start - (color_class * ((green_start - green_end) / classes)),
                 blue_start - (color_class * ((blue_start - blue_end) / classes)))
        return View.convert_rbg_triplet_hexadecimal(color)

    @staticmethod
    def convert_rbg_triplet_hexadecimal(rbg):
        return '#'+''.join(map(chr, rbg)).encode('hex')


class MapView(View):

    def __init__(self, master, width, height, legend_view,
                 n_cols, n_rows, n_classes=View._N_CLASSES,
                 fuel_color_map=View.DEFAULT_FUEL_COLOR_MAP,):
        View.__init__(self, master=master, width=width, height=height,
                      n_classes=n_classes, fuel_color_map=fuel_color_map)
        self.__legend_view = legend_view
        self.__n_cols, self.__n_rows = n_cols, n_rows
        self.__start_x, self.__start_y, self.__square_side = MapView.get_dimensions(width, height,
                                                                                    n_cols, n_rows)
        self.__fuel_model = None
        self.__terrain_model = None
        self.__ignition_model = None
        self.__fire_state = None
        self.__is_fire_state_changed = False

    @override
    def add_fuel_model(self, fuel_model):
        View.add_fuel_model(self, fuel_model)
        self.__fuel_model = fuel_model
        self.__legend_view.add_fuel_model(fuel_model)

    @override
    def add_terrain_model(self, terrain_model):
        View.add_terrain_model(self, terrain_model)
        self.__terrain_model = terrain_model
        self.__legend_view.add_terrain_model(terrain_model)

    @override
    def add_ignition_model(self, ignition_model):
        View.add_ignition_model(self, ignition_model)
        self.__ignition_model = ignition_model
        self.__legend_view.add_ignition_model(ignition_model)

    @override
    def activate_fuel_view(self):
        View.activate_fuel_view(self)
        self.__legend_view.activate_fuel_view()

    @override
    def activate_terrain_view(self):
        View.activate_terrain_view(self)
        self.__legend_view.activate_terrain_view()

    @override
    def activate_ignition_view(self):
        View.activate_ignition_view(self)
        self.__legend_view.activate_ignition_view()

    @override
    def activate_simulation_view(self):
        View.activate_simulation_view(self)
        self.__legend_view.activate_simulation_view()

    @override
    def refresh(self):
        is_refreshed = View.refresh(self)
        if (not is_refreshed) and (self._active_part == View._SIMULATION_ACTIVE) and\
           self.__is_fire_state_changed:
            self._draw_simulation_view()
            self.__is_fire_state_changed = False
            return True
        return False

    def update_fire_state(self, fire_state):
        self.__fire_state = fire_state
        self.__is_fire_state_changed = True
        self.refresh()

    @override
    def _draw_fuel_view(self):
        if self.__fuel_model is not None:
            side = self.__square_side
            for i in xrange(self.__n_rows):
                for j in xrange(self.__n_cols):
                    x = self.__start_x + j * side
                    y = self.__start_y + i * side
                    rbg_color = self._fuel_color_map[self.__fuel_model[i][j]]
                    hex_color = View.convert_rbg_triplet_hexadecimal(rbg_color)
                    Canvas.create_rectangle(self, x, y, x+side, y+side, fill=hex_color)

    @override
    def _draw_terrain_view(self):
        if self.__terrain_model is not None:
            self.__draw_continuous_view(self._elev_min, self._elev_max,
                                        self.__terrain_model, self._color_scheme,
                                        self._n_classes)

    @override
    def _draw_ignition_view(self):
        if self.__ignition_model is not None:
            self.__draw_continuous_view(self._ign_min, self._ign_max,
                                        self.__ignition_model, self._color_scheme,
                                        self._n_classes)

    @override
    def _draw_simulation_view(self):
        if self.__fire_state is not None:
            self.__draw_continuous_view(0.0, 1.0, self.__fire_state,
                                        View.YELLOW_RED_SCHEME, 10,
                                        is_simulation_view=True)

    def __draw_continuous_view(self, min_val, max_val, value_matrix,
                               scheme, n_classes, is_simulation_view=False):
        color_scheme = View.DEFAULT_GRADIENT_COLOR_SCHEMES[scheme]
        side = self.__square_side
        for i in xrange(self.__n_rows):
            for j in xrange(self.__n_cols):
                if is_simulation_view and value_matrix[i][j] <= 0:
                    continue
                x = self.__start_x + j * side
                y = self.__start_y + i * side
                color = View.calculate_color(min_val, max_val, n_classes,
                                             value_matrix[i][j], color_scheme)
                Canvas.create_rectangle(self, x, y, x+side, y+side, fill=color)

    @staticmethod
    def get_dimensions(canvas_width, canvas_height, n_cols, n_rows):
        if n_cols > n_rows:
            drawn_col_width = canvas_width / n_cols
        else:
            drawn_col_width = canvas_height / n_rows
        start_x = (canvas_width - (drawn_col_width * n_cols)) / 2
        start_y = (canvas_height - (drawn_col_width * n_rows)) / 2
        return start_x, start_y, drawn_col_width


class LegendView(View):

    def __init__(self, master, width, height, n_classes=View._N_CLASSES,
                 fuel_color_map=View.DEFAULT_FUEL_COLOR_MAP):
        View.__init__(self, master=master, width=width, height=height,
                      n_classes=n_classes, fuel_color_map=fuel_color_map)
        self.__fuel_types = None

    @override
    def add_fuel_model(self, fuel_model):
        View.add_fuel_model(self, fuel_model)
        self.__fuel_types = View.find_unique_elements(fuel_model)

    @override
    def add_terrain_model(self, terrain_model):
        View.add_terrain_model(self, terrain_model)

    @override
    def add_ignition_model(self, ignition_model):
        View.add_ignition_model(self, ignition_model)

    @override
    def _draw_fuel_view(self):
        if self.__fuel_types is not None:
            pass

    @override
    def _draw_terrain_view(self):
        if self._elev_min is not None and self._elev_max is not None:
            pass

    @override
    def _draw_ignition_view(self):
        if self._ign_min is not None and self._ign_max is not None:
            pass

    @override
    def _draw_simulation_view(self):
        pass


def override(f): return f
