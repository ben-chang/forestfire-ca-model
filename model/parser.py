SKIP_LINES = 6
COL_WORD = 'col'
ROW_WORD = 'row'

INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE = 'Inconsistent ' + ROW_WORD + ' and/or ' + ROW_WORD +\
                                               ' Information Exception: value that follows ' +\
                                                ROW_WORD + ' or/and ' + COL_WORD + ' keyword(s)' +\
                                               'is(are) non-number-like value.'

MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE = 'Missing ' + ROW_WORD + ' and/or ' + COL_WORD +\
                                          ' Information Exception: value(s) is missing after' +\
                                          COL_WORD + ' and/or ' + ROW_WORD + ' keyword(s).'

MISSING_HEADER_EXCEPTION_MESSAGE = 'Missing Header Exception: ' + ROW_WORD +\
                                   ' and/or ' + COL_WORD + ' keyword(s) are missing from header.'

NON_MATCHING_DIMENSIONS_EXCEPTION_MESSAGE = "Row or Column dimensions don't match between header" +\
                                            "and file content."

NON_NUMBER_VALUES_IN_GRID_EXCEPTION = ".ASCII grid contains non-number characters."


def parse_ascii_file(path, ints=False):
    try:
        opened_file = open(path, 'r')
        n_cols_n_rows = parse_header(opened_file)
        n_cols = n_cols_n_rows[0]
        n_rows = n_cols_n_rows[1]
        matrix = [[0] * n_cols for i in xrange(n_rows)]
        check, i = 0, 0
        try:
            for line in opened_file:
                check += 1
                if check <= SKIP_LINES:
                    continue
                words = line.split(' ')
                for j in xrange(n_cols):
                    if ints:
                        matrix[i][j] = int(words[j])
                    else:
                        matrix[i][j] = float(words[j])
                i += 1
        except ValueError:
            raise ValueError(NON_NUMBER_VALUES_IN_GRID_EXCEPTION)
        except IndexError:
            raise IndexError(NON_MATCHING_DIMENSIONS_EXCEPTION_MESSAGE)
        return matrix
    except:
        raise


def parse_header(input_file):
    n_cols = None
    n_rows = None
    for line in input_file:
        words = line.split(' ')
        if words[0] == COL_WORD:
            try:
                n_cols = int(words[1])
            except IndexError:
                raise IndexError(MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE)
            except ValueError:
                raise ValueError(INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE)
        if words[0] == ROW_WORD:
            try:
                n_rows = int(words[1])
            except IndexError:
                raise IndexError(MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE)
            except ValueError:
                raise ValueError(INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE)
        if is_header_parsing_finished(n_cols, n_rows):
            break
    if not is_header_parsing_finished(n_cols, n_rows):
        raise Exception(MISSING_HEADER_EXCEPTION_MESSAGE)
    return tuple([n_cols, n_rows])


def is_header_parsing_finished(n_cols, n_rows):
    return n_rows is not None and n_cols is not None


#def override(f): return f


#def abstractmethod(f): return f
