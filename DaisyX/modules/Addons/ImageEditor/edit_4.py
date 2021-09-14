# By @TroJanzHEX
import io
import os
import shutil

import cv2
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageOps

from EzilaXBotV.config import get_str_key

RemoveBG_API = get_str_key("REM_BG_API_KEY", required=False)


async def rotate_90(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "rotate_90.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "Downloading image", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("Processing Image...")
            src = cv2.imread(a)
            image = cv2.rotate(src, cv2.cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(edit_img_loc, image)
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
        print("rotate_90-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
