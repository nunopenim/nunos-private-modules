# Copyright 2020 nunopenim @github
#
# Licensed under the DBADPL-B (Don't Be A Dick Public License B), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBADPL-B (So use it freely, but if you make a 
# shitload of cash, buy me a beer or a pizza. Thanks.

from userbot import tgclient, PROJECT, MODULE_DESC, MODULE_DICT, MODULE_INFO
from userbot.sysutils.configuration import getConfig
from userbot.version import VERSION
from userbot.config import AutomationConfig as cfg
from userbot.include.aux_funcs import event_log, module_info
from telethon.events import NewMessage
from userbot.sysutils.registration import register_cmd_usage, register_module_desc, register_module_info
from userbot.sysutils.event_handler import EventHandler

log = getLogger(__name__)
ehandler = EventHandler(log)
LOGGING = getConfig("LOGGING")


AUTVERSION = "2.0.0"

CASBAN_ENABLED = cfg.CASBAN_ENABLED
CASBAN_SENDERS = cfg.CASBAN_SENDERS

AUTOMATOR_REPLY = "AUTOMATION v." + AUTVERSION + " System powered by " + PROJECT + " v." + VERSION

@ehandler.on(incoming=True)
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

register_cmd_usage("aut", "", USAGE)
register_module_desc(DESCRIPTION)
register_module_info(name="Automation", authors="nunopenim", version=AUTVERSION)
