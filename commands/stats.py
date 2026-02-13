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
        res = cur.execute("SELECT * FROM users WHERE dsID = ?", (member_id,))
        return res
    else:
        return result

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='stats')
    async def stats(self, inter: disnake.AppCommandInteraction, member: disnake.Member = None):
        try:
            if member is None:
                member = inter.author
            checkUser(member.id)
            cur.execute("SELECT * FROM users WHERE dsID = ?", (member.id,))
            result = cur.fetchone()
            status = ''
            date = ''
            cur.execute("SELECT * FROM marriages WHERE one_id = ? OR two_id = ?", (member.id, member.id))
            res = cur.fetchone()
            if res is None:
                status = "Не состоит в браке"
                date = "Не состоит в браке"
            else:
                date = result[2]
                if res[0] == member.id: status = await inter.guild.fetch_member(res[1])
                elif res[1] == member.id: status = await inter.guild.fetch_member(res[0])
            embed = disnake.Embed(
                title=f"Статистика {member.name}",
                description=f"""
    **Никнейм:** `{member.name}`
    **ID:** `{member.id}`
    **Баланс в кошельке:** `{result[2]}`
    **Баланс на карте:** `{result[1]}`
    **Женат(а) на:** `{status}`
    **Дата брака:** `{date}`
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
    bot.add_cog(Stats(bot))
    