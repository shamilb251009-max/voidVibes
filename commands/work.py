import disnake
from disnake.ext import commands
import random
import sqlite3
import datetime as dt

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

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name='work', description="Получить деньги за работу(КД 30 мин.)")
    async def work(self, inter: disnake.AppCommandInteraction):
            try:
                member = inter.author
                checkUser(member.id)
                cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(member.id)[2]+random.randint(30, 500), member.id))
                cur.execute("SELECT * FROM users WHERE dsID = ?", (member.id,))
                res = cur.fetchone()
                if res[3] is None:
                    cur.execute("UPDATE users SET nextWork = ? WHERE dsID = ?", (dt.datetime.now() + dt.timedelta(minutes=30), member.id))
                    con.commit()
                    cur.execute("SELECT * FROM users WHERE dsID = ?", (member.id,))
                    embed = disnake.Embed(
                    title=f"Работа {random.choice(['на шахте', 'собирателем бутылок', 'художником', 'строителем'])}",
                    description=f"""
    Вы поработали на славу! Сегодня вы заработали **{random.randint(30, 500)}** монет
    """)
                    await inter.response.send_message(embed=embed, ephemeral=True)
                else:
                    if dt.datetime.now() >= dt.datetime.fromisoformat(res[3]):
                        cur.execute("UPDATE users SET nextWork = ? WHERE dsID = ?", (dt.datetime.now() + dt.timedelta(minutes=30), member.id))
                        con.commit()
                        embed = disnake.Embed(
                    title=f"Работа {random.choice(['на шахте', 'собирателем бутылок', 'художником', 'строителем'])}",
                    description=f"""
    Вы поработали на славу! Сегодня вы заработали **{random.randint(30, 500)}** монет
    """)
                        await inter.response.send_message(embed=embed, ephemeral=True)
                    else:
                        embed = disnake.Embed(description=f"Стоп... Подождите до {dt.datetime.fromisoformat(res[3]).strftime("%d.%m.%Y %H:%M")}")
                        await inter.response.send_message(embed=embed, ephemeral=True)
            except Exception:
                error = disnake.Embed(
        title="Ошибка", 
        description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
    )   
                await inter.response.send_message(embed=error, ephemeral=True)


def setup(bot):
    bot.add_cog(Work(bot))
        