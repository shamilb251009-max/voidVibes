import disnake
from disnake.ext import commands
import sqlite3

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()

class Accept(disnake.ui.View):
    def __init__(self, member):
        super().__init__()
        self.member = member
    @disnake.ui.button(label="Да", style=disnake.ButtonStyle.green)
    async def accept(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await inter.response.edit_message(view=self)
        cur.execute("DELETE FROM marriages WHERE one_id = ? OR two_id = ?", (self.member.id, self.member.id))
        con.commit()
        await inter.followup.send("Вы развелись!", ephemeral=True)

    @disnake.ui.button(label="Нет", style=disnake.ButtonStyle.red)
    async def no_accept(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await inter.response.edit_message(view=self)
        await inter.followup.send("Вы отказались от развода", ephemeral=True)


class Divorce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='divorce')
    async def divorce(self, inter: disnake.AppCommandInteraction):
        cur.execute("SELECT * FROM marriages WHERE one_id = ? OR two_id = ?", (inter.author.id, inter.author.id))
        result = cur.fetchone()
        if result is None:
            await inter.response.send_message("Вы не состоите в браке", ephemeral=True)
        else:
            view = Accept(inter.author)
            await inter.response.send_message('Вы уверены, что хотите развестись?', view=view)


def setup(bot):
    bot.add_cog(Divorce(bot))