import disnake
from disnake.ext import commands
import sqlite3
import os

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()

def add_zero(val):
    val = str(val)
    if len(val) == 1:
        return f"000{val}"
    elif len(val) == 2:
        return f"00{val}"
    elif len(val) == 3:
        return f"0{val}"
    else:
        return val

class Edit_ticket(disnake.ui.View):
    def __init__(self, bot, member, channel, id):
        self.bot = bot
        self.member = member
        self.channel = channel
        self.ticket_id = id
        super().__init__()
    @disnake.ui.button(label="Взять тикет", style=disnake.ButtonStyle.success)
    async def take_ticket(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        cur.execute("SELECT * FROM tickets WHERE ticketID = ?", (self.ticket_id,))
        ticketModerator = cur.fetchone()[2]
        if ticketModerator is None:
            cur.execute("UPDATE tickets SET modID = ? WHERE dsID = ?", (inter.author.id, self.member.id))
            con.commit()
            await inter.response.send_message("Вы взяли тикет на рассмотрение", ephemeral=True)

        else:
            await inter.response.send_message("Тикет уже находится на рассмотрении", ephemeral=True)

    @disnake.ui.button(label="Закрыть тикет", style=disnake.ButtonStyle.danger)
    async def close_ticket(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        cur.execute("SELECT * FROM tickets WHERE ticketID = ?", (self.ticket_id,))
        ticketModerator = cur.fetchone()[2]
        if ticketModerator == inter.author.id:
            await inter.response.send_message("Вы успешно закрыли тикет", ephemeral=True)
            str = ""
            async for message in inter.channel.history(limit=None):
                if message.author.id != 1468639801833160887:
                    str += f"**{message.author.name}**: {message.content}\n"
            log = await inter.guild.fetch_channel(os.getenv('TICKETS'))
            await self.channel.delete(reason="Закрытие тикета")
            await self.member.send(embed=disnake.Embed(
                title="Тикет закрыт модератором",
                description=f"""
```История сообщений:```
{str}
"""
            ))
            await log.send(embed=disnake.Embed(
                title=f"Закрыт тикет-{add_zero(self.ticket_id)}",
                description=f"""
Тикет рассматривал: {inter.author.mention} | `ID: {inter.author.id}`

```История сообщений:```
{str}
"""
            ))
            await self.member.send("`Ваш тикет был закрыт модератором!`")
            
        elif ticketModerator != inter.author.id and ticketModerator != None:
            await inter.response.send_message("Тикет рассматривается не вами", ephemeral=True)
        else:
            await inter.response.send_message("Сначала возьмите тикет на рассмотрение", ephemeral=True)
        
    


class TicketButton(disnake.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @disnake.ui.button(label="Создать обращение", style=disnake.ButtonStyle.primary)
    async def create(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        cur.execute("INSERT INTO tickets (dsID, modID) VALUES (?, ?)", (inter.author.id, None))
        con.commit()
        cur.execute("SELECT * FROM tickets WHERE dsID = ?", (inter.author.id,))
        res = cur.fetchall()
        channel = await inter.guild.create_text_channel(name=f"ticket-{add_zero(res[-1][0])}")
        view = Edit_ticket(self.bot, inter.author, channel=channel, id=res[-1][0])
        embed = disnake.Embed(
            title="Обращение",
            description="""
Вопрос пользователя:
```Тут какой-то вопрос```
"""
        )
        await channel.send(f"{inter.author.mention}", embed=embed, view=view)

class Ticketmenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ticketmenu')
    async def ticketmenu(self, ctx):
        view = TicketButton(self.bot)
        embed = disnake.Embed(
            title="Создания обращения",
            description="Чтобы создать обращение нажмите на кнопку ниже"
        )
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Ticketmenu(bot))