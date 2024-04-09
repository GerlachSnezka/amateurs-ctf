import json
import os
from urllib.parse import unquote
from datetime import datetime

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def generate_writeup(data, me, year):
    categories = {}

    for challenge in data['data']:
        if challenge['id'] in [s['id'] for s in me['data']["solves"]]:
            category = challenge['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(challenge)

    for category, challenges in categories.items():
        category_dir = os.path.join(str(year), category.lower().replace(" ", "-")) 
        os.makedirs(category_dir, exist_ok=True)

        for challenge in challenges:
            name_decoded = unquote(challenge['name'])
            name_lowercase = name_decoded.lower() 
            name_with_dash = name_lowercase.replace(" ", "-")  
            challenge_file_path = os.path.join(category_dir, f"{name_with_dash}.md")

            with open(challenge_file_path, 'w') as f:
                f.write(f"---\n")
                f.write(f"title: \"{name_decoded}\"\n")
                f.write(f"description: \"{challenge['description'].split("\n")[0].strip()}\"\n")  
                f.write(f"points: {challenge['points']}\n")
                f.write(f"solves: {challenge['solves']}\n")
                f.write(f"author: nobody\n")
                f.write(f"---\n\n")
                f.write(f"yeh' {name_decoded}.... it was hard lol\n")
                

        with open(os.path.join(category_dir, 'README.md'), 'w') as readme_file:
            readme_file.write(f"# {category.capitalize()} Challenges\n\n")
            readme_file.write("List of challenges in this category:\n\n")
            for challenge in challenges:
                name_decoded = unquote(challenge['name'])
                name_with_dash = name_decoded.lower().replace(" ", "-")
                readme_file.write(f"- {name_decoded} - Solves: {challenge['solves']}\n")

    with open(os.path.join(str(year), 'README.md'), 'w') as year_readme_file:
        year_readme_file.write("# Challenge Writeup\n\n")

        for category, challenges in categories.items():
            year_readme_file.write(f"## {category.capitalize()} Challenges\n\n")

            for challenge in challenges:
                name_decoded = unquote(challenge['name'])
                name_with_dash = name_decoded.lower().replace(" ", "-")
                solved = challenge['id'] in [s['id'] for s in me['data']["solves"]]
                year_readme_file.write(f"- **{name_decoded}** ({challenge['points']} points) - Solved: {'✔' if solved else '❌'} - Solves: {challenge['solves']}\n\n")



def main():
    year = datetime.now().year
    data = load_data(f"{year}/data.json")
    me = load_data(f"{year}/me.json")
    generate_writeup(data, me, year)

    print("Writeup directory structure created successfully.")

if __name__ == "__main__":
    main()
