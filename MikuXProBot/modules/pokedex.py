

import requests
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# REPO => Your Bots File Name
from MikuXProBot import pgram as app

# Function to retrieve Pokemon information from the API
def get_pokemon_info(name_or_id):
    base_url = "https://sugoi-api.vercel.app/pokemon"
    params = {}

    if isinstance(name_or_id, str):
        params["name"] = name_or_id
    elif isinstance(name_or_id, int):
        params["id"] = name_or_id
    else:
        return None

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()

    return None

# Command handler for the /pokedex command
@app.on_message(filters.command("pdx"))
async def pokedex_command(client: Client, message: Message) -> None:
    try:
        if len(message.command) > 1:
            pokemon_name_or_id = message.command[1]
            pokemon_info = get_pokemon_info(pokemon_name_or_id)

            if pokemon_info:
                # Extract relevant information from the API response
                pokemon = pokemon_info.get("name")
                pokedex_id = pokemon_info.get("id")
                height = pokemon_info.get("height")
                weight = pokemon_info.get("weight")
                abilities = [
                    ability["ability"]["name"]
                    for ability in pokemon_info.get("abilities", [])
                ]
                types = [
                    type_info["type"]["name"]
                    for type_info in pokemon_info.get("types", [])
                ]
                image_url = pokemon_info["sprites"]["other"]["official-artwork"][
                    "front_default"
                ]

                # Create the caption for the message
                caption = f"""
➖➖➖[ Ｐｏｋéｄｅｘ ]➖➖➖

╒═══「 **{pokemon.upper()}** 」

**Pokedex Id ➢** `{pokedex_id}`
**Type ➢** {', '.join(types)}
**Abilities ➢** {', '.join(abilities)}
**Height ➢** `{height}`
**Weight ➢** `{weight}`
"""

                # Create an inline keyboard for additional functionality
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            "STATS", callback_data=f"stats_{pokemon_name_or_id}"
                        )
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(inline_keyboard)

                # Reply with a photo and caption, along with the inline keyboard
                await message.reply_photo(
                    photo=image_url, caption=caption, reply_markup=reply_markup
                )
            else:
                await message.reply_text("Pokemon not found.")
        else:
            await message.reply_text("Please provide a Pokemon name or ID.")
    except KeyError:
        await message.reply_text("Pokemon information is incomplete or incorrect.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Callback query handler for the "STATS" button
@app.on_callback_query(filters.regex("^stats_"))
async def show_stats(client: Client, callback_query: CallbackQuery) -> None:
    try:
        pokemon_name_or_id = callback_query.data.split("_")[1]
        pokemon_info = get_pokemon_info(pokemon_name_or_id)

        if pokemon_info:
            # Extract the stats information from the API response
            stats = pokemon_info.get("stats")
            stats_text = "**Stats ➢**\n\n"

            # Format the stats information into text
            for stat in stats:
                stat_name = stat["stat"]["name"]
                base_stat = stat["base_stat"]
                stats_text += f"{stat_name.upper()}: {base_stat}\n"

            # Edit the message with the updated stats information
            await callback_query.edit_message_text(stats_text)
        else:
            await callback_query.message.reply_text("Pokemon not found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {str(e)}")
