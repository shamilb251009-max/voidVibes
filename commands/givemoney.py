import disnake
from disnake.ext import commands
import sqlite3

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()

def checkUser(member_id):
    cur.execute("SELECT * FROM users WHERE dsID = ?", (member_id, ))
    result = cur.fetchone()
    if result is None:
        cur.execute("INSERT INTO users (dsID, wallet, deposit, nextWork) VALUES (?,?,?,?)", (member_id, 0, 0, None))
        con.commit()
        cur.execute("SELECT * FROM users WHERE dsID = ?", (member_id,))
        return cur.fetchone()
    else:
        return result
    
class Givemoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name='givemoney', description="Выдать деньги пользователю")
    @commands.has_permissions(administrator=True)
    async def givemoney(self, inter: disnake.ApplicationCommandInteraction, sum: int, member: disnake.Member = None, type: int = commands.Param(
        choices=[
            disnake.OptionChoice('Deposit', 0),
            disnake.OptionChoice('Wallet', 1)
        ]
    )):
        if member is None:
            member = inter.author
        checkUser(member.id)
        if sum < 0:
            embed = disnake.Embed(
                title="Недопустимное значение",
                description="Сумма меньше нуля, а это недопустимо"
            )
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            cur.execute("SELECT * FROM users WHERE dsID = ?", (member.id,))
            res = cur.fetchone()
            if type == 0:
                cur.execute("UPDATE users SET deposit = ? WHERE dsID = ?", (res[1]+sum, member.id))
                con.commit()
                embed = disnake.Embed(
                    title="Выдача монет пользователю",
                    description=f"""
Вы успешно выдали **{sum}** монет пользователю
"""
                )
                await inter.response.send_message(embed=embed, ephemeral=True)
            else:
                cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (res[2]+sum, member.id))
                con.commit()
                embed = disnake.Embed(
                    title="Выдача монет пользователю",
                    description=f"""
Вы успешно выдали **{sum}** монет пользователю
"""
                )
                await inter.response.send_message(embed=embed, ephemeral=True)


    @givemoney.error
    async def kick_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            embedError = disnake.Embed(
                title="Ошибка",
                description="У вас недостаточно прав для использования команды"
            )
            await inter.response.send_message(embed=embedError, ephemeral=True)
            


def setup(bot):
    bot.add_cog(Givemoney(bot))