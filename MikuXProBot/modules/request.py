


from pyrogram import filters
from pyrogram.types import *
from MikuXProBot import pgram as app

LOG_ID = int("-1001800525670")

@app.on_message(filters.command("request"))
async def requests(client: app, message: Message):
    text_link = message.link
    text = message.text.split("/request")[1]
    EVENT = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        text="Event", url=text_link
      )
    ]
  ]
    )

    USER_TEXT = f'''**<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> your request has been successfully sent to our developers, soon they will reply you
ThankYou :)**'''
    DEV_TEXT = f'''**!New Request Master

User :- <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
Request :- {text}**
'''
    await client.send_message(LOG_ID, DEV_TEXT,reply_markup=EVENT)
    await message.reply_text(USER_TEXT)
