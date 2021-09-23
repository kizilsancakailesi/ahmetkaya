import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}


@Client.on_message(filters.command("vizyon"))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        if len(m.command) < 2:
            await m.reply("`Reply to some Video or Give Some Live Stream Url!`")
        else:
            livelink = m.text.split(None, 1)[1]
            msg = await m.reply("`Canlı Akış başlatılıyor...`")
            chat_id = m.chat.id
            await asyncio.sleep(1)
            try:
                group_call = group_call_factory.get_group_call()
                await group_call.join(chat_id)
                await group_call.start_video(livelink, enable_experimental_lip_sync=True)
                VIDEO_CALL[chat_id] = group_call
                await msg.edit(f"**▶️ [Canlı Akış](canlı bağlantı) başlatıldı !**")
            except Exception as e:
                await msg.edit(f"**Hata** -- `{e}`")
    elif replied.video or replied.document:
        msg = await m.reply("`indiriliyor...`")
        video = await client.download_media(m.reply_to_message)
        chat_id = m.chat.id
        await asyncio.sleep(2)
        try:
            group_call = group_call_factory.get_group_call()
            await group_call.join(chat_id)
            await group_call.start_video(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("**▶️ Akış Başlatıldı!**")
        except Exception as e:
            await msg.edit(f"**Hata** -- `{e}`")
    else:
        await m.reply("`Bazı Videoları Yanıtlayın!`")

@Client.on_message(filters.command("Durdur"))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("**⏹️ CANLI AKIŞ DURDURULDU!**")
    except Exception as e:
        await m.reply(f"**🚫 HATA** - `{e}`")
