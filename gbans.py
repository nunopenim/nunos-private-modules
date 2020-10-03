# Copyright 2020 nunopenim @github
#
# Licensed under the DBADPL-B (Don't Be A Dick Public License B), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBADPL-B (So use it freely, but if you make a
# shitload of cash, buy me a beer or a pizza. Thanks.

from userbot import tgclient
from telethon.events import NewMessage
from userbot.include.aux_funcs import fetch_user
from userbot.config import GbanConfigs as cfg

GBAN = cfg.GBAN
GBAN_BOT_IDS = cfg.GBAN_BOT_IDS

@tgclient.on(NewMessage(pattern=r"^\.gban(?: |$)(.*)", outgoing=True))
async def gbanner(request):
    if not GBAN:
        await request.edit("`You haven't enable the gban router in config.py!`")
        return
    message = request.pattern_match.group(1)
    args = message.split()
    response = ''
    user = await fetch_user(request, full_user=True, get_chat=False)
    if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
        await request.edit("`I am gonna gban myself because my owner is an idiot (give me a proper username ffs!)`")
        return
    user = str(user.user.id)
    if len(args) >= 2 and not request.reply_to_msg_id:
        reason = str(message.split(' ', 1)[1])
    elif len(args) == 1 and not request.reply_to_msg_id:
        reason = ""
    elif len(args) == 0 and not request.reply_to_msg_id:
        await request.edit("`Lemme gban you for not giving a proper username!`")
        return
    else:
        reason = message
    gbantext = '/gban ' + user + ' ' + reason
    for i in GBAN_BOT_IDS:
        async with tgclient.conversation(i) as conv:
            await conv.send_message(gbantext)
            x = await conv.get_response()
            if x:
                pass
            else:
                x = i + '  didn\'t respond'
        response += i + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
    await request.edit("`" + response + "`")
    return

@tgclient.on(NewMessage(pattern=r"^\.ungban(?: |$)(.*)", outgoing=True))
async def ungbanner(request):
    if not GBAN:
        await request.edit("`You haven't enable the gban router in config.py!`")
        return
    message = request.pattern_match.group(1)
    args = message.split()
    response = ''
    user = await fetch_user(request, full_user=True, get_chat=False)
    if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
        await request.edit("`I am gonna gban myself because my owner is an idiot (give me a proper username ffs!)`")
        return
    user = str(user.user.id)
    if len(args) >= 2 and not request.reply_to_msg_id:
        reason = str(message.split(' ', 1)[1])
    elif len(args) == 1 and not request.reply_to_msg_id:
        reason = ""
    elif len(args) == 0 and not request.reply_to_msg_id:
        await request.edit("`Lemme gban you for not giving a proper username!`")
        return
    else:
        reason = message
    gbantext = '/ungban ' + user + ' ' + reason
    for i in GBAN_BOT_IDS:
        async with tgclient.conversation(i) as conv:
            await conv.send_message(gbantext)
            x = await conv.get_response()
            if x:
                pass
            else:
                x = i + '  didn\'t respond'
        response += i + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
    await request.edit("`" + response + "`")
    return

@tgclient.on(NewMessage(pattern=r"^\.gkick(?: |$)(.*)", outgoing=True))
async def ungkicker(request):
    if not GBAN:
        await request.edit("`You haven't enable the gban router in config.py!`")
        return
    message = request.pattern_match.group(1)
    args = message.split()
    response = ''
    user = await fetch_user(request, full_user=True, get_chat=False)
    if str(type(user)) != '<class \'telethon.tl.types.UserFull\'>':
        await request.edit("`I am gonna gkick myself because my owner is an idiot (give me a proper username ffs!)`")
        return
    user = str(user.user.id)
    if len(args) >= 2 and not request.reply_to_msg_id:
        reason = str(message.split(' ', 1)[1])
    elif len(args) == 1 and not request.reply_to_msg_id:
        reason = ""
    elif len(args) == 0 and not request.reply_to_msg_id:
        await request.edit("`Lemme gkick you for not giving a proper username!`")
        return
    else:
        reason = message
    gbantext = '/gkick ' + user + ' ' + reason
    for i in GBAN_BOT_IDS:
        async with tgclient.conversation(i) as conv:
            await conv.send_message(gbantext)
            x = await conv.get_response()
            if x:
                pass
            else:
                x = i + '  didn\'t respond'
        response += i + ': ' + x.text.replace("**", "").replace("`", "").replace("tg://user?id=", "") + '\n\n'
    await request.edit("`" + response + "`")
    return
