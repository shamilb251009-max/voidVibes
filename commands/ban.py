import disnake
import os
from disnake.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='ban', description="Заблокировать пользователя на сервере")
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, time: int, reason: str = "Не указана"):
        try:
            if member == inter.author:
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Нельзя заблокировать самого себя!"
                )
                await inter.response.send_message(embed=embedError, ephemeral=True)
            elif member == await self.bot.fetch_user(1468639801833160887):
                embedError = disnake.Embed(
                    title="Ошибка",
                    description="Я бот... Зачем меня блокировать?"
                )
                await inter.response.send_message(embed=embedError, ephemeral=True)
            else:
                log = await self.bot.fetch_channel(os.getenv('BANS'))
                embedBan = disnake.Embed(
                    title="Блокировка участника на сервере",
                    description=f"""
        Модератор **{inter.author.name}** заблокировал участника **{member.name}**
        На **{time}** дней
        По причине: **{reason}**
        """
                )
                await inter.response.send_message(embed=embedBan)

                embedLog=disnake.Embed(
                    title="Блокировка участника",
                    description=f"""
    **Пользователь:**
    ```{member.name} | ID: {member.id}```

    **Модератор:**
    ```{inter.author.name} | ID: {inter.author.id}```

    **Срок:**
    ```{time} дней```

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
    
    @ban.error
    async def ban_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embedError = disnake.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для использования команды"
            )
            await inter.response.send_message(embed=embedError, ephemeral=True)
            

def setup(bot):
    bot.add_cog(Ban(bot))