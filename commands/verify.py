import disnake
from disnake.ext import commands

class Edit_verify(disnake.ui.View):
    def __init__(self, bot, user_id, values):
        self.bot = bot
        self.user_id = user_id
        self.values = values
        super().__init__()

    @disnake.ui.button(label="Отказать", style=disnake.ButtonStyle.red)
    async def no_verify(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await inter.response.edit_message(view=self)

        user = await inter.guild.fetch_member(self.user_id)
        await user.send(embed=disnake.Embed(description="```Вам отказали в верификации. Попробуйте подать снова```"))

    @disnake.ui.button(label="Одобрить", style=disnake.ButtonStyle.green)
    async def yes_verify(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        user = await inter.guild.fetch_member(self.user_id)
        gender = self.values[2]
        if gender == '0':
            await user.add_roles(await inter.guild.fetch_role(1470037242591576076), await inter.guild.fetch_role(1470013953487933495))
            await user.remove_roles(await inter.guild.fetch_role(1470013918586867732))
        else:
            await user.add_roles(await inter.guild.fetch_role(1470037124307882005), await inter.guild.fetch_role(1470013953487933495))
            await user.remove_roles(await inter.guild.fetch_role(1470013918586867732))
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await inter.response.edit_message(view=self)
        await user.send(embed=disnake.Embed(description="```Вам одобрили верификацию. Поздравляем!```"))




class Modal(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot

        components = [
            disnake.ui.TextInput(
                label="Введите ваш возраст",
                style=disnake.TextInputStyle.short,
                custom_id='Возраст'
            ),
            disnake.ui.TextInput(
                label="Откуда вы узнали о нас?",
                style=disnake.TextInputStyle.short,
                custom_id='Откуда он узнал о нас'
            ),
            disnake.ui.TextInput(
                label="Укажите ваш пол(0 - муж., 1 - жен.)",
                style=disnake.TextInputStyle.short,
                custom_id='Пол'
            ),

        ]

        super().__init__(title="Верификация", components=components)

    async def callback(self, interaction: disnake.ModalInteraction):
        await interaction.response.send_message("Спасибо за отправку формы. Ожидайте рассмотрения", ephemeral=True)
        embed = disnake.Embed(title=f"Заявка на верификацию")
        arr = []
        for k, v in interaction.text_values.items():
            embed.add_field(
                name=k,
                value=v,
                inline=False
            )
            arr.append(v)
        embed.add_field(
            name="От кого",
            value=interaction.author.mention,
            inline=False
        )

        staff_chat = await self.bot.fetch_channel(1470017010854265060)
        view = Edit_verify(self.bot, interaction.author.id, arr)
        await staff_chat.send(embed=embed, view=view)

class Button(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    @disnake.ui.button(label="Пройти верификацию", style=disnake.ButtonStyle.primary)
    async def button_func(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        modal = Modal(self.bot)
        await inter.response.send_modal(modal=modal)

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.slash_command(name='verify')
    async def verify(self, inter: disnake.AppCommandInteraction):
        view = Button(self.bot)
        await inter.response.send_message(embed=disnake.Embed(description="Чтобы пройти верификацию нажмите на кнопку ниже"), view=view)


def setup(bot):
    bot.add_cog(Verify(bot))