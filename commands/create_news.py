import disnake
from disnake.ext import commands

class Modal(disnake.ui.Modal):
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel

        components = [
            disnake.ui.TextInput(
                label="Заголовок новости",
                style=disnake.TextInputStyle.short,
                custom_id="header"
            ),
            disnake.ui.TextInput(
                label="Текст новости",
                style=disnake.TextInputStyle.long,
                custom_id="text",
            ),
            disnake.ui.TextInput(
                label="Ссылка на картинку",
                style=disnake.TextInputStyle.short,
                custom_id="url",
                required=False
            )
        ]

        super().__init__(title="Новость", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
            try:
                embed = disnake.Embed(
                    title=f"{inter.text_values['header']}",
                    description=f"{inter.text_values['text']}"
                )
                embed.set_image(url=inter.text_values['url'])
                await self.channel.send('@everyone',embed=embed)
                await inter.response.send_message("Вы успешно отправили новость", ephemeral=True)
            except Exception:
                error = disnake.Embed(
        title="Ошибка", 
        description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
    )   
                await inter.response.send_message(embed=error, ephemeral=True)

class Create_news(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='create_news', description="Создать новость")
    async def create_news(self, inter: disnake.AppCommandInteraction, channel: disnake.TextChannel):
        modal = Modal(self.bot, channel)
        await inter.response.send_modal(modal=modal)


def setup(bot):
    bot.add_cog(Create_news(bot))