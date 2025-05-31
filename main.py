import asyncio
from datetime import datetime, timedelta, timezone
from email.mime import image
import discord
from IPython import embed
from discord.ext import commands
from pyexpat.errors import messages

intents = discord.Intents.all()
bot = commands.Bot("!", intents = intents)

@bot.event
async def on_ready():
    comandosSync = await bot.tree.sync()
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="Swcty"))
    print('bot ready successfully')
    print(f"Sync commands: {len(comandosSync)} ")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Comando não encontrado!", ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("Você não tem permissão para executar este comando!", ephemeral=True)
    else:
        raise error

@bot.event 
async def on_raw_reaction_add(payload):
    channel_send_id = "Your Channel ID without quotation marks here"
    try:
        channel = bot.get_channel(payload.channel_id)
        if not channel:
            print(f"Canal não encontrado: {payload.channel_id}")
            return

        channel_to_send = bot.get_channel(channel_send_id)
        if not channel_to_send:
            print(f"Canal de destino não encontrado: {channel_send_id}")
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except Exception as e:
            print(f"Erro ao buscar mensagem: {e}")
            return

        member_name = payload.member.name if payload.member else "Usuário Desconhecido"
        emoji = str(payload.emoji) if payload.emoji else "emoji desconhecido"

        await channel_to_send.send(
            f"O usuário {member_name} adicionou {emoji} no canal: {channel.name}"
        )
    except AttributeError as e:
        print(f"Erro ao processar reação (AttributeError): {e}")
    except Exception as e:
        print(f"Erro inesperado ao processar reação: {e}")

@bot.command()
async def Hello(ctx: commands.Context):
    mention = ctx.author.mention
    server = ctx.guild
    await ctx.reply(f"Hello, user {mention}, by {server}")

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="🏓Pong!", color=0x00ff00)
    embed.add_field(name="Latência do bot", value=f"{round(bot.latency * 1000)}ms")
    await ctx.send(embed=embed)
    print(f"Latência do bot: {round(bot.latency * 1000)}ms")

@bot.command()
async def falar(ctx: commands.Context,*, texto):
    await ctx.reply(texto)

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
@commands.has_permissions(moderate_members=True)
async def clearall(ctx):
    await ctx.channel.purge()

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

@bot.command()
async def status(ctx: commands.Context):
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("@ezzgabb"))

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member_to_kick: discord.Member, *, motivo=None):
    channel_send_id = 1365507156979355658

    # Verifica permissões do bot
    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.reply("Não tenho permissão para expulsar membros!", ephemeral=True)
        return

    # Verifica hierarquia de cargos
    if ctx.guild.me.top_role <= member_to_kick.top_role:
        await ctx.reply("Não posso expulsar um membro com cargo igual ou superior ao meu!", ephemeral=True)
        return

    # Obter canal para enviar a mensagem
    channel_to_send = bot.get_channel(channel_send_id)
    if not channel_to_send:
        await ctx.reply(f"Canal de logs não encontrado (ID: {channel_send_id})", ephemeral=True)
        return
    try:
        await member_to_kick.kick(reason=motivo)

        # Enviar mensagem no canal de logs
        await channel_to_send.send(
            f"**O usuário {member_to_kick.mention} foi expulso.**\n"
            f"**ID do Ex-membro: {member_to_kick.id}**\n"
            f"**Motivo: {motivo or 'Não especificado'}**\n"
            f"**Canal: {ctx.channel.name}**\n"
            f"**Por: {ctx.author.mention}**\n"
        )

        # Confirmar a ação
        await ctx.send(f"O usuário {member_to_kick.mention} foi expulso! Motivo: {motivo or 'Não especificado'}")

    except discord.Forbidden:
        await ctx.reply("Não tenho permissão para expulsar este membro!", ephemeral=True)
    except discord.HTTPException:
        await ctx.reply("Ocorreu um erro ao tentar expulsar o membro.", ephemeral=True)


@bot.command()
@commands.has_permissions(moderate_members=True)
async def ban(ctx, member_to_ban: discord.Member, *, motivo=None):
    channel_send_id = 1365507156979355658

    # Verifica permissões do bot
    if not ctx.guild.me.guild_permissions.ban_members:
        await ctx.reply("Não tenho permissão para banir membros!", ephemeral=True)
        return

    # Verifica hierarquia de cargos
    if ctx.guild.me.top_role <= member_to_ban.top_role:
        await ctx.reply("Não posso banir um membro com cargo igual ou superior ao meu!", ephemeral=True)
        return

    # Obter canal para enviar a mensagem
    channel_to_send = bot.get_channel(channel_send_id)
    if not channel_to_send:
        await ctx.reply(f"Canal de logs não encontrado (ID: {channel_send_id})", ephemeral=True)
        return

    try:
        await member_to_ban.ban(reason=motivo)

        # Enviar mensagem no canal de logs
        await channel_to_send.send(
            f"**O usuário {member_to_ban.mention} foi banido.**\n"
            f"**ID do Ex-membro: {member_to_ban.id}**\n"
            f"**Motivo: {motivo or 'Não especificado'}**\n"
            f"**Canal: {ctx.channel.name}**\n"
            f"**Por: {ctx.author.mention}**\n"
        )

        # Confirmar a ação
        await ctx.send(f"O usuário {member_to_ban.mention} foi banido! Motivo: {motivo or 'Não especificado'}")

    except discord.Forbidden:
        await ctx.reply("Não tenho permissão para banido este membro!", ephemeral=True)
    except discord.HTTPException:
        await ctx.reply("Ocorreu um erro ao tentar banido o membro.", ephemeral=True)

# Creator Ban e Creator Kick servem para quando voce nao tem as permissoes de administrador no servidor
@bot.command()
async def creatorban(ctx, member_to_ban: discord.Member):
    try:
        await member_to_ban.ban()

        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.reply("Não tenho permissão para banir membros!", ephemeral=True)
            return

        if ctx.guild.me.top_role <= member_to_ban.top_role:
            await ctx.reply("Não posso banir um membro com cargo igual ou superior ao meu!", ephemeral=True)
            return

        await ctx.reply(f"O usuário {member_to_ban.mention} foi banido!", ephemeral=True)
    except discord.Forbidden:
        await ctx.reply(f"Não foi possivel concluir essa ação", ephemeral=True)


@bot.command()
async def creatorkick(ctx, member_to_ban: discord.Member):
    try:

        if not ctx.guild.me.guild_permissions.ban_members:
            await ctx.reply("Não tenho permissão para kickar membros!", ephemeral=True)
            return

        if ctx.guild.me.top_role <= member_to_ban.top_role:
            await ctx.reply("Não posso kickar um membro com cargo igual ou superior ao meu!", ephemeral=True)
            return

        await member_to_ban.kick()
        await ctx.reply(f"O usuário {member_to_ban.mention} foi kickado!", ephemeral=True)

    except discord.Forbidden:
        await ctx.reply("Não foi possível concluir essa ação", ephemeral=True)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name} - Informações do servidor", color=0x00ff00)
    embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="ID", value=guild.id, inline=False)
    embed.add_field(name="Owner", value=guild.owner, inline=False)
    embed.add_field(name="Criador", value=guild.owner, inline=False)
    embed.add_field(name="Membros", value=guild.member_count, inline=False)
    embed.add_field(name="Cargos", value=len(guild.roles), inline=False)
    embed.add_field(name="Canais", value=len(guild.channels), inline=False)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(moderate_members=True)
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    roles = [role for role in member.roles]
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"Informações do usuário {member}")
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"ID: {member.id}")
    embed.add_field(name="Nome de Usuário", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Status", value=member.status, inline=False)
    embed.add_field(name="Cargos", value=" ".join([role.mention for role in roles]), inline=False)
    embed.add_field(name="Criado em", value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Entrou em", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author
    embed = discord.Embed(title=f"{member.name}'s avatar")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def ajuda(ctx):
    try:
        view = discord.ui.View()
        botao = discord.ui.Button(
            label="Source do bot!", 
            url="https://github.com/enzogabrielS/Bot-Discord",
            style=discord.ButtonStyle.green
        )
        embed = discord.Embed(
            title="Comandos do Bot", 
            description="Comandos disponíveis no bot:", 
            color=0x00ff00
        )
        embed.add_field(name="!ping", value="Verifica se o bot está online.", inline=False)
        embed.add_field(name="!clear [quantidade]", value="Limpa a quantidade de mensagens especificada.", inline=False)
        embed.add_field(name="!spam [mensagem] [quantidade]", value="Envia a mensagem especificada [quantidade] vezes.", inline=False)
        embed.add_field(name="!status", value="Ativa ou desativa o status do bot.", inline=False)
        embed.add_field(name="!clearall", value="Limpa todas as mensagens do canal.", inline=False)
        embed.add_field(name="!kick [membro] [motivo](opcional)", value="Expulsa um membro do servidor.", inline=False)
        embed.add_field(name="!ban [membro] [motivo](opcional)", value="Bane um membro do servidor.", inline=False)
        embed.add_field(name="!serverinfo", value="Exibe informações do servidor.", inline=False)
        embed.add_field(name="!userinfo [membro] (opcional)", value="Exibe informações do usuário.", inline=False)
        embed.add_field(name="!avatar [membro] (opcional)", value="Exibe o avatar do usuário.", inline=False)
        embed.add_field(name="!falar [texto]", value="Fala o texto especificado.", inline=False)
        embed.add_field(name="!ajuda", value="Exibe essa mensagem de ajuda.", inline=False)
        embed.set_footer(text="Desenvolvido por enzo!")
        view.add_item(botao)
        await ctx.send(embed=embed, view=view)
    except discord.Forbidden:
        await ctx.reply("Não foi possível concluir essa ação", ephemeral=True)
    except discord.HTTPException:
        await ctx.reply("Erro ao enviar a mensagem. Tente novamente.", ephemeral=True)
    except Exception as e:
        await ctx.reply(f"Ocorreu um erro inesperado: {str(e)}", ephemeral=True)


bot.run("")
