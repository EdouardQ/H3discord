import discord

color = 0xFF6500

key_features = {
    'temp' : 'Température',
    'feels_like' : 'Ressentie',
    'temp_min' : 'Minimum température',
    'temp_max' : 'Maximum température'
}

def parse_data(data):
    del data['humidity']
    del data['pressure']
    return data

def weather_message(data, location):
    location = location.title()
    message = discord.Embed(
        title=f'{location} Méteo',
        description=f'Voici la météo vers {location}.',
        color=color
    )
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message

def error_message(location):
    location = location.title()
    return discord.Embed(
        title='Error',
        description=f'Il y a une erreur dans la récupération des données de la ville : {location}.',
        color=color
    )