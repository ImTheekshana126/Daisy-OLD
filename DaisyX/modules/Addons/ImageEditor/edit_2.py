# By @TroJanzHEX
import os
import shutil

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance


async def circle_with_bg(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "circle.png"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("Processing Image...")
            img = Image.open(a).convert("RGB")
            npImage = np.array(img)
            h, w = img.size
            alpha = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0, 0, h, w], 0, 360, fill=255)
            npAlpha = np.array(alpha)
            npImage = np.dstack((npImage, npAlpha))
            Image.fromarray(npImage).save(edit_img_loc)
            await message.reply_chat_action("upload_photo")
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("circle_with_bg-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
