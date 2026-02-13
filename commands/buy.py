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

class Buy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name='buy')
    async def buy(self, inter: disnake.AppCommandInteraction, id: int):
        try:
            checkUser(inter.author.id)
            cur.execute("SELECT * FROM store WHERE id = ?", (id,))
            result = cur.fetchone()
            amount = int(result[3])
            role_id = result[4]
            name = result[1]
            if amount > checkUser(inter.author.id)[2]:
                embed = disnake.Embed(
                    title="Недостаточно средств",
                    description="У вас недостаточно средств в кошельке, чтобы совершить покупку"
                )
                await inter.response.send_message(embed=embed)
            else:
                if role_id is None:
                    cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(inter.author.id)[2]-amount, inter.author.id))
                    con.commit()
                    await inter.response.send_message(f"Вы успешно купили товар **{name}** за {amount} монет")
                else:
                    cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(inter.author.id)[2]-amount, inter.author.id))
                    con.commit()
                    role = await inter.guild.fetch_role(role_id)
                    await inter.author.add_roles(role)
                    await inter.response.send_message(f"Вы успешно купили товар **{name}** за {amount} монет")
        except Exception:
            error = disnake.Embed(
            title="Ошибка", 
            description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
        )   
            await inter.response.send_message(embed=error)
    

def setup(bot):
    bot.add_cog(Buy(bot))