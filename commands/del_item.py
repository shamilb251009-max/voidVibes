import disnake
from disnake.ext import commands
import sqlite3

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()

class Del_item(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='del_item')
    async def del_item(self, ctx, id: int):
        try:
            cur.execute("SELECT 1 FROM store WHERE id = ?", (id,))
            result = cur.fetchone()
            if result is None:
                await ctx.send(f"Предмет с ID = {id} не найден в таблице.")
            else:
                cur.execute("DELETE FROM store WHERE id = ?", (id,))
                con.commit()
                await ctx.send(f"Вы успешно удалили предмет с ID = {id}")
        except Exception:
            error = disnake.Embed(
            title="Ошибка", 
            description="Произошла недпридвиденная ошибка. Повторите попытку позже"    
            )   
            await ctx.send(embed=error)
            
def setup(bot):
    bot.add_cog(Del_item(bot))