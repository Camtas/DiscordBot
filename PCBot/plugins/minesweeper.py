"""This module contains the bot's rock paper scissors minigame command."""

import random
import crescent
import hikari
import miru
from crescent.ext import docstrings
from PCBot.botdata import BotData
from typing import Optional

plugin = crescent.Plugin[hikari.GatewayBot, BotData]()

class Tile:
    """Class to store information about each tile"""
    
    tileID = 0
    uncovered = False
    flagged = False
    
    def __init__(self, tileID):
        self.tileID = tileID


tile_emojis = ['\N{LARGE YELLOW SQUARE}', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '\N{LARGE GREEN SQUARE}', '\N{BOMB}']
message_callbacks = []

class MineSweeperView(miru.View):
    """Miru view with button to draw up grid"""
    
    grid_size: int
    bomb_num: int
    
    message = ''
    grid = None
    
    def __init__(self, grid_size: int, bomb_num) -> None:
        super().__init__()
        self.grid_size = grid_size
        self.bomb_num = bomb_num
        self.grid = [ [Tile(0)]*grid_size for i in range(grid_size)]
        message_callbacks.append(self.on_message_create)
        self.setup()
        
    def setup(self) -> None:
        """ randomly scatters bombs in the grid """
        for bomb in range(self.bomb_num):
            x = (int)(random.random() * self.grid_size)
            y = (int)(random.random() * self.grid_size)
            if(self.grid[x][y].tileID != 10):
                self.grid[x][y].tileID = 10
            else:
                while(self.grid[x][y].tileID == 10):
                    x = (int)(random.random() * self.grid_size)
                    y = (int)(random.random() * self.grid_size)
                self.grid[x][y].tileID = 10
            # this is ugly I'm just lazy and couldn't think of a better way but it porbably works
            xUpper = (bool)(x-1 > -1)
            xLower = (bool)(x+1 < self.grid_size)
            yUpper = (bool)(y-1 > -1)
            yLower = (bool)(y+1 < self.grid_size)
            
            if(xUpper):
                if(self.grid[x-1][y].tileID < 8):
                    self.grid[x-1][y].tileID += 1
                if(yUpper):
                    if(self.grid[x-1][y-1].tileID < 8):
                        self.grid[x-1][y-1].tileID += 1
                if(yLower):
                    if(self.grid[x-1][y+1].tileID < 8):
                        self.grid[x-1][y+1].tileID += 1
            if(xLower):
                if(self.grid[x+1][y].tileID < 8):
                    self.grid[x+1][y].tileID += 1
                if(yUpper):
                    if(self.grid[x+1][y-1].tileID < 8):
                        self.grid[x+1][y-1].tileID += 1
                if(yLower):
                    if(self.grid[x+1][y+1].tileID < 8):
                        self.grid[x+1][y+1].tileID += 1
                        
            if(yUpper):
                if(self.grid[x][y-1].tileID < 8): 
                    self.grid[x][y-1].tileID += 1
            
            if(yLower):
                if(self.grid[x][y+1].tileID < 8):
                    self.grid[x][y+1].tileID += 1
    
    async def make_move(self, ctx: miru.ViewContext) -> None:
        self.message = ''

        """ draws up the board by editing the message """
        for i in range(self.grid_size):
            self.message += '\n'
            for j in range(self.grid_size):
                # add tile_emojis[tile.tileID] to string
                if(self.grid[i][j].uncovered == False):
                    self.message += f'{tile_emojis[9]}'
                else:
                    self.message += f'{tile_emojis[self.grid[i][j].tileID]}'
        await ctx.edit_response(f'{self.message}')
    
    
    @miru.button(label='Start', emoji=tile_emojis[10],
                 style=hikari.ButtonStyle.PRIMARY)
    async def rock_button(self, ctx: miru.ViewContext,
                          button: miru.Button) -> None:
        await self.make_move(ctx)

    async def on_message_create(self, event: hikari.MessageCreateEvent):
        if event.message.author.is_bot:
            return
        await event.message.respond("Hello!")

@plugin.include
@crescent.event
async def on_message_create(event: hikari.MessageCreateEvent):
    for callback in message_callbacks:
        await callback(event)


@plugin.include
@docstrings.parse_doc
@crescent.command(name='minesweeper', dm_enabled=False)
class MineSweeperCommand:
    """
    Play Minesweeper

    Requested by Camtas(camtas).
    Implemented by something sensible(somethingsensible) &
                   Camtas(camtas).

    Args:
        selected_grid_size: size of grid
        selected_bomb_num: number of bombs in game
    """

    selected_grid_size = crescent.option(int, default = 9, min_value=2, max_value=18)
    selected_bomb_num = crescent.option(int, default = 5, min_value=1, max_value=80)


    async def callback(self, ctx: crescent.Context) -> None:
        """Handle rpschallenge command being run by showing button view."""
        view = MineSweeperView(grid_size = self.selected_grid_size, bomb_num = self.selected_bomb_num)
        await ctx.respond(
          'Minesweeper',
          components=view
        )
        plugin.model.miru.start_view(view)
