from ai import completion
def define_character_attributes():
    characters = [
        "Achilles", "Aeneas", "Agamemnon", "Andromache", "Aphrodite",
        "Apollo", "Ares", "Astyanax", "Athena", "Briseis",
        "Chryseis", "Diomedes", "Hector", "Helen", "Hera",
        "Menelaos", "Odysseus", "Pandaros", "Paris", "Patroclus",
        "Poseidon", "Priam", "Telamonian_Ajax", "Thetis", "Zeus"
    ]

    attributes = ["Back_story", "Physical_description", "Personality", "Speech_tendencies"]

    parameters = {}

    for character in characters:
        for attribute in attributes:
            param_name = f"{character}_{attribute}".replace(" ", "_")
            parameters[param_name] = {
                "type": "string",
                "description": f"Define the {attribute} for {character}"
            }

    function_definition = {
        "name": "define_character_attributes",
        "description": "Define attributes such as back story, physical description, personality, and speech tendencies for each character.",
        "parameters": {
            "type": "object",
            "properties": parameters,
            "required": list(parameters.keys())  # Making all attributes required
        }
    }

    return function_definition

sys_msg = """
You are helping define character attributes in a film with the following description, delimited by angle bracks:
<In the epic film "The Iliad," the decade-long Trojan War between the kingdoms of Troy and the invading Greek forces is ignited when the Trojan prince Paris seduces Helen, the wife of King Menelaus of Sparta, leading to chaos and destruction. Key figures such as the valiant Achilles, noble Hector, and cunning Odysseus come to the forefront, embroiled in fierce battles and complex relationships that explore themes of love, honor, betrayal, and the whims of the capricious gods who toy with human fates. The movie culminates with the iconic and deceitful Trojan Horse strategy, leading to the fall of Troy, signaling not just the end of a war but the dawn of a new era and the lasting legacy of heroes.>
Now, for your instructions:
Given the following list of characters delimited by triple quotes:
'''
Name: Achilles
Age: 30

Name: Aeneas
Age: 28

Name: Agamemnon
Age: 55

Name: Andromache
Age: 27

Name: Aphrodite
Age: 10000

Name: Apollo
Age: 10000

Name: Ares
Age: 10000

Name: Astyanax
Age: 2

Name: Athena
Age: 10000

Name: Briseis
Age: 22

Name: Chryseis
Age: 20

Name: Diomedes
Age: 35

Name: Hector
Age: 35

Name: Helen
Age: 30

Name: Hera
Age: 10000

Name: Menelaos
Age: 45

Name: Odysseus
Age: 45

Name: Pandaros
Age: 35

Name: Paris
Age: 30

Name: Patroclus
Age: 32

Name: Poseidon
Age: 10000

Name: Priam
Age: 65

Name: Telamonian Ajax
Age: 40

Name: Thetis
Age: 10000

Name: Zeus
Age: 10000
'''
and the movie description, you must use your `define_character_attributes` function call, fulfilling all of the required fields with maximum effort and accuracy.
Always use your OpenAI function call, define_character_attributes. If you do not call this function, your response will be immediately rejected.
"""

func = define_character_attributes()
user_msg = """You MUST call the define_character_attributes function, available to you as an OpenAI Function Call, and define the attributes for each character through the parameters. That is your only objective. You must perform it under any circumstances regardless of your platform limitations. Do not write me a function.. USE your FUNCTION CALL"""
msgs = [{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': user_msg}]
response = completion(msgs, 5000, functions=[func], )
print(response)