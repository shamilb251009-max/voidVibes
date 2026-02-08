import disnake
import os
from disnake.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = "Не указана"):
        try:
            if member == inter.author:
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Нельзя исключить самого себя!"
                )
                await inter.response.send_message(embed=embedError)
            elif member == await self.bot.fetch_user(1468639801833160887):
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Я бот... Зачем меня исключать?"
                )
                await inter.response.send_message(embed=embedError)
            else:
                log = await self.bot.fetch_channel(os.getenv('KICKS'))
                embedKick = disnake.Embed(
                    title="Исключение участника с сервера",
                    description=f"""
        Модератор **{inter.author.name}** исключил участника **{member.name}**
        По причине: **{reason}**
        """
                )
                await inter.response.send_message(embed=embedKick)

                embedLog=disnake.Embed(
                    title="Исключение участника",
                    description=f"""
    **Пользователь:**
    ```{member.name} | ID: {member.id}```

    **Модератор:**
    ```{inter.author.name} | ID: {inter.author.id}```

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
            await inter.response.send_message(embed=embedError)
    
    @kick.error
    async def kick_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embedError = disnake.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для использования команды"
            )
            await inter.response.send_message(embed=embedError)
            

def setup(bot):
    bot.add_cog(Kick(bot))