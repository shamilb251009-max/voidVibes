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

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name='deposit')
    async def deposit(self, inter: disnake.AppCommandInteraction, sum: int = None):
        try:
            member = inter.author
            checkUser(member.id)
            if sum is None:
                sum = checkUser(member.id)[2]
            if sum > checkUser(member.id)[2]:
                embed = disnake.Embed(
                    title="Недостаточно средств",
                    description="У вас нету столько монет в кошельке"
                )
                await inter.response.send_message(embed=embed)
            elif sum < 0:
                embed = disnake.Embed(
                    title="Недопустимое значение",
                    description="Значение меньше нуля, а это недопустимо"
                )
                await inter.response.send_message(embed=embed)
            else:
                cur.execute("SELECT deposit, wallet FROM users WHERE dsID = ?", (member.id,))
                res = cur.fetchone()
                cur.execute("UPDATE users SET wallet = ?, deposit = ? WHERE dsID = ?", (res[1]-sum, res[0]+sum, member.id))
                con.commit()
                embed = disnake.Embed(
                    title="Перевод денег на карту",
                    description=f"""
    Вы успешно перевели **{sum}** монет на карту
                """
                )
                await inter.response.send_message(embed=embed)
        except Exception:
                error = disnake.Embed(
        title="Ошибка", 
        description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
    )   
                await inter.response.send_message(embed=error)

def setup(bot):
    bot.add_cog(Deposit(bot))