SKIP_LINES = 6
COL_WORD = 'col'
ROW_WORD = 'row'

INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE = 'Inconsistent ' + ROW_WORD + ' and/or ' + ROW_WORD +\
                                               ' Information Exception: value that follows '      +\
                                                ROW_WORD + ' or/and ' + COL_WORD + ' keyword(s)'  +\
                                               'is(are) non-number-like value.'

MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE = 'Missing ' + ROW_WORD + ' and/or ' + COL_WORD       +\
                                          ' Information Exception: value(s) is missing after' +\
                                          COL_WORD + ' and/or ' + ROW_WORD + ' keyword(s).'

MISSING_HEADER_EXCEPTION_MESSAGE = 'Missing Header Exception: ' + ROW_WORD +\
                                   ' and/or ' + COL_WORD + ' keyword(s) are missing from header.'
NON_MATCHING_DIMENSIONS_EXCEPTION_MESSAGE = "Row or Column dimensions don't match between header" +\
                                            "and file content."
NON_NUMBER_VALUES_IN_GRID_EXCEPTION = ".ASCII grid contains non-number characters."

def parse_ASCII_file (path, ints=False):
    try:
        opened_file = open(path, 'r')
        nCols_nRows = parse_header(opened_file)
        nCols = nCols_nRows[0]
        nRows = nCols_nRows[1]
        matrix = [[0] * nCols for i in xrange(nRows)]
        check, i = 0, 0
        try:
            for line in opened_file:
                check += 1
                if (check <= SKIP_LINES):
                    continue
                words = line.split(' ')
                for j in xrange(nCols):
                    if (ints):
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

def parse_header (file):
    nCols = None
    nRows = None
    for line in file:
        words = line.split(' ')
        if (words[0] == COL_WORD):
            try:
                nCols = int(words[1])
            except IndexError:
                raise IndexError(MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE)
            except ValueError:
                raise ValueError(INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE)
        if (words[0] == ROW_WORD):
            try:
                nRows = int(words[1])
            except IndexError:
                raise IndexError(MISSING_ROW_COL_VALUE_EXCEPTION_MESSAGE)
            except ValueError:
                raise ValueError(INCONSISTENT_ROW_COL_VALUE_EXCEPTION_MESSAGE)
        if (is_header_parsing_finished(nCols, nRows)):
            break
    if not (is_header_parsing_finished(nCols, nRows)):
        raise Exception(MISSING_HEADER_EXCEPTION_MESSAGE)
    return (nCols, nRows)

def is_header_parsing_finished(nCols, nRows):
    return nRows != None and nCols != None