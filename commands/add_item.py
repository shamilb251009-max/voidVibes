import disnake
from disnake.ext import commands
import sqlite3

con = sqlite3.connect("C:/Users/shamil/Desktop/devtbot/db/economycs.sqlite")
cur = con.cursor()


class Add_item(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='add_item')
    async def add_item(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        embed=disnake.Embed(
            title="Карточка товара",
            description=f""""""
        )
        msg = await ctx.send(embed=embed)

        await ctx.send("Введите название товара:")
        name = await self.bot.wait_for('message', check=check, timeout=60)
        embed.add_field(
            name="Название",
            value=name.content,
            inline=False
        )
        await msg.edit(embed=embed)
        await ctx.send("Введите стоимость товара: ")
        amount = await self.bot.wait_for('message', check=check, timeout=60)
        embed.add_field(
            name="Стоимость",
            value=amount.content,
            inline=False
        )
        await msg.edit(embed=embed)
        await ctx.send("Введите описание товара: ")
        desc = await self.bot.wait_for('message', check=check, timeout=60)
        embed.add_field(
            name="Описание",
            value=desc.content,
            inline=False
        )
        await msg.edit(embed=embed)
        await ctx.send("Какая роль будет выдаваться после покупки(если никакая отправьте skip)")
        role = await self.bot.wait_for('message', check=check, timeout=60)
        if role.content.lower() == 'skip' or role.content.lower() == '-':
            embed.add_field(
                name="Роль",
                value="Отсутствует",
                inline=False
            )
            cur.execute("INSERT INTO store (name, desc, amount, role_id) VALUES (?,?,?,?)", (name.content, desc.content, int(amount.content), None))
            con.commit()
        else:
            embed.add_field(
                name="Роль",
                value=role.content,
                inline=False
            )
            cur.execute("INSERT INTO store (name, desc, amount, role_id) VALUES (?,?,?,?)", (name.content, desc.content, int(amount.content), int(role.content.replace('<@&', '').strip('>'))))
            con.commit()
        await msg.edit(embed=embed)
        await ctx.send("Спасибо за ответы. Товар успешно создан")



def setup(bot):
    bot.add_cog(Add_item(bot))