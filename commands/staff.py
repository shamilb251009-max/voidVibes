import disnake
from disnake.ext import commands
import os

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='staff')
    async def staff(self, inter: disnake.ApplicationCommandInteraction):
        mod1 = inter.guild.get_role(1468651280074539114)
        membersMod1 = mod1.members

        mod2 = inter.guild.get_role(1468651334398906438)
        membersMod2 = mod2.members

        mod3 = inter.guild.get_role(1468651373322305577)
        membersMod3 = mod3.members

        headDevs = inter.guild.get_role(1468651424521916610)
        membersHeadDev = headDevs.members
        lst1 = [member.mention for member in membersMod1]
        lst2 = [member.mention for member in membersMod2]
        lst3 = [member.mention for member in membersMod3]
        lstHeadDevs = [member.mention for member in membersHeadDev]
        await inter.response.send_message(embed=disnake.Embed(description=f"""                                        
**Head of Developers**
{'\n'.join(lstHeadDevs)}

**Модераторы третьего уровня**
{'\n'.join(lst3)}

**Модераторы второго уровня**
{'\n'.join(lst2)}

**Модераторы первого уровня**
{'\n'.join(lst1)}

"""))
                

def setup(bot):
    bot.add_cog(Staff(bot))