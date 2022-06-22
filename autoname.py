import asyncio
import random
from telethon.tl import functions
from .. import loader, utils

class AutoNameMod(loader.Module):
    """none"""
    strings = {"name": "AutoName"}
    name = ["ＳＴＡＮＩＳＬＡＶ", "ꌗ꓄ꍏꈤꀤꌗ꒒ꍏᐯ", "丂ㄒ卂几丨丂ㄥ卂ᐯ", "🅢🅣🅐🅝🅘🅢🅛🅐🅥", "ⓈⓉⒶⓃⒾⓈⓁⒶⓋ", "₴₮₳₦ł₴Ⱡ₳V", "รtคภเรlคש", "ꌚꋖꁲꋊꂑꌚ꒒ꁲꀰ", "ѕтαηιѕℓαν", "ς੮คՈɿςՆค౮", "sᴛᴀɴɪsʟᴀᴠ", "STᗩᑎISᒪᗩᐯ", "🅂🅃🄰🄽🄸🅂🄻🄰🅅", "ʂɬąŋıʂƖą۷", "SᖶᗩᘉᓰSᒪᗩᐺ", "ꜱтₐ៷ᵢꜱԼₐᵥ", "ᏕᏖᏗᏁᎥᏕᏝᏗᏉ", "ΣΤΛΝΙΣLΛV"]

    async def client_ready(self, client, db):
        self.client = client

        async def periodic():
            while True:
                await self.client(functions.account.UpdateProfileRequest(first_name = random.choice(self.name)))
                await asyncio.sleep(20)
        loop = asyncio.get_event_loop()
        task = loop.create_task(periodic())
