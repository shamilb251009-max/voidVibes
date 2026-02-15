import disnake
from disnake.ext import commands

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='staff', description="Посмотреть список действующих модераторов")
    async def staff(self, inter: disnake.ApplicationCommandInteraction):
        owner = inter.guild.get_role(1458937520925577269) # Владелец сервера
        co_owner = inter.guild.get_role(1458937524100792360) # Зам владельца сервера
        curator = inter.guild.get_role(1458937527095394518) # Кураторы
        seniorModerator = inter.guild.get_role(1471917129358901389) # Старшие модераторы
        moderator = inter.guild.get_role(1458937530207699230)
        juniorModerator = inter.guild.get_role(1458937532472365108)
        ownerList = [member.mention for member in owner.members] if owner and owner.members else ['Отсутствует']
        co_ownerList = [member.mention for member in co_owner.members] if co_owner and co_owner.members else ['Отсутствует']
        curatorList = [member.mention for member in curator.members] if curator and curator.members else ['Отсутствует']
        senModeratorList = [member.mention for member in seniorModerator.members] if seniorModerator and seniorModerator.members else ['Отсутствует']
        moderatorList = [member.mention for member in moderator.members] if moderator and moderator.members else ['Отсутствует']
        juniorModeratorList = [member.mention for member in juniorModerator.members] if juniorModerator and juniorModerator.members else ['Отсутствует']

        await inter.response.send_message(embed=disnake.Embed(description=f"""                                        
**Владелец сервера**
{'\n'.join(ownerList)}

**Зам.Владельца сервера**
{'\n'.join(co_ownerList)}

**Кураторы**
{'\n'.join(curatorList)}

**Старшие модераторы**
{'\n'.join(senModeratorList)}

**Модераторы**
{'\n'.join(moderatorList)}

**Младшие модераторы**
{'\n'.join(juniorModeratorList)}

"""), ephemeral=True)
                

def setup(bot):
    bot.add_cog(Staff(bot))