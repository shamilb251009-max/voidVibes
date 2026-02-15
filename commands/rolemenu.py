import disnake
from disnake.ext import commands

class Del_Add_Role(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        self.newsrole = 1458937570573422809
        super().__init__()
    @disnake.ui.button(label="✔ Получить/Снять роль", style=disnake.ButtonStyle.secondary)
    async def edit_role(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        role = await inter.guild.fetch_role(self.newsrole)
        if role not in inter.author.roles:
            await inter.author.add_roles(role)
            await inter.response.send_message("Вам успешно выдана роль", ephemeral=True)
        else:
            await inter.author.remove_roles(role)
            await inter.response.send_message("У вас успешно снята роль", ephemeral=True)


class Rolemenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='rolemenu')
    async def rolemenu(self, ctx):
        view = Del_Add_Role(self.bot)
        await ctx.send(embed=disnake.Embed(
            title="Получение роли",
            description="Нажми на кнопку ниже, чтобы получить роль"
        ), view=view)

def setup(bot):
    bot.add_cog(Rolemenu(bot))