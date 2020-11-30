# Importing necessary libraries
import os
import asyncio
import random
import discord
import theGameClass

# Setting up the client
client = discord.Client()

# Defining some constants
ME         = client.get_user(531401464648695808)
ADMIN_CODE = random.randint(0,999999999)
with open("token.txt") as f:    # Getting the token from token.txt
    TOKEN = f.read().rstrip("\n")

# Defining game related varibles
in_game = False
game = theGameClass.dogeTheAsteroids()

# Printing what server's its connected to once connected
@client.event
async def on_ready():
    for i in client.guilds:
        print("Connected to: '"+ str(i) + "'")
    print("Admin code:", ADMIN_CODE)

# Do stuff when the bot recives a message
@client.event
async def on_message(message):
    # Ignore the bot's messages
    if message.author == client.user:
        return
    # Globalize important variables
    global in_game, game

    # Start a game if not in any game and the correct command is given    
    if not in_game:
        if message.content.startswith("GAMESTART"):
            in_game = True
            print("Game Started")
            
            game.update_screen()
            screen = game.get_screen()
            gameScrn = await message.channel.send("```css\n{Score: "+str(game.score)+"}\n"+screen+"```")
            game.run = True
            game.player = message.author

            while game.run:
                game.update_screen()
                screen = game.get_screen()
                await gameScrn.edit(content="```css\n{Score: "+str(game.score)+"}\n"+screen+"```")
                game.score += 1

                if game.collision_check():
                    in_game = False
                    await message.channel.send(f"Game Ended\nScore: {game.score}")
                    game = theGameClass.dogeTheAsteroids()
                    break

                # Delay so the game runs at more stable FPS and to make the game easier
                tmp1 = 2-client.latency
                if tmp1 > 0: await asyncio.sleep(tmp1)
    else:
        # Delete all messages so the game screen does'nt go out of the window
        await message.delete()

        # Stop the game and display the score if the user wants to
        if message.content.startswith("GAMESTOP") and message.author == game.player:
            in_game = False
            await message.channel.send(f"Game Ended\nScore: {game.score}")
            game = theGameClass.dogeTheAsteroids()
        
        elif message.content == "W":
            game.dir -= 1
        elif message.content == "S":
            game.dir += 1

# Run the bot so all the hard work comes to pay
client.run(TOKEN)