import requests

def get_all_characters():
    url = "https://rickandmortyapi.com/api/character/"
    all_characters = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_characters.extend(data['results'])
            url = data['info']['next']  # Get the next page URL
        else:
            print(f"Error: {response.status_code}")
            break
    return all_characters

def get_episode_info(episode_urls):
    episodes = []
    for episode_url in episode_urls:
        response = requests.get(episode_url)
        if response.status_code == 200:
            episode_data = response.json()
            episode_name = episode_data['name']
            episode_code = episode_data['episode']  # Format: "S01E01"
            episodes.append(f"{episode_code} - {episode_name}")
        else:
            print(f"Error fetching episode info: {response.status_code}")
    return episodes

def search_characters():
    while True:
        # Option to change filter variables before proceeding with the search
        confirm = input("Do you want to enter new filters? (yes/no): ").strip().lower()
        if confirm == 'yes':
            gender = input("Enter gender (or leave blank): ").strip() or None
            species = input("Enter species (or leave blank): ").strip() or None
            origin = input("Enter origin (or leave blank): ").strip() or None
            name = input("Enter name (or leave blank): ").strip() or None
            location = input("Enter location (or leave blank): ").strip() or None
        else:
            gender, species, origin, name, location = None, None, None, None, None

        # If no filters are provided, list all characters
        if not (gender or species or origin or name or location):
            all_characters = get_all_characters()
            for character in all_characters:
                print(f"Name: {character['name']}, Gender: {character['gender']}, Species: {character['species']}, Origin: {character['origin']['name']}, Location: {character['location']['name']}")
                episodes = get_episode_info(character['episode'])
                print(f"Appeared in: {', '.join(episodes)}")
        else:
            url = "https://rickandmortyapi.com/api/character/"
            params = {}

            # Only include filters if the user provides a value
            if gender:
                params['gender'] = gender
            if species:
                params['species'] = species
            if name:
                params['name'] = name

            response = requests.get(url, params=params)

            if response.status_code == 200:
                characters = response.json()['results']

                # Manually filter by location and origin
                for character in characters:
                    character_origin = character['origin']['name']
                    character_location = character['location']['name']

                    # Check if user-specified location and origin match
                    if location and location.lower() not in character_location.lower():
                        continue
                    if origin and origin.lower() not in character_origin.lower():
                        continue

                    print(f"Name: {character['name']}, Gender: {character['gender']}, Species: {character['species']}, Origin: {character_origin}, Location: {character_location}")

                    # Fetch episode details
                    episodes = get_episode_info(character['episode'])
                    print(f"Appeared in: {', '.join(episodes)}")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        # Ask if the user wants to search again or change filters
        again = input("Would you like to search for another character? (yes/no): ").strip().lower()
        if again == 'no':
            break
        elif again == 'yes':
            continue  # Restarts the entire search
        # If 'search' is chosen, it will continue with the current filters

# Run the function
search_characters()