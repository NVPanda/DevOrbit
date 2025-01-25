# utf-8
import re

IMPROPER_KEYWORDS = [
    "adult", "porn", "xxx", "18+", "nsfw", "sex", "erotica", "xvideos"
]

def ValidatesLinks(github, linkedin, site):
    """
    Valida os links fornecidos (GitHub, LinkedIn e site pessoal) com base em regex.
    Retorna um dicionário indicando quais links são válidos.
    """

    github_regex = r"^https:\/\/(www\.)?github\.com\/[\w-]+(\/[\w-]+)?\/?$"
    linkedin_regex =  r"^https:\/\/(www\.)?linkedin\.com\/[\w-]+(\/[\w-]+)?\/?$"
    site_regex = r"^(https?:\/\/)?(www\.)?[\w\-]+\.[a-z]{2,}(\.[a-z]{2,})?(\/[\w\-]*)*\/?$"

    for text_in_link in IMPROPER_KEYWORDS:
        if text_in_link in github:
            return f"Link to github and invalid", False
        
        elif text_in_link in linkedin:
            return "Link to linkedin and invalid", False
        
        elif text_in_link in site:
            return f"Link to site and invalid", False
        
        

    results = {
        "github_valid": re.match(github_regex, github) is not None ,
        "linkedin_valid": re.match(linkedin_regex, linkedin) is not None,
        "site_regex": re.match(site_regex, site) is not None
    }

    return results

var = ValidatesLinks(
    github='https://github.com/gilderlan',
    linkedin="https://linkedin.com/in/gilderlan",
    site= ''

)

print(var)