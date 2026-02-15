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
    @commands.command(name='buy')
    async def buy(self, ctx, id: int):
        try:
            checkUser(ctx.author.id)
            cur.execute("SELECT * FROM store WHERE id = ?", (id,))
            result = cur.fetchone()
            amount = int(result[3])
            role_id = result[4]
            name = result[1]
            if amount > checkUser(ctx.author.id)[2]:
                embed = disnake.Embed(
                    title="Недостаточно средств",
                    description="У вас недостаточно средств в кошельке, чтобы совершить покупку"
                )
                await ctx.send(embed=embed)
            else:
                if role_id is None:
                    cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(ctx.author.id)[2]-amount, ctx.author.id))
                    con.commit()
                    await ctx.send(f"Вы успешно купили товар **{name}** за {amount} монет", ephemeral=True)
                else:
                    cur.execute("UPDATE users SET wallet = ? WHERE dsID = ?", (checkUser(ctx.author.id)[2]-amount, ctx.author.id))
                    con.commit()
                    role = await ctx.guild.fetch_role(role_id)
                    await ctx.author.add_roles(role)
                    await ctx.send(f"Вы успешно купили товар **{name}** за {amount} монет", ephemeral=True)
        except Exception:
            error = disnake.Embed(
            title="Ошибка", 
            description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
        )   
            await ctx.send(embed=error, ephemeral=True)
    

def setup(bot):
    bot.add_cog(Buy(bot))