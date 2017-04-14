from random import randint
import math


class Simulation(object):

    WIND_INF_Y_INTERCEPT = 1
    WIND_INF_SLOPE = 2/30.0
    TOPOGRAPHY_INF_Y_INTERCEPT = 1
    TOPOGRAPHY_INF_SLOPE = 2/50.0
    DIAGONAL_DISTANCE_WEIGHT = 0.83

    DEFAULT_FUEL_LOOKUP_TABLE = {
                                  0: 0,
                                  1: 0.1,
                                  2: 0.2,
                                  3: 0.3,
                                  4: 0.4,
                                  5: 0.5,
                                  6: 0.6,
                                  7: 0.7,
                                  8: 0.8,
                                  9: 0.9,
                                  10: 1.0
                                }

    def __init__(self, fuel_matrix, terrain_matrix,
                 event_durations, cell_side_length, ignition_matrix,
                 lookup_table=DEFAULT_FUEL_LOOKUP_TABLE):
        self.width = len(fuel_matrix[0])
        self.height = len(fuel_matrix)
        self.fuel_matrix = fuel_matrix
        self.terrain_inf_matrix = self.__initialise_terrain_influence_matrix(terrain_matrix)
        self.ignition_probabilities = self.__get_ignition_probabilities(ignition_matrix)
        self.event_durations = event_durations
        self.cell_side_length = cell_side_length
        self.lookup_table = lookup_table
        self.max_spread_rate = Simulation.get_max_key(self.lookup_table)

    def __initialise_terrain_influence_matrix(self, terrain_matrix):
        terrain_influence_matrix = []
        for i in xrange(1, self.height, 1):
            sub_matrix = []
            for j in xrange(1, self.width, 1):
                w_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i][j-1],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                n_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i-1][j],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                e_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i][j+1],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                s_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i+1][j],
                                              Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                              Simulation.TOPOGRAPHY_INF_SLOPE)
                nw_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i-1][j-1],
                                               Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                               Simulation.TOPOGRAPHY_INF_SLOPE)
                ne_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i-1][j+1],
                                               Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                               Simulation.TOPOGRAPHY_INF_SLOPE)
                se_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i+1][j+1],
                                               Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                               Simulation.TOPOGRAPHY_INF_SLOPE)
                sw_inf = Simulation.linear_map(terrain_matrix[i][j] - terrain_matrix[i-1][j-1],
                                               Simulation.TOPOGRAPHY_INF_Y_INTERCEPT,
                                               Simulation.TOPOGRAPHY_INF_SLOPE)
                sub_matrix.append((w_inf, n_inf, e_inf, s_inf,
                                   nw_inf, ne_inf, se_inf, sw_inf))
            terrain_influence_matrix.append(sub_matrix)
        return terrain_influence_matrix

    @staticmethod
    def get_n_iterations(max_spread_rate, cell_side_length,
                         event_duration):
        return int((3600 * event_duration) / (cell_side_length / max_spread_rate))

    @staticmethod
    def get_max_key(dictionary):
        max_val_key = dictionary.keys()[0]
        for key in dictionary.keys:
            if dictionary[key] > dictionary[max_val_key]:
                max_val_key = key
        return max_val_key

    def __get_ignition_probabilities(self, ignition_matrix):
        potential_locations = []
        for i in xrange(self.height):
            for j in xrange(self.width):
                for k in xrange(ignition_matrix[i][j]):
                    potential_locations.append((i, j))
        return potential_locations

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
    def local_rule(self_state, w_state, n_state, e_state, s_state,
                   nw_state, ne_state, se_state, sw_state,
                   w_elev_inf, n_elev_inf, e_elev_inf, s_elev_inf,
                   nw_elev_inf, ne_elev_inf, se_elev_inf, sw_elev_inf,
                   w_wind, n_wind, e_wind, s_wind,
                   nw_wind, ne_wind, se_wind, sw_wind, self_spread_rate):
        next_state = self_spread_rate *\
                    (self_state + (w_state * w_elev_inf * w_wind +
                                   n_state * n_elev_inf * n_wind +
                                   e_state * e_elev_inf * e_wind +
                                   s_state * s_elev_inf * s_wind) +
                     Simulation.DIAGONAL_DISTANCE_WEIGHT *
                                  (nw_state * nw_elev_inf * nw_wind +
                                   ne_state * ne_elev_inf * ne_wind +
                                   se_state * se_elev_inf * se_wind +
                                   sw_state * sw_elev_inf * sw_wind)
                     )
        return min(1, next_state)

    def spread_fire(self, wind_data, random_ignition=False):

        previous_states = [[0] * (self.width+1) for i in xrange(self.height+1)]
        event_duration = Simulation.random_choice(self.event_durations)
        n_iterations = Simulation.get_n_iterations(self.max_spread_rate,
                                                   self.cell_side_length,
                                                   event_duration)

        wind = Simulation.random_choice(wind_data)
        wind_dir, wind_speed = wind[0], wind[1]
        w_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 180)
        n_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 90)
        e_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 0)
        s_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 270)
        nw_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 135)
        ne_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 45)
        se_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 315)
        sw_wind_inf = Simulation.calculate_wind_influence(wind_dir, wind_speed, 225)

        if not random_ignition:
            origin = Simulation.random_choice(self.ignition_probabilities)
            ignition_column, ignition_row = origin[1], origin[0]

        else:
            ignition_column = Simulation.random_choice([i for i in xrange(self.width)])
            ignition_row = Simulation.random_choice([i for i in xrange(self.height)])

        previous_states[ignition_row][ignition_column] = 1

        for i in xrange(n_iterations):
            next_states = []
            for j in xrange(1, self.height+1, 1):
                sub_next_states = []
                for k in xrange(1, self.width+1, 1):
                    if (j == 0 or j == self.height) or (k == 0 or k == self.width):
                        sub_next_states.append(0)
                        continue
                    self_state = previous_states[j][k]
                    spread_rate = self.lookup_table.get(self.fuel_matrix[i][j])
                    w_state, w_elev_inf = previous_states[j][k-1], self.terrain_inf_matrix[j][k][0]
                    n_state, n_elev_inf = previous_states[j-1][k], self.terrain_inf_matrix[j][k][1]
                    e_state, e_elev_inf = previous_states[j][k+1], self.terrain_inf_matrix[j][k][2]
                    s_state, s_elev_inf = previous_states[j+1][k], self.terrain_inf_matrix[j][k][3]
                    nw_state, nw_elev_inf = previous_states[j-1][k-1], self.terrain_inf_matrix[j][k][4]
                    ne_state, ne_elev_inf = previous_states[j-1][k+1], self.terrain_inf_matrix[j][k][5]
                    se_state, se_elev_inf = previous_states[j+1][k+1], self.terrain_inf_matrix[j][k][6]
                    sw_state, sw_elev_inf = previous_states[j+1][k-1], self.terrain_inf_matrix[j][k][7]
                    next_state = Simulation.local_rule(self_state, w_state, n_state, e_state, s_state,
                                                       nw_state, ne_state, se_state, sw_state,
                                                       w_elev_inf, n_elev_inf, e_elev_inf, s_elev_inf,
                                                       nw_elev_inf, ne_elev_inf, se_elev_inf, sw_elev_inf,
                                                       w_wind_inf, n_wind_inf, e_wind_inf, s_wind_inf,
                                                       nw_wind_inf, ne_wind_inf, se_wind_inf, sw_wind_inf,
                                                       spread_rate)
                    sub_next_states.append(next_state)
                next_states.append(sub_next_states)
            previous_states = next_states
