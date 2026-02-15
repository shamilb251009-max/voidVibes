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
    
class Rolepay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='rolepay', description="Выдать деньги всем обладателям определенной роли")
    @commands.has_permissions(administrator=True)
    async def rolepay(self, inter: disnake.AppCommandInteraction, role: disnake.Role, sum: int):
        members = role.members
        idMembers = [i.id for i in members]
        for id in idMembers:
            checkUser(id)
            cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(id)[2]+sum, id))
            con.commit()
        embed = disnake.Embed(
            title="Выдача монет",
            description=f"""
Вы успешно выдали всем пользователям с ролью {role.mention} по **{sum}** монет
"""
        )
        await inter.response.send_message(embed=embed, ephemeral=True)
        

def setup(bot):
    bot.add_cog(Rolepay(bot))