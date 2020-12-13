# Copyright 2020 githubcatw @github
# Copyright 2020 nunopenim @github
#
# Licensed under the DBBPL
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBBPL

from userbot import tgclient, MODULE_DESC, MODULE_DICT, MODULE_INFO
from userbot.include.aux_funcs import module_info
from telethon.events import NewMessage
from os.path import basename
import io
import math
import random
import urllib.request
from os import remove
from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto, DocumentAttributeSticker

CLONE_STR = ["Cloning the sticker"]


@tgclient.on(NewMessage(outgoing=True, pattern="^\.clone"))
async def clone(args):
    if not args.text[0].isalpha() and args.text[0] in ("."):
        user = await tgclient.get_me()
        if not user.username:
            user.username = user.first_name
        message = await args.get_reply_message()
        photo = None
        emojibypass = False
        is_anim = False
        emoji = None

        if message and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                await args.edit(f"`{random.choice(CLONE_STR)}`")
                photo = io.BytesIO()
                photo = await tgclient.download_media(message.photo, photo)
            elif "image" in message.media.document.mime_type.split('/'):
                await args.edit(f"`{random.choice(CLONE_STR)}`")
                photo = io.BytesIO()
                await tgclient.download_file(message.media.document, photo)
                if (DocumentAttributeFilename(file_name='sticker.webp') in
                        message.media.document.attributes):
                    emoji = message.media.document.attributes[1].alt
                    emojibypass = True
            elif "tgsticker" in message.media.document.mime_type:
                await args.edit(f"`{random.choice(CLONE_STR)}`")
                await tgclient.download_file(message.media.document,
                                        'AnimatedSticker.tgs')

                attributes = message.media.document.attributes
                for attribute in attributes:
                    if isinstance(attribute, DocumentAttributeSticker):
                        emoji = attribute.alt

                emojibypass = True
                is_anim = True
                photo = 1
            else:
                await args.edit("`Unsupported File!`")
                return
        else:
            await args.edit("`I can't kang that...`")
            return

        if photo:
            splat = args.text.split()
            if not emojibypass:
                emoji = "🤔"
            pack = 1
            if len(splat) == 3:
                pack = splat[2]  # User sent both
                emoji = splat[1]
            elif len(splat) == 2:
                if splat[1].isnumeric():
                    # User wants to push into different pack, but is okay with
                    # thonk as emote.
                    pack = int(splat[1])
                else:
                    # User sent just custom emote, wants to push to default
                    # pack
                    emoji = splat[1]

            packname = f"a{user.id}_by_{user.username}_{pack}"
            packnick = f"@{user.username}'s kang pack Vol.{pack}"
            cmd = '/newpack'
            file = io.BytesIO()
            print(photo)
            if not is_anim:
                image = await resize_photo(photo)
                file.name = "sticker.png"
                image.save(file, "PNG")
            else:
                packname += "_anim"
                packnick += " (Animated)"
                cmd = '/newanimated'

            response = urllib.request.urlopen(
                urllib.request.Request(f'http://t.me/addstickers/{packname}'))
            htmlstr = response.read().decode("utf8").split('\n')

            if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
                async with tgclient.conversation('Stickers') as conv:
                    await conv.send_message('/addsticker')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    while "120" in x.text:
                        pack += 1
                        packname = f"a{user.id}_by_{user.username}_{pack}"
                        packnick = f"@{user.username}'s kang pack Vol.{pack}"
                        await args.edit("`Switching to Pack " + str(pack) +
                                        " due to insufficient space`")
                        await conv.send_message(packname)
                        x = await conv.get_response()
                        if x.text == "Invalid pack selected.":
                            await conv.send_message(cmd)
                            await conv.get_response()
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await conv.send_message(packnick)
                            await conv.get_response()
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            if is_anim:
                                await conv.send_file('AnimatedSticker.tgs')
                                remove('AnimatedSticker.tgs')
                            else:
                                file.seek(0)
                                await conv.send_file(file, force_document=True)
                            await conv.get_response()
                            await conv.send_message(emoji)
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message("/publish")
                            if is_anim:
                                await conv.get_response()
                                await conv.send_message(f"<{packnick}>")
                            # Ensure user doesn't get spamming notifications
                            await conv.get_response()
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await conv.send_message("/skip")
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            await conv.send_message(packname)
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await conv.get_response()
                            # Ensure user doesn't get spamming notifications
                            await tgclient.send_read_acknowledge(conv.chat_id)
                            await args.edit(
                                f"`Sticker added in a Different Pack !\
                                \nThis Pack is Newly created!\
                                \nYour pack can be found [here](t.me/addstickers/{packname})",
                                parse_mode='md')
                            return
                    if is_anim:
                        await conv.send_file('AnimatedSticker.tgs')
                        remove('AnimatedSticker.tgs')
                    else:
                        file.seek(0)
                        await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        await args.edit(
                            "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                        )
                        return
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message('/done')
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
            else:
                await args.edit("`Brewing a new Pack...`")
                async with tgclient.conversation('Stickers') as conv:
                    await conv.send_message(cmd)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(packnick)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    if is_anim:
                        await conv.send_file('AnimatedSticker.tgs')
                        remove('AnimatedSticker.tgs')
                    else:
                        file.seek(0)
                        await conv.send_file(file, force_document=True)
                    rsp = await conv.get_response()
                    if "Sorry, the file type is invalid." in rsp.text:
                        await args.edit(
                            "`Failed to add sticker, use` @Stickers `bot to add the sticker manually.`"
                        )
                        return
                    await conv.send_message(emoji)
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message("/publish")
                    if is_anim:
                        await conv.get_response()
                        await conv.send_message(f"<{packnick}>")
                    # Ensure user doesn't get spamming notifications
                    await conv.get_response()
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.send_message("/skip")
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    await conv.send_message(packname)
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)
                    await conv.get_response()
                    # Ensure user doesn't get spamming notifications
                    await tgclient.send_read_acknowledge(conv.chat_id)

            await args.edit(
                f"`Sticker kanged successfully!`\
                \nPack can be found [here](t.me/addstickers/{packname})",
                parse_mode='md')

async def resize_photo(photo):
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image

DESC = "Sticker Management Module - Allows you to clone or add existing stickers"

USG = "`.clone`\
    \nUsage: Reply .kang to a sticker or an image to add it to your userbot pack.\
    \n\n`.clone [emoji('s)]`\
    \nUsage: Works just like .clone but uses the emoji you picked.\
    \n\n`.clone [number]`\
    \nUsage: Add's the sticker/image to the specified pack but uses 🤔 as emoji.\
    \n\n`.clone [emoji('s)] [number]`\
    \nUsage: Add's the sticker/image to the specified pack and uses the emoji('s) you picked."

MODULE_DESC.update({basename(__file__)[:-3]:DESC})
MODULE_DICT.update({basename(__file__)[:-3]:USG})
MODULE_INFO.update({basename(__file__)[:-3]: module_info(name='Sticker Manager', version='1.0.0')})
