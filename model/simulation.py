from random import randint
import math
class Simulation(object):

    WIND_INF_Y_INTERCEPT = 1
    WIND_INF_SLOPE = 2/30.0
    TOPOGRAPHY_INF_Y_INTERCEPT = 1
    TOPOGRAPHY_INF_SLOPE = 2/50.0
    DIAGONAL_DISTANCE_WEIGHT = 0.83

    DEFAULT_FUEL_LOOKUP_TABLE = {
                                 0 : 0,
                                 1 : 0.1,
                                 2 : 0.2,
                                 3 : 0.3,
                                 4 : 0.4,
                                 5 : 0.5,
                                 6 : 0.6,
                                 7 : 0.7,
                                 8 : 0.8,
                                 9 : 0.9,
                                 10: 1.0
                                }

    def __init__(self, fuel_matrix, terrain_matrix, wind_data,
                 event_durations, cell_side_length,
                 lookup_table=DEFAULT_FUEL_LOOKUP_TABLE, ignition_matrix=False):
        self.width = len(fuel_matrix[0])
        self.height = len(fuel_matrix)
        self.fuel_matrix = fuel_matrix
        self.terrain_influence_matrix = self.initialise_terrain_influence_matrix(terrain_matrix)
        self.wind_data = wind_data
        self.ignition_matrix = ignition_matrix
        self.event_durations = event_durations
        self.cell_side_length = cell_side_length
        self.lookup_table = lookup_table
        self.max_spread_rate = Simulation.get_max_key(self.lookup_table)

    def initialise_terrain_influence_matrix(self, terrain_matrix):
        terrain_influence_matrix = [[1] * self.width for i in xrange(self.height)]
        for i in xrange(self.height):
            for j in xrange(self.width):
                w_inf, n_inf, e_inf, s_inf = 1, 1, 1, 1
                nw_inf, ne_inf, se_inf, sw_inf = 1, 1, 1, 1
                if i == 0 and j == 0:
                    e_inf = Simulation.linear_map(terrain_matrix[i][j + 1] - terrain_matrix[i][j],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i + 1][j] - terrain_matrix[i][j],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                    se_inf = Simulation.linear_map(terrain_matrix[i + 1][j + 1] - terrain_matrix[i][j],
                                               Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                               Simulation.TOPOGRAPHY_INF_SLOPE)

                elif i == 0 and j == self.width - 1:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j - 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i + 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    sw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                elif i == self.height - 1 and j == 0:

                    n_inf = Simulation.linear_map(terrain_matrix[i - 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    e_inf = Simulation.linear_map(terrain_matrix[i][j + 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    ne_inf = Simulation.linear_map(terrain_matrix[i - 1][j + 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)

                elif i == self.height - 1 and j == self.width - 1:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j - 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    n_inf = Simulation.linear_map(terrain_matrix[i - 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    nw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                elif j == 0:
                    n_inf = Simulation.linear_map(terrain_matrix[i - 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    e_inf = Simulation.linear_map(terrain_matrix[i][j + 1] - terrain_matrix[i][j],
                                                 Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                 Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i + 1][j] - terrain_matrix[i][j],
                                                 Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                 Simulation.TOPOGRAPHY_INF_SLOPE)
                    ne_inf = Simulation.linear_map(terrain_matrix[i - 1][j + 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    se_inf = Simulation.linear_map(terrain_matrix[i + 1][j + 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                elif j == self.width - 1:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j - 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    n_inf = Simulation.linear_map(terrain_matrix[i - 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i + 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    nw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                    sw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)

                elif i == 0:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j - 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    e_inf = Simulation.linear_map(terrain_matrix[i][j + 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i + 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    se_inf = Simulation.linear_map(terrain_matrix[i + 1][j + 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                    sw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                elif i == self.width - 1:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j - 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    n_inf = Simulation.linear_map(terrain_matrix[i - 1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    e_inf = Simulation.linear_map(terrain_matrix[i][j + 1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    nw_inf = Simulation.linear_map(terrain_matrix[i - 1][j - 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)
                    ne_inf = Simulation.linear_map(terrain_matrix[i - 1][j + 1] - terrain_matrix[i][j],
                                                   Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                   Simulation.TOPOGRAPHY_INF_SLOPE)

                else:
                    w_inf = Simulation.linear_map(terrain_matrix[i][j-1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    n_inf = Simulation.linear_map(terrain_matrix[i-1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    e_inf = Simulation.linear_map(terrain_matrix[i][j+1] - terrain_matrix[i][j],                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    s_inf = Simulation.linear_map(terrain_matrix[i+1][j] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    nw_inf = Simulation.linear_map(terrain_matrix[i-1][j-1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    ne_inf = Simulation.linear_map(terrain_matrix[i-1][j+1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    se_inf = Simulation.linear_map(terrain_matrix[i+1][j+1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                    sw_inf = Simulation.linear_map(terrain_matrix[i-1][j-1] - terrain_matrix[i][j],
                                                  Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                                  Simulation.TOPOGRAPHY_INF_SLOPE)
                terrain_influence_matrix[i][j] = (w_inf, n_inf, e_inf, s_inf,
                                                  nw_inf, ne_inf, se_inf, sw_inf)
        return terrain_influence_matrix

    @staticmethod
    def get_n_iterations(max_spread_rate, cell_side_length,
                         event_duration):
        return int((3600 * event_duration) / (cell_side_length / max_spread_rate))

    @staticmethod
    def get_max_key(dictionary):
        max_rate_key = dictionary.keys()[0]
        for key in dictionary.keys:
            if dictionary[key] > dictionary[max_rate_key]:
                max_rate_key = key
        return max_rate_key

    def find_ignition_location(self):
        if not self.ignition_matrix:
            row = randint(0, self.height - 1)
            col = randint(0, self.width - 1)
            return tuple([row, col])
        else:
            potential_locations = []
            for i in xrange(self.height):
                for j in xrange(self.width):
                    for k in xrange(self.ignition_matrix[i][j]):
                        potential_locations.append((i, j))
            return potential_locations[randint(0, len(potential_locations) - 1)]

    @staticmethod
    def random_choice(collection):
        return collection[randint(0, len(collection) - 1)]

    @staticmethod
    def calculate_wind_influence(wind_direction, wind_speed,
                                 influence_direction):
        wind_dir_rad = (wind_direction / 180.0) * math.pi
        inf_dir_rad = (influence_direction / 180.0) * math.pi
        delta_dir_rad = math.fabs(wind_dir_rad / inf_dir_rad)
        wind_speed_inf_comp = wind_speed * math.cos(delta_dir_rad)
        return Simulation.linear_map(wind_speed_inf_comp, Simulation.WIND_INF_Y_INTERCEPT,
                                     Simulation.WIND_INF_SLOPE)


    @staticmethod
    def linear_map(x, y_intercept, slope):
        return min(0.01, y_intercept + (slope * x))

    @staticmethod
    def local_rule(self_state, w_state, n_state, e_state, S_state,
                   nw_state, ne_state, se_state, sw_state,
                   w_elevation, n_elevation, e_elevation, s_elevation,
                   nw_elevation, ne_elevation, se_elevation, sw_elevation,
                   w_wind_inf, n_wind_inf, e_wind_inf, s_wind_inf,
                   nw_wind, ne_wind, se_wind, sw_wind, self_spread_rate)
        return self_spread_rate * \
               (self_state + (w_state))

    def spread_fire(self):
        previous_states = [[0] * self.width for i in xrange(self.height)]
        next_states = [[0] * self.width for i in xrange(self.height)]
        origin = self.find_ignition_location()
        event_duration = Simulation.random_choice(self.event_durations)
        n_iterations = Simulation.get_n_iterations(self.max_spread_rate,
                                                   self.cell_side_length,
                                                   event_duration)
        ignition_column, ignition_row = origin[1], origin[0]
        previous_states[ignition_row][ignition_column] = 1
        wind = Simulation.random_choice(self.wind_data)
        wind_dir, wind_speed = wind[0], wind[1]

        W_WIND_INFLUENCE =  Simulation.calculate_wind_influence(wind_dir, wind_speed, 180)
        N_WIND_INFLUENCE =  Simulation.calculate_wind_influence(wind_dir, wind_speed, 90)
        E_WIND_INFLUENCE =  Simulation.calculate_wind_influence(wind_dir, wind_speed, 0)
        S_WIND_INFLUENCE =  Simulation.calculate_wind_influence(wind_dir, wind_speed, 270)
        NW_WIND_INFLUENCE = Simulation.calculate_wind_influence(wind_dir, wind_speed, 135)
        NE_WIND_INFLUENCE = Simulation.calculate_wind_influence(wind_dir, wind_speed, 45)
        SE_INFLUENCE =      Simulation.calculate_wind_influence(wind_dir, wind_speed, 315)
        SW_WIND_INFLUENCE = Simulation.calculate_wind_influence(wind_dir, wind_speed, 225)

        for i in xrange(n_iterations):
            for j in xrange(self.height):
                for k in xrange(self.width):
                    if j == 0 and k == 0:

                    if j == 0 and k == self.width-1:
                        pass
                    if j == self.height-1 and k == 0:
                        pass
                    if j == self.height-1 and k == self.width-1:
                        pass
                    if j == 0:
                        pass
                    if j == self.height-1:
                        pass
                    if k == 0:
                        pass
                    if k == self.width-1:
                        pass
                    else:






