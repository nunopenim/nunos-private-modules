# Copyright 2020 nunopenim @github
#
# Licensed under the DBADPL-B (Don't Be A Dick Public License B), v1.0
#
# You may not use this file or any of the content within it, unless in
# compliance with the DBADPL-B (So use it freely, but if you make a 
# shitload of cash, buy me a beer or a pizza. Thanks.

from userbot import tgclient, VERSION, PROJECT, MODULE_DESC, MODULE_DICT, LOGGING
from userbot.config import AutomationConfig as cfg
from userbot.include.aux_funcs import event_log
from telethon.events import NewMessage
from os.path import basename

AUTOMATION_ENABLED = cfg.AUTOMATION_ENABLED
AUTOMATION_SENDERS = cfg.AUTOMATION_SENDERS
AUTOMATION_COMMANDS = cfg.AUTOMATION_COMMANDS
AUTOMATION_TRIGGERS = cfg.AUTOMATION_TRIGGERS

AUTOMATOR_REPLY = "Automation System powered by " + PROJECT + " v." + VERSION

@tgclient.on(NewMessage(incoming=True))
async def automation(sender):
    if AUTOMATION_ENABLED and sender.is_private and (sender.sender_id in AUTOMATION_SENDERS):
        for trigger in AUTOMATION_TRIGGERS:
            if trigger in sender.raw_text:
                commandId = AUTOMATION_TRIGGERS.index(trigger)
                command = AUTOMATION_COMMANDS[commandId]
                x = sender.raw_text.split(trigger)
                data = x[1]
                replyStr = command + " " + data + " " + AUTOMATOR_REPLY
                await sender.reply(replyStr)
                if LOGGING:
                    await event_log(sender, "AUTOMATION", "The command `{}` has been successfully executed in the sender `{}`".format(replyStr, sender.sender_id))

DESCRIPTION = "Private taylored module for my own private use. You know what it does."
USAGE = "It's all based in config file, so yeah... If you have this, you probably know how it works anyway."

MODULE_DESC.update({basename(__file__)[:-3]: DESCRIPTION})
MODULE_DICT.update({basename(__file__)[:-3]: USAGE})
