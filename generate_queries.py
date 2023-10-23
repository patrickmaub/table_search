


    

QUERY_FORMATTER_FUNCTION_CALL = {   "name": "generate_search_queries",
        "description": "The function you call when generating search queries to ensure consistent formatting and structure. When presented, you MUST call this function. The search queries you generate, reflect the level of specifity of the target cells. If you have many target cells, you try and make more general queries which can potentilly find answers to many of your questions.",
        "parameters": {
            "type": "object",
            "properties": { "query_1":{
                "type": "string",
                "description": f"The first of 5 search queries you generate in order to fill out the provided cells. Unique and original to the other queries and previous queries."
            }, "query_2":{
                "type": "string",
                "description": f"The second of 5 search queries you generate in order to fill out the provided cells. Unique and original to the other queries and previous queries."
            }, "query_3":{
                "type": "string",
                "description": f"The third of 5 search queries you generate in order to fill out the provided cells. Unique and original to the other queries and previous queries."
            }, "query_4":{
                "type": "string",
                "description": f"The fourth of 5 search queries you generate in order to fill out the provided cells. Unique and original to the other queries and previous queries."
            }, "query_5":{
                "type": "string",
                "description": f"The fifth of 5 search queries you generate in order to fill out the provided cells. Unique and original to the other queries and previous queries."
            }},
        }}