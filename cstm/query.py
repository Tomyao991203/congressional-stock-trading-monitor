from typing import Union

def where_condition(var_name:str, var_value: Union[int, str]) -> str:
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
    
    
    
    
    