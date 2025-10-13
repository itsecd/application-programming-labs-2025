import re
"""
this module parses data.
"""



# parse data to user
def Parse_data(data) -> dict[str, str]:

    """
    This function translates text into a dictionary
    """


    pattern = r".+:."

    data = re.split(pattern, data, maxsplit=0)

    try: 
        user = {
            "index": data[0],
            "firstname": data[1],
            "secondname": data[2],
            "gender": data[3],
            "birthday": data[4],
            "credentials": data[5],
            "city": data[6],
        }
    
    except IndexError:
        print("error while parsing data:")
        print(data)
    return user


# parse user-credentials
def Parse_user(user) -> bool:
    
    """
    checks the dictionary value of email address
    """

    patter = r"\w+@(yandex|gmail|yaho|ssau|mail)(\.ru|\.com|\.mail)"
    if (re.findall(patter, user["credentials"])):
        return True
    return False




