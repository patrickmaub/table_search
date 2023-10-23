def table_to_function_params(target_cells):
    """
    Convert the table structure into a function params format.
    
    Args:
        table_structure (dict): The table structure to convert.

    Returns:
        dict: The converted table structure in function params format.
    """

    str_row_columns = []
    for cell in target_cells:
        str_row_columns.append({"name": f"{cell[0]}_{cell[1]}", "description": f"Accurate, context-aware value for {cell[0]} in column {cell[1]}. Must be extracted directly from the `External Context` provided in the prompt. Otherwise set to 'null'."})
    # Extracting the parameters from the table structure
    parameters = {}
    for cell in target_cells:
        parameters[f"{cell[0]}_{cell[1]}_context_verifier_snippet"] = {
        "type": "string",
        "description": f"Used to verify that the answer extracted for '{cell[0]}_{cell[1]}' {cell[0]} in column {cell[1]}. Repeat, word for word, the snippet of context from which the value was retrieved. Again, snippet of context, verbatim, in the value of this field."
        }
    for val in str_row_columns:
        parameters[val["name"]] = {
            "type": "string",
            "description": val["description"]
        }
        #add to parameters, for each cell, a citation parameter.

    # Construct the function definition
    function_definition = {
        "name": "fill_cells",
        "description": "Assign values to cells based on the context provided in the prompt. For each cell you need to fill out, there is a pair of parameters: the first is the value you need to fill in, which must be retrieved from the context provided in the user's prompt, and the second is the context verifier snippet. The context verifier snippet is used to verify that the answer extracted for the cell is correct. Repeat, word for word, the snippet of context from which the value was retrieved.",
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": []
        }
    }

    return function_definition

def create_no_external_context_function_call():
    function_definition = {
    "name": "external_context_not_relevant",
    "description": "Indicate that the external context provided does not contain relevant information for any of the target cells. This function should be called when, after thorough analysis, you determine that the context material lacks data necessary for completing the table cells.",
    "parameters": {
        "type": "object",
        "properties": {
            "no_relevant_info": {
                "type": "boolean",
                "description": "A flag that should always be set to true when calling this function, indicating that the external context was indeed irrelevant for the task at hand."
            },
            "explanation": {
                "type": "string",
                "description": "A detailed explanation clarifying why the provided external context did not contain necessary information. This should highlight what was missing in the context that made it insufficient for the task."
            }
        },
        "required": ["no_relevant_info", "explanation"]
    }
}

    return function_definition
def create_queries_params(table_structure):
    """
    Define the function parameters for the create_queries function call.
    
    Args:
        table_structure (dict): The table structure based on which the queries should be created.

    Returns:
        dict: The function definition for create_queries.
    """
    # Extracting the parameters from the table structure
    parameters = {}
    for row_name, columns in table_structure.items():
        for column_name in columns:
            # Concatenate row_name with column_name using "_" as a separator
            param_name = f"{row_name}_{column_name}".replace(" ", "_")
            parameters[param_name] = {
                "type": "string",
                "description": f"Search query for {row_name} in column {column_name}"
            }

    # Construct the function definition
    function_definition = {
        "name": "create_queries",
        "description": "Generate search queries to fill the table data.",
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": []
        }
    }

    return function_definition
