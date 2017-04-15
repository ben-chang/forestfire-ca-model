from random import randint
import math


class Simulation(object):
    """
    Simulation class: A simulation object that simulates individual wildfires
                      based on constant landscape characteristics (fuel configuration,
                      topography and spatial ignition likelihoods). The class and the
                      fire_spread() function is flexible in the sense that it allows
                      users to use any arbitrary fire event duration, ignition location,
                      wind speed and wind direction for individual spread events.
    """

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
                 cell_side_length, ignition_matrix,
                 lookup_table=DEFAULT_FUEL_LOOKUP_TABLE):

        """
        :param fuel_matrix     : A python nested list (matrix) of 'int' values
                                 representing the landscape's fuel configuration.
        :param terrain_matrix  : A python nested list (matrix) of 'int'/'float'
                                 values representing the landscape's topography.
        :param cell_side_length: An 'int'/'float' value indicating the
                                 resolution of the landscape.
        :param ignition_matrix : A python nested list (matrix) of 'int'/'float'
                                 values between 0-100 representing the spatial
                                 ignition likelihoods of the landscape.
        :param lookup_table    : A dictionary of 'int' keys & 'float' values
                                 where keys map from 'int' fuel type codes
                                 to associated spread rate values in m/s.
        """

        self.width = len(fuel_matrix[0])
        self.height = len(fuel_matrix)
        self.fuel_matrix = fuel_matrix
        self.terrain_inf_matrix = self.__initialise_terrain_influence_matrix(terrain_matrix)
        self.ignition_probabilities = self.__get_ignition_probabilities(ignition_matrix)
        self.cell_side_length = cell_side_length
        self.lookup_table = lookup_table
        self.max_spread_rate = Simulation.get_max_key(self.lookup_table)

    def __initialise_terrain_influence_matrix(self, terrain_matrix):

        """
        :param terrain_matrix           : A python nested list (matrix) of 'int'/'float'
                                          values representing the landscape's topography.
        :return terrain_influence_matrix: A python nested list (matrix) of tuples containing
                                          8 terrain influence values from the eight cardinal
                                          spread directions (W, N, E, S, NW, NE, SE, SW)
                                          influencing fire spread towards the middle cell.

        """
        terrain_matrix = Simulation.add_buffer_zone(terrain_matrix, 1, 0)
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

    def __get_ignition_probabilities(self, ignition_matrix):

        """
        :param ignition_matrix     : A python nested list (matrix) of 'int'/'float'
                                     values between 0-100 representing the spatial
                                     ignition likelihoods of the landscape
        :return potential_locations: A list of multiple ignition locations where
                                     landscape[i][j] is appended to ignition
                                     probability list proportionally to its
                                     ignition likelihood
        """

        potential_locations = []
        for i in xrange(self.height):
            for j in xrange(self.width):
                for k in xrange(ignition_matrix[i][j]):
                    potential_locations.append((i, j))
        return potential_locations

    def spread_fire(self, wind_data, event_duration_hrs,
                    random_ignition=False):
        """
        :param wind_data         :  A tuple of wind direction and wind speed:
                                    wind direction: counter-clockwise departure from
                                                    West-East axis in degrees.
                                    wind speed:     in m/s.
        :param event_duration_hrs:  Length of spread event in hours.
        :param random_ignition   : 'Boolean' value indicating ignition type:
                                   'True'  = random ignition
                                   'False' = probability based ignition
        :return fire_dimension   :  List of tuples storing fire perimeter
                                   'x' & 'y' values plus ignition origin .
        """

        previous_states = [[0] * (self.width+1) for i in xrange(self.height+1)]
        n_iterations = Simulation.get_n_iterations(self.max_spread_rate,
                                                   self.cell_side_length,
                                                   event_duration_hrs)

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

    @staticmethod
    def add_buffer_zone(matrix, buffer_size, buffer_fill):
        """
        :param matrix           : Arbitrary nested Python List (matrix).
        :param buffer_size      : 'int' value representing buffer zone width
        :param buffer_fill      : Any arbitrary value to fill matrix buffer zone.
        :return buffered_matrix : Buffered matrix.
        """
        n_cols = len(matrix[0])
        buffered_matrix = [[buffer_fill] * (n_cols+buffer_size*2)] * buffer_size
        for row in matrix:
            buffered_matrix.append(([buffer_fill] * buffer_size) + row + ([buffer_fill] * buffer_size))
        buffered_matrix += [[buffer_fill] * (n_cols + buffer_size * 2)] * buffer_size
        return buffered_matrix

    @staticmethod
    def get_n_iterations(max_spread_rate, cell_side_length,
                         event_duration):
        """
        :param max_spread_rate : 'int' fuel of fuel type with maximum spread rate in m/s.
        :param cell_side_length: 'int'/'float' resolution of landscape in meters.
        :param event_duration  :  Length of fire spread event in hours.
        :return                : 'int' number indicating the number of simulation iterations.
        """
        return int((3600 * event_duration) / (cell_side_length / max_spread_rate))

    @staticmethod
    def get_max_key(dictionary):
        """
        :param dictionary  : Any arbitrary dictionary.
        :return max_val_key: The key of maximum value within the dictionary.
        """
        max_val_key = dictionary.keys()[0]
        for key in dictionary.keys:
            if dictionary[key] > dictionary[max_val_key]:
                max_val_key = key
        return max_val_key

    @staticmethod
    def random_choice(collection):
        """
        :param collection: Any arbitrary iterable python collection.
        :return          : A random element of the input python collection.
        """
        return collection[randint(0, len(collection) - 1)]

    @staticmethod
    def calculate_wind_influence(wind_direction, wind_speed,
                                 influence_direction):
        """
        :param wind_direction     : 'int' counter-clockwise departure
                                     of wind direction from West-East axis in degrees.
        :param wind_speed         : 'int' value indicating wind speed in m/s.
        :param influence_direction: 'int' counter-clockwise departure of spread
                                     direction from West-East axis in degrees
        :return:
        """
        wind_dir_rad = (wind_direction / 180.0) * math.pi
        inf_dir_rad = (influence_direction / 180.0) * math.pi
        delta_dir_rad = math.fabs(wind_dir_rad / inf_dir_rad)
        wind_speed_inf_comp = wind_speed * math.cos(delta_dir_rad)
        return Simulation.linear_map(wind_speed_inf_comp, Simulation.WIND_INF_Y_INTERCEPT,
                                     Simulation.WIND_INF_SLOPE)

    @staticmethod
    def linear_map(x, y_intercept, slope):
        """
        :param x          : 'int'/'float' predictor value
        :param y_intercept: 'int'/'float' indicating 'y' axis interception location
        :param slope      : 'int'/'float' value of x/y slope
        :return           :  linearly predicted 'y' value
        """
        return min(0.01, y_intercept + (slope * x))

    @staticmethod
    def local_rule(self_state, w_state, n_state, e_state, s_state,
                   nw_state, ne_state, se_state, sw_state,
                   w_elev_inf, n_elev_inf, e_elev_inf, s_elev_inf,
                   nw_elev_inf, ne_elev_inf, se_elev_inf, sw_elev_inf,
                   w_wind, n_wind, e_wind, s_wind,
                   nw_wind, ne_wind, se_wind, sw_wind, self_spread_rate):
        """
        :param self_state       : 'float' value between 0-1 indicating state of cell.
        :param w_state          : 'float' value between 0-1 indicating state of cell to west.
        :param n_state          : 'float' value between 0-1 indicating state of cell to north.
        :param e_state          : 'float' value between 0-1 indicating state of cell to east.
        :param s_state          : 'float' value between 0-1 indicating state of cell to south.
        :param nw_state         : 'float' value between 0-1 indicating state of cell to north-west.
        :param ne_state         : 'float' value between 0-1 indicating state of cell to north-east.
        :param se_state         : 'float' value between 0-1 indicating state of cell to south-east.
        :param sw_state         : 'float' value between 0-1 indicating state of cell to south-west.
        :param w_elev_inf       : 'float' value greater than 0 indicating slope influence from west.
        :param n_elev_inf       : 'float' value greater than 0 indicating slope influence from north.
        :param e_elev_inf       : 'float' value greater than 0 indicating slope influence from east.
        :param s_elev_inf       : 'float' value greater than 0 indicating slope influence from south.
        :param nw_elev_inf      : 'float' value greater than 0 indicating slope influence from north-west.
        :param ne_elev_inf      : 'float' value greater than 0 indicating slope influence from north-east.
        :param se_elev_inf      : 'float' value greater than 0 indicating slope influence from south-east.
        :param sw_elev_inf      : 'float' value greater than 0 indicating slope influence from south-west.
        :param w_wind           : 'float' value greater than 0 indicating wind influence from west.
        :param n_wind           : 'float' value greater than 0 indicating wind influence from north.
        :param e_wind           : 'float' value greater than 0 indicating wind influence from east.
        :param s_wind           : 'float' value greater than 0 indicating wind influence from south.
        :param nw_wind          : 'float' value greater than 0 indicating wind influence from north-west.
        :param ne_wind          : 'float' value greater than 0 indicating wind influence from north-east.
        :param se_wind          : 'float' value greater than 0 indicating wind influence from south-east.
        :param sw_wind          : 'float' value greater than 0 indicating wind influence from south-west.
        :param self_spread_rate : 'float' value representing the spread rate of fuel type on cell.
        :return                 : 'float' value between 0 and 1 indicating cell's next state.
        """
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
