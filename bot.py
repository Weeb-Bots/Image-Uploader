import os
import wget
import logging
import shutil
import tgcrypto
import asyncio

from PIL import Image
from pyrogram import Client as Pyro, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from asyncio import sleep
from Config import Config
from progress import progress

# Logger Part
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(message)s')
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Pyrogram
AP = Pyro(":memory:",
          api_id=Config.API_ID,
          api_hash=Config.API_HASH,
          bot_token=Config.BOT_TOKEN
     )
prefix = ["/","!","?",";","+","-"]
image = "https://images.hdqwalls.com/wallpapers/anime-background-city-night-4k-pb.jpg"
DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION

if not os.path.exists(DOWNLOAD_LOCATION):
  os.mkdir(DOWNLOAD_LOCATION)

@AP.on_message(filters.private & filters.incoming & filters.command("start", prefix))
async def start(_, msg: Message):
   user = msg.from_user
   text = f"ʜᴇʟʟᴏ {user.mention(style='md')},\nᴛʜɪs ʙᴏᴛ ɪs sᴘᴇᴄɪᴀʟ ᴍᴀᴅᴇ ғᴏʀ ᴀɴɪᴍᴇ ᴡᴀʟʟᴘᴀᴘᴇʀ ᴄʜᴀɴɴᴇʟ ғᴏʀ @Anime_Pile ᴀɴᴅ ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ᴜᴘʟᴏᴀᴅ sɪɴɢʟᴇ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ɪɴ ʙᴏᴛʜ ᴛʏᴘᴇs ᴏʀ ɪɴ sɪɴɢʟᴇ ᴛʏᴘᴇ."
   await msg.reply_photo(image, caption=text, quote=True)

@AP.on_message(filters.private & filters.incoming & filters.command("help", prefix))
async def help(_, msg: Message):
   text = "**Steps To Use This Bot:-**\n\n1. Get A Direct Dl-URL From Internet\n2. Paste The Link Here With /ul CMD.\n3. Choose Your Option From The Reply Keyboard.\n4. Just Wait Now For Your Link To Be Fullfill.(Will Get Error Msg When The Link is Wrong or Broken)"     
   await msg.reply_photo(image, caption=text, quote=True)

@AP.on_message(filters.private & filters.incoming & filters.command("ul", prefix))
async def mainreq(_, msg: Message):
   text = msg.text
   await msg.reply_text(msg)
   if bool(msg.command[1]):
     url = msg.command[1]
   else:
     return await msg.reply_text("**ᴤᴇɴᴅ ʏᴏᴜʀ ʟɪɴᴋ ᴡɪᴛʜ ᴛʜᴇ ᴄᴍᴅ**")
   await asyncio.sleep(2)
   first = await msg.reply_text(f"**Processing Your Link:-**\n\n{url}")
   try:
        download = wget.download(url, DOWNLOAD_LOCATION)
   except Exception as e:
        LOGGER.info(str(e))
        await first.delete()
        await msg.reply_text("Error:\n`" + str(e) + "`")
        return
   try:
     await first.edit_text("--Download Completed✅--\n\n**Now Uploading Will Start Soon**")
   except Exception as e:
     await msg.reply_text("--Download Completed✅--\n\n**Now Uploading Will Start Soon**")
   await first.delete()
   await upload(download, msg)

async def upload(path, msg):
    if os.path.isdir(path):
      await msg.reply_text("Uploading Folder Is Prohibited For Me.\n**I Can Only Upload A Single File.**")
      shutil.rmtree(path)
      return
    elif not os.path.exists(path):
      return await mess.reply_text(f"`{path}` Not Found")
    else:
      pass
    up = await msg.reply_text("`Uploading...`")
    filename = path if not path.find("/") else path.split("/")[-1]
    cap = f"{filename}"
    try:
      if filename.endswith((".mkv",".mp4")):
         await mess.reply_video(path, caption=cap, quote=True, progress=progress, progress_args=(total, current, up))
      if filename.endswith((".jpg",".png",".jpeg",".webm")):
         img = Image.open(path)
         cap = f" ({img.width}x{img.height})\n\n@AnimePileWallpaper"
         await mess.reply_photo(path, caption=cap, quote=False, progress=progress, progress_args=(total, current, up))
         await mess.reply_document(path, caption=cap, quote=False, force_document=True, progress=progress, progress_args=(total, current, up))
      else:
         await mess.reply_document(path, caption=cap, quote=True, progress=progress, progress_args=(total, current, up))
    except FloodWait as e:
       await sleep(e.x)
       await upload(path, msg)
    except Exception as e:
      return await mess.reply_text("Error:\n`" + str(e) + "`")
    await up.delete()
    os.remove(path)
    await sleep(2)

print("#Bot Started")
AP.run()
