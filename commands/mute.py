import disnake
import os
from disnake.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='mute', description="Заглушить пользователя")
    @commands.has_permissions(mute_members=True)
    async def mute(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, time: int, reason: str = "Не указана"):
        try:
            if member == inter.author:
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Нельзя заглушить самого себя!"
                )
                await inter.response.send_message(embed=embedError, ephemeral=True)
            elif member == await self.bot.fetch_user(1468639801833160887):
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Я бот... Зачем меня заглушивать?"
                )
                await inter.response.send_message(embed=embedError, ephemeral=True)
            else:
                log = await self.bot.fetch_channel(os.getenv('MUTES'))
                await member.timeout(duration=time*60)
                embedMute = disnake.Embed(
                    title="Заглушка участника на сервере",
                    description=f"""
        Модератор **{inter.author.name}** заглушил участника **{member.name}**
        На **{time}** минут
        По причине: **{reason}**
        """
                )
                await inter.response.send_message(embed=embedMute)

                embedLog=disnake.Embed(
                    title="Заглушка участника",
                    description=f"""
    **Пользователь:**
    ```{member.name} | ID: {member.id}```

    **Модератор:**
    ```{inter.author.name} | ID: {inter.author.id}```

    **Срок:**
    ```{time} минут```

    **Причина:**
    ```{reason}```
            """
                )
                
                await log.send(embed=embedLog)
        except Exception:
            embedError = disnake.Embed(
                title="Ошибка",
                description="Произошла недпридвиденная ошибка. Повторите попытку позже"
            )
            await inter.response.send_message(embed=embedError, ephemeral=True)
    
    @mute.error
    async def mute_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embedError = disnake.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для использования команды"
            )
            await inter.response.send_message(embed=embedError, ephemeral=True)
            

def setup(bot):
    bot.add_cog(Mute(bot))