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

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name='pay')
    async def pay(self, inter: disnake.AppCommandInteraction, member: disnake.Member, sum: int):
        try:
            author = inter.author
            checkUser(author.id)
            checkUser(member.id)
            cur.execute("SELECT * FROM users WHERE dsID = ?", (author.id,))
            depositAuthor = cur.fetchone()[1]
            cur.execute("SELECT * FROM users WHERE dsID = ?", (member.id,))
            depositMember = cur.fetchone()[1]
            if sum > depositAuthor:
                embed = disnake.Embed(
                    title="Недостаточно средств",
                    description="У вас на карте недостаточно средств"
                )
                await inter.response.send_message(embed=embed)
            elif sum < 0:
                embed = disnake.Embed(
                    title="Недопустимое значение",
                    description="Сумма меньше нуля, а это недопустимо"
                )
                await inter.response.send_message(embed=embed)
            else:
                cur.execute("UPDATE users SET deposit = ? WHERE dsID = ?", (depositAuthor-sum, author.id))
                cur.execute("UPDATE users SET deposit = ? WHERE dsID = ?", (depositMember+sum, member.id))
                con.commit()
                embed = disnake.Embed(
                    title="Перевод денег",
                    description=f"""
    Вы успешно передали {sum} монет {member.mention}
    """
                )
                await inter.response.send_message(embed=embed)
        except Exception:
            embedError = disnake.Embed(
                title="Ошибка",
                description="Произошла недпридвиденная ошибка. Повторите попытку позже"
            )
            await inter.response.send_message(embed=embedError)





def setup(bot):
    bot.add_cog(Pay(bot))