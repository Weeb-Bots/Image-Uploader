import math

async def progress(current, total, msg):
   dl_now = humanbytes(current)
   complete = humanbytes(total)
   per = current * 100 / total
   msgg = f'📤Uploaded: {dl_now}\n🗂️Total Size: {complete}\n♻️Percentage: {round(per, 2)}%'
   try:
     await msg.edit_text(msgg)
   except:
     pass

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
  if not size:
    return ""
  power = 2**10
  n = 0
  Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
  while size > power:
    size /= power
    n += 1
  return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'
