import disnake
from disnake.ext import commands
import sqlite3

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='shop')
    async def shop(self, inter: disnake.AppCommandInteraction):
        cur.execute("SELECT * FROM store")
        items = cur.fetchall()
        str = ""
        for i in items:
            if i[4] == None:
            # 0 - id; 1 - name; 2 - desc; 3 - amount; 4 - role_id
                str += f"""
    `[{i[0]}]`
    ```Название: {i[1]}```
    ```Описание: {i[2]}```
    ```Цена: {i[3]}```
    `Выдаваемая роль:` Отсутствует\n
    """
            else:
                str += f"""
    `[{i[0]}]`
    ```Название: {i[1]}```
    ```Описание: {i[2]}```
    ```Цена: {i[3]}```
    `Выдаваемая роль:` <@&{i[4]}>\n
    """
                await inter.response.send_message(embed=disnake.Embed(
                title="Магазин",
                description=str
            ))
                


def setup(bot):
    bot.add_cog(Shop(bot))