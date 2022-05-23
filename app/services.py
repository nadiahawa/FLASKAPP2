import requests as r



def getallpokes():
    pokemons_api = r.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=50')
    if pokemons_api.status_code == 200:
        pokemons_data = pokemons_api.json()
    else:
        return 'broken api'
    # name = pokemons_data['results'][0]['name']
    name = [v['name'] for v in pokemons_data['results']]
    url = [v['url'] for v in pokemons_data['results']]
    return {
        'name': name,
        'url' : url
        }

def morepokedata():
    pokemons_api = r.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=50')        
    if pokemons_api.status_code == 200:
        pokemons_api = pokemons_api.json()
    else:
        return 'broken'
    for pokemon in range(len(pokemons_api['results'])):
        pokname = pokemons_api['results'][pokemon]['name']
        url = pokemons_api['results'][pokemon]['url']
        urln = r.get(url)
        urln = urln.json()
        weight = urln['weight']
        all_abilities = [v['ability']['name']for v in urln['abilities']]
        pok_typ = [v['type']['name']for v in urln['types']]
        pokimon = [weight,all_abilities,pok_typ]
        final_weight = [pokimon[0]]
        final_abilities = [pokimon[1]]
        final_type = [pokimon[2]]
        listy = {
            'weight': final_weight,
            'abilities': final_abilities,
            'types': final_type
            }
        return listy
# pokemons_api = r.get('https://pokeapi.co/api/v2/pokemon/?offset=0&limit=898')        
# if pokemons_api.status_code == 200:
#     pokemons_api = pokemons_api.json()
# for pokemon in range(len(pokemons_api['results'])):
#     x = pokemons_api['results'][pokemon]['name']
#     all_pokemon.append(x)

# def morepokedata():
#     number_pokes = range(1127)
#     for x in number_pokes:
#         data = r.get('https://pokeapi.co/api/v2/pokemon/{x}')
#         if data.status_code == 200:
#             data = data.json()
#             data_games1 = data['base_experience']
#             data_games2 = data['weight']
#             data_games3 = data['height']
#             data_games4 = data['id']
#             data_games5 = data['types'][0]['type']['name']
#             data_games6 = [v['ability']['name'] for v in data['abilities']]
#             print(data_games1)


# morepokedata()