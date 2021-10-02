# Copyright 2020 nunopenim @github
#
# Licensed under the DBADPL-B (Don't Be A Dick Public License B), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBADPL-B (So use it freely, but if you make a 
# shitload of cash, buy me a beer or a pizza. Thanks.

from userbot import PROJECT
from userbot.sysutils.event_handler import EventHandler
from userbot.sysutils.configuration import getConfig
from userbot.version import VERSION
from userbot.include.aux_funcs import event_log
from userbot.sysutils.registration import (register_cmd_usage,
                                           register_module_desc,
                                           register_module_info)
from logging import getLogger
from telethon.events import NewMessage


log = getLogger(__name__)
ehandler = EventHandler(log)
LOGGING = getConfig("LOGGING")
AUTVERSION = "3.0.0"
CASBAN_ENABLED = getConfig("CASBAN_ENABLED", False)
CASBAN_SENDERS = getConfig("CASBAN_SENDERS", [])
AUTOMATOR_REPLY = (f"AUTOMATION v{AUTVERSION} System powered by "
                   f"{PROJECT} v{VERSION}")


@ehandler.on_Pattern(pattern=r"^CAS Banned user detected: (.*)",
                     events=NewMessage,
                     name="automation",
                     chats=CASBAN_SENDERS,
                     no_cmd=True,
                     incoming=True)
async def auto_cas_ban(sender):
    if not CASBAN_ENABLED:
        return
    userid = sender.message.message.split(" ")[-1]
    try:
        userid = int(userid)
    except:
        log.warning(f"User id from CAS Message is not numeric")
        return
    replyStr = f"/gban {userid} {AUTOMATOR_REPLY}"
    await sender.reply(replyStr)
    if LOGGING:
        await event_log(sender,
                        "AUTOMATION",
                        user_name="Automatic CAS Ban",
                        user_id=userid,
                        custom_text=f"Issued to: `{sender.sender_id}`")
    return


DESCRIPTION = ("Private taylored module for my own private use. "
               "If you are using it, you know what it does.\n\n**ALERT**: "
               "This module is not suitable for human consumption! "
               "Please refrain from using it unless you know what you are "
               "doing!")
USAGE = ("It's all based in config file, so yeah... If you have this, "
         "you probably know how it works anyway.\n\n**ALERT**: This module "
         "is not suitable for human consumption! Please refrain from using "
         "it unless you know what you are doing!")

register_cmd_usage("automation", None, USAGE)
register_module_desc(DESCRIPTION)
register_module_info(
    name="Automation",
    authors="nunopenim",
    version=AUTVERSION
)
