from typing import Union, List


def where_condition(var_name: str, var_value: Union[int, str]) -> str:
    """
    return a string representing the condition for where
    @param var_name: the name of the key which the variable corresponds to
    @param var_value: the value of the variable
    @return: 'True' if the var_value is None or empty string, 'var_name = var_value' otherwise
    """
    if var_value is None or var_value == '':
        return 'True'
    if type(var_value).__name__ == 'int':
        return f'{var_name} = {var_value}'
    return f'{var_name} = \'{var_value}\''


def expression_wrapper(expression: Union[str, int], is_str: bool) -> str:
    """
    wrap the value with quotation marks if we want it to be a string value in the query
    :param expression: the expression we want to wrap up
    :type expression:  Union[str, int]
    :param is_str: a boolean indicating if the expression will be a str value in the query.
    :type is_str: bool
    :return: a str that is either 'a' or '\'a\''
    :rtype: str
    """
    if expression == '':
        return expression
    return f'\'{expression}\'' if is_str else f'{expression}'


def value_between(expression: str, lower_bound: Union[int, str], upper_bound: Union[int, str],
                  bound_is_str: bool = False):
    """
    Return a between condition string (i.e.: A between lower_bound and upper_bound)
    :param bound_is_str: whether the bound value is str type or not
    :type bound_is_str: bool
    :param expression: the expression we are examining
    :type expression: str
    :param lower_bound: value lower bound
    :type lower_bound: str or int
    :param upper_bound: value upper bound
    :type upper_bound: str or int
    :return: a between condition string
    :rtype: str
    """
    if lower_bound == "" or upper_bound == "" or expression == "":
        return "TRUE"
    return f"{expression} BETWEEN {expression_wrapper(lower_bound, bound_is_str)} AND " \
           f"{expression_wrapper(upper_bound, bound_is_str)}"


def value_greater_equal(expression: str, exact_value: Union[int, str], bound_is_str: bool = False):
    """
    Return a greater than condition string (i.e.: greater then exact_value)
    :param bound_is_str: whether the bound value is str type or not
    :type bound_is_str: bool
    :param expression: the expression we are examining
    :type expression: str
    :param exact_value: the expect value
    :return: a greater than condition string
    :rtype: str
    """
    if exact_value == "" or expression == "":
        return "TRUE"
    return f"{expression} >= {expression_wrapper(exact_value, bound_is_str)}"


def value_less_equal(expression: str, exact_value: Union[int, str], bound_is_str: bool = False):
    """
    Return a less than condition string (i.e.: less then exact_value)
    :param bound_is_str: whether the bound value is str type or not
    :type bound_is_str: bool
    :param expression: the expression we are examining
    :type expression: str
    :param exact_value: the expect value
    :return: a less than condition string
    :rtype: str
    """
    if exact_value == "" or expression == "":
        return "TRUE"
    return f"{expression} <= {expression_wrapper(exact_value, bound_is_str)}"


def equal_condition(expression: str, exact_value: Union[int, str], value_is_string: bool = True) -> str:
    """
    return an equal condition for string (SQLite)
    :param value_is_string: whether the exact value is string or not
    :type value_is_string: bool
    :param expression: the expression we are evaluating
    :param exact_value: the expect value
    :return: an equal condition for string in the form of XXX = 'aa' or 'TRUE' if one
        of input is empty
    """
    if exact_value == "" or expression == "":
        return "TRUE"
    return f"{expression} = {expression_wrapper(exact_value, value_is_string)}"


def aggregating_conditions(conditions: List[str]):
    """
    aggregating a list of conditions. Auto-inject "AND" between conditions unless detect a specified "OR" condition
    :param conditions: list of conditions
    :type conditions: list[str]
    :return: aggregated condition
    :rtype: str
    """
    if len(conditions) == 0 or conditions[-1] == 'OR':
        return "TRUE"
    result = f"({conditions[0]}"
    for condition in conditions[1:]:
        result = f"{result}) OR (" if condition == 'OR' else f"{result} AND {condition}"
    return result + ")"


def cases_str(expression: str, case_value_pairs: dict, else_value: Union[int, str], as_var_name: str,
              key_is_str: bool = False, value_is_str: bool = False):
    """
    return a string in the format of "CASE expression when exp_1 then ... when exp_n then ... ELSE else_value END as
        as_var_name". Used as a selected key. Currently, user has to make sure input is correct
    :param key_is_str: if the key should be a string, then TRUE, FALSE otherwise
    :type key_is_str: bool
    :param value_is_str:  if the value should be a string, then TRUE, FALSE otherwise
    :type value_is_str: bool
    :param as_var_name: the name we assign to this variable
    :type as_var_name: str
    :param expression: the expression we are evaluating, could be empty
    :type expression: str
    :param case_value_pairs: a dictionary where the key is the possible expression value, the value is the assign value
    :type case_value_pairs: dict
    :param else_value: the final assign value
    :type else_value: str or int
    :return: the final case string
    :rtype: str
    """

    case = f'CASE {expression}'
    assert len(case_value_pairs) != 0
    # raise Exception('you cannot have 0 cases')
    for key, value in case_value_pairs.items():
        case = f'{case} WHEN {expression_wrapper(key, key_is_str)} THEN {expression_wrapper(value, value_is_str)}'
    else_str = f' ELSE {expression_wrapper(else_value, value_is_str)}'
    end_as_str = f' END AS {as_var_name}'
    return case + else_str + end_as_str
