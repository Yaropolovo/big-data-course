from pyspark.sql.functions import col, struct, lit


def expand_df(df_to_expand):
    expanded_df = df_to_expand
    for col in expanded_df.schema.jsonValue().get('fields'):
        if isinstance(col.get('type'), dict):
            expanded_df = expand_struct_col(expanded_df, col)
    return expanded_df


def expand_struct_col(df, struct_col_schema):
    df_expanded = df
    col_name_to_drop = struct_col_schema.get('name')
    nested = struct_col_schema.get('type')

    if nested.get('type') == 'struct':
        for var in nested.get('fields'):

            long_name = col_name_to_drop + '.' + var.get('name')
            var_type = var.get('type')

            if isinstance(var_type, dict):
                var['name'] = long_name
                df_expanded = expand_struct_col(df_expanded, var)
            else:
                df_expanded = df_expanded.withColumn(long_name,
                                                     col(long_name))

    df_expanded = df_expanded.drop(col_name_to_drop)
    return df_expanded


def add_col_to_dict(col_name: str, child_as_dict: dict) -> dict:
    new_dict = child_as_dict

    if '.' in col_name:
        parent, child = col_name.split('.', 1)
        if parent in new_dict:
            new_dict[parent] = add_col_to_dict(child, new_dict[parent])
        else:
            new_dict[parent] = add_col_to_dict(child, {})
    else:
        new_dict[col_name] = None

    return new_dict


def create_named_struct_from_list(dict_of_col, parent_name):
    expression = "named_struct("
    for key, value in dict_of_col.items():
        if isinstance(value, dict):
            nested_parent_name = parent_name + '.' + key
            nested_str = create_named_struct_from_list(value, nested_parent_name)
            expression += f"'{key}', " + nested_str + ", "
        else:
            expression += f"'{key}', `{parent_name}.{key}`, "
    expression = expression[:-2] + ")"
    return expression


def create_list_of_expr(schema_as_dict):
    list_of_expr = []
    for key, value in schema_as_dict.items():
        if value:
            expr = create_named_struct_from_list(value, key) + ' as ' + key
            list_of_expr.append(expr)
        else:
            list_of_expr.append(key)
    return list_of_expr


def update_df(df, columns_dict):
    """
    Updates existing columns or creates new in dataframe df using
    columns from columns_dict.
    :param df: input dataframe
    :type df: pyspark.sql.Dataframe
    :param columns_dict: Key-value dictionary of columns which need to
    be updated. Key is a column name in
    the format of path.to.col
    :type param: Dict[str, pyspark.sql.Column]
    :return: dataframe with updated columns
    :rtype pyspark.sql.DataFrame
    """
    updated_df = df

    updated_df = expand_df(updated_df)
    for key in columns_dict.keys():
        updated_df = updated_df.withColumn(key, columns_dict.get(key))

    schema_as_dict = {}
    for full_name in updated_df.schema.names:
        schema_as_dict = add_col_to_dict(full_name, schema_as_dict)

    updated_df = updated_df.selectExpr(
        create_list_of_expr(schema_as_dict)
    )

    return updated_df
