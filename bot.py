import os
import wget
import logging
import shutil

from pyrogram import Client as Pyro, filters
from pyrogram.types import Message
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

@AP.on_message(filters.private & filters.incoming & ~filters.edited & filters.command("start", prefix))
async def start(msg: message, client):
   user = msg.from_user
   text = f"ʜᴇʟʟᴏ {user.mention(style='md')},\nᴛʜɪs ʙᴏᴛ ɪs sᴘᴇᴄɪᴀʟ ᴍᴀᴅᴇ ғᴏʀ ᴀɴɪᴍᴇ ᴡᴀʟʟᴘᴀᴘᴇʀ ᴄʜᴀɴɴᴇʟ ғᴏʀ @Anime_Pile ᴀɴᴅ ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ᴜᴘʟᴏᴀᴅ sɪɴɢʟᴇ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ɪɴ ʙᴏᴛʜ ᴛʏᴘᴇs ᴏʀ ɪɴ sɪɴɢʟᴇ ᴛʏᴘᴇ."
   await msg.reply_photo(image, text, parse_mode='md', quote=False)

@AP.on_message(filters.private & filters.incoming & ~filters.edited & filters.command("help", prefix))
async def help(msg: message, client):
   text = "**Steps To Use This Bot:-**\n\n1. Get A Direct Dl-URL From Internet\n2. Paste The Link Here With /ul CMD.\n3. Choose Your Option From The Reply Keyboard.\n4. Just Wait Now For Your Link To Be Fullfill.(Will Get Error Msg When The Link is Wrong or Broken)"     
   await msg.reply_photo(image, text, parse_mode='md', quote=True)

@AP.on_message(filters.private & filters.incoming & ~filters.edited & filters.command("ul", prefix))
async def mainreq(msg: message, client):
   text = msg.text
   if not bool(text.find(" ")):
     return await msg.reply_text("**ᴤᴇɴᴅ ʏᴏᴜʀ ʟɪɴᴋ ᴡɪᴛʜ ᴛʜᴇ ᴄᴍᴅ**")
   else:
     pass
   url = text.replace("/ul ")
   first = await msg.reply_text(f"**Processing Your Link:-**\n\n{url}")
   try:
        download = wget.download(url, DOWNLOAD_LOCATION)
   except Exception as e:
        LOGGER.info(str(e))
        await first.delete()
        await one.reply_text("Error:\n`" + str(e) + "`")
        return
   try:
     await one.edit_text("--Download Completed✅--\n\n**Now Uploading Will Start Soon**")
   except Exception as e:
     await msg.reply_text("--Download Completed✅--\n\n**Now Uploading Will Start Soon**")
   await one.delete()
   await upload(download, msg)

async def upload(path, msg):
   if os.path.isdir(path):
      await mess.reply_text("Uploading Folder Is Prohibited For Me.\n**I Can Only Upload A Single File.**", parse_mode='md')
      shutil.rmtree(path)
      return
    elif not os.path.exists(path):
      return await mess.reply_text(f"`{path}` Not Found")
    else:
      pass
    up = await mess.reply_text("`Uploading...`")
    filename = path if not path.find("/") else path.split("/")[-1]
    cap = f"{filename}"
    try:
      if filename.endswith((".mkv",".mp4")):
         await mess.reply_video(path, caption=cap, quote=True, progress=progress, progress_args=(total, current, up))
      if filename.endswith((".jpg",".png",".jpeg",".webm")):
         wala = await mess.reply_photo(path, quote=False, progress=progress, progress_args=(total, current, up))
         caption = f"({wala.photo.width}x{wala.photo.height})\n\n@Anime_Pile_Wallpaper"
         await caption(wala, caption, 0)
         wala2 = await mess.reply_document(path, quote=False, force_document=True, progress=progress, progress_args=(total, current, up))
         await caption(wala2, caption, 0)
      else:
         await mess.reply_document(path, caption=cap, quote=True, progress=progress, progress_args=(total, current, up))
    except Exception as e:
      return await mess.reply_text("Error:\n`" + str(e) + "`")
    await up.delete()
    os.remove(path)
    await sleep(3)
 
async def caption(wala, caption, loop):
   if loop > 3:
     return await wala.reply_text("Caption Could Not Be Modified", quote=True)
   else:
     try:
       cap = await wala.edit_text(caption)
     except Exception as e:
       LOGGER.info(e)
       loop += 1
       await sleep(1)
       await caption(docwala, loop)
   return cap

AP.run()
