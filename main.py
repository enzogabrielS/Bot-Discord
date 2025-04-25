import asyncio
from datetime import datetime, timedelta, timezone
from email.mime import image
import discord
from discord.ext import commands
from pyexpat.errors import messages

intents = discord.Intents.all()
bot = commands.Bot(".", intents = intents)

@bot.event
async def on_ready():
    comandosSync = await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Swcty"))
    print('bot ready successfully')
    print(f"Sync commands: {len(comandosSync)} ")

@bot.event
async def on_raw_reaction_add(payload):
    try:
        channel = client.get_channel(payload.channel_id)
        member_name = payload.member.name if payload.member else "Unknown User"
        print(f"the user {member_name} do {payload.emoji} added on channel: {channel.name}")
    except AttributeError as e:
        print(f"Erro ao processar reação: {e}")


@bot.command()
async def ola(ctx: commands.Context):
    mention = ctx.author.mention
    server = ctx.guild
    await ctx.reply(f"Hello, user {mention}, by {server}")

@bot.command()
async def falar(ctx: commands.Context,*, texto):
    await ctx.reply(texto)

@bot.command()
async def somar(ctx: commands.Context,num1:int, num2:int):
    result = num1 + num2
    await ctx.reply(f"a soma de {num1} e {num2}, sera igual a {result}.")

@bot.command()
async def clear(ctx: commands.Context, quantidade:int = 100, limite:int = 1000):
    agora = datetime.now(timezone.utc)
    limite_tempo = agora - timedelta(days=14)

    mensagens_apagaveis = 0
    async for mensagem in ctx.channel.history(limit=limite):
        if mensagem.created_at > limite_tempo:
            mensagens_apagaveis += 1
    minha_embed = discord.Embed()
    minha_embed.title = "🧹 Apagando as mensagens... 🧹 "
    minha_embed.description = f"{mensagens_apagaveis} mensagens irão ser deletadas"
    await ctx.send(embed=minha_embed, delete_after=10)
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=quantidade)
    minha_embed = discord.Embed()
    minha_embed.description = f"{mensagens_apagaveis} mensagens foram apagadas"
    await ctx.send(embed=minha_embed, delete_after=10)

@bot.command()
async def pix(ctx: commands.Context):
    async def replybutton(interact: discord.Interaction):
        await interact.response.send_message("Pix: 8aa8a7c5-7ba8-4a80-996b-2c0e27b00486", ephemeral=True, delete_after=60)

    view = discord.ui.View()
    button = discord.ui.Button(label="🛒", style=discord.ButtonStyle.green)
    button_url = discord.ui.Button(label="@ezzgabb", style=discord.ButtonStyle.grey, url="https://www.instagram.com/ezzgabb/")
    button.callback = replybutton

    view.add_item(button)
    view.add_item(button_url)
    await ctx.reply(view=view)

@bot.command()
async def status(ctx: commands.Context):
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("@ezzgabb"))

@bot.command()
async def spam(ctx: commands.Context, mensagem, quantidade: int):
    try:
        if quantidade <= 1:
            await ctx.reply("O valor exige ser maior que 1.", ephemeral=True, delete_after=4)
            return

        await ctx.reply(f"Enviando {quantidade} vezes a sua mensagem...", ephemeral=True, delete_after=10)

        for _ in range(quantidade):
            await asyncio.sleep(3)
            await ctx.send(mensagem)

    except Exception as e:
        await ctx.reply(f"Ocorreu um erro: {e}", ephemeral=True, delete_after=10)

bot.run("MTM1NjA0NTcwODE1MDcwNjI3Ng.Ghv0YQ.-9UQErp7PIjtQP_srmGr_S4Oy03JnlQtWtUUKU")