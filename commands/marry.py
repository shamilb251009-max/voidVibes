import disnake
from disnake.ext import commands
import sqlite3
import asyncio
import datetime as dt

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()


class Accept(disnake.ui.View):
    def __init__(self, member, author):
        super().__init__()
        self.member = member
        self.author = author

    @disnake.ui.button(label="Согласиться", style=disnake.ButtonStyle.green)
    async def accept(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id == self.member.id:
            cur.execute("INSERT INTO marriages (one_id, two_id, date) VALUES (?,?,?)", (self.member.id, self.author.id, dt.datetime.now()))
            con.commit()
            embed = disnake.Embed(
                title="Брак",
                description=f"""
    Поздравляем {self.author.mention} и {self.member.mention} с браком!
    """
            )
            for child in self.children:
                if isinstance(child, disnake.ui.Button):
                    child.disabled = True
            await inter.response.edit_message(view=self)
            await inter.followup.send(embed=embed)
        else:
            await inter.response.send_message("Предложение было отправлено не вам!", ephemeral=True)
    
    @disnake.ui.button(label="Отказаться", style=disnake.ButtonStyle.red)
    async def no_accept(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id == self.member.id:    
            for child in self.children:
                if isinstance(child, disnake.ui.Button):
                    child.disabled = True
            await inter.response.edit_message(view=self)
            await inter.followup.send("Вы отказались от предложения", ephemeral=True)
        else:
            await inter.response.send_message("Предложение было отправлено не вам!", ephemeral=True)

class Marry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='marry', description="Предложить пользователю брак")
    async def marry(self, inter: disnake.AppCommandInteraction, member: disnake.Member):
        if member == inter.author:
            await inter.response.send_message("Нельзя отправить предложение самому себе!", ephemeral=True)
        else:
            cur.execute("SELECT * FROM marriages WHERE one_id = ?", (inter.author.id,))
            res1 = cur.fetchone()
            cur.execute("SELECT * FROM marriages WHERE two_id = ?", (inter.author.id,))
            res2 = cur.fetchone()
            if res1 is None and res2 is None:
                await inter.response.defer()
                view = Accept(member, inter.author)
                msg = await inter.followup.send(f"{member.mention} вам {inter.author.mention} предложил вступить в брак", view=view)
                await asyncio.sleep(30)
                await msg.edit(content=f"Время вышло...", view=None)
            else:
                await inter.response.send_message("Вы или пользователь уже в браке, нельзя отправлять предложение....", ephemeral=True)


def setup(bot):
    bot.add_cog(Marry(bot))