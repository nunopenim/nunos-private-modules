# Copyright 2020 nunopenim @github
#
# Licensed under the DBADPL-B (Don't Be A Dick Public License B), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBADPL-B (So use it freely, but if you make a 
# shitload of cash, buy me a beer or a pizza. Thanks.

from userbot import tgclient, VERSION, PROJECT, MODULE_DESC, MODULE_DICT, LOGGING, MODULE_INFO
from userbot.config import AutomationConfig as cfg
from userbot.include.aux_funcs import event_log, module_info
from telethon.events import NewMessage
from os.path import basename

AUTVERSION = "1.0.1"

CASBAN_ENABLED = cfg.CASBAN_ENABLED
CASBAN_SENDERS = cfg.CASBAN_SENDERS

AUTOMATOR_REPLY = "AUTOMATION v." + AUTVERSION + " System powered by " + PROJECT + " v." + VERSION

@tgclient.on(NewMessage(incoming=True))
async def auto_cas_ban(sender):
    trigger = "CAS Banned user detected: "
    if CASBAN_ENABLED and sender.is_private and (sender.sender_id in CASBAN_SENDERS):
        if trigger in sender.raw_text:
            command = "/gban"
            x = sender.raw_text.split(trigger)
            data = x[1]
            replyStr = command + " " + data + " " + AUTOMATOR_REPLY
            await sender.reply(replyStr)
            if LOGGING:
                await event_log(sender, "AUTOMATION", "Automatic CAS Ban\nIssued to: `{}`".format(sender.sender_id))

DESCRIPTION = "Private taylored module for my own private use. If you are using it, you know what it does.\n\n**ALERT**: This module is not suitable for human consumption! Please refrain from using it unless you know what you are doing!"
USAGE = "It's all based in config file, so yeah... If you have this, you probably know how it works anyway.\n\n**ALERT**: This module is not suitable for human consumption! Please refrain from using it unless you know what you are doing!"

MODULE_DESC.update({basename(__file__)[:-3]: DESCRIPTION})
MODULE_DICT.update({basename(__file__)[:-3]: USAGE})
MODULE_INFO.update({basename(__file__)[:-3]: module_info(name="Automation", version=AUTVERSION)})
