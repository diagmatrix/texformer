import logging
from uuid import uuid4
import re
from telegram.ext import Updater, InlineQueryHandler
from telegram import InlineQueryResultCachedPhoto, InputTextMessageContent
import matplotlib.pyplot as plt
import matplotlib

# Config
botID = "xxxx" # ID of the bot
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{{amsmath}}"
updater = Updater(token=botID,use_context=True)
bot = updater.bot
dispatcher = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",level=logging.INFO)
upload_id = 000000 # Private channel ID for the bot to send the imgs

# Creates the image with the formula
def to_latex(formula,id):
    img_name = "image.jpeg"
    fig = plt.figure()
    fig.text(0.5,0.5,formula,fontsize=20,horizontalalignment="center",verticalalignment="center")
    fig.savefig(img_name)
    return img_name

# Handler of inline requestes
def inline_formula(update, context):
    query = update.inline_query.query
    if not query:
        return
    if (re.search(r"\^\$.*\$",query) is None):
        return
    # Create the photo
    print("TRANSFORMING: "+query+"\n")
    photoinfo = bot.send_photo(
        chat_id=-1001457635665,
        photo=open(to_latex(query,update.inline_query.id),"rb"),
        caption="Formula"
    )
    # Send the photo
    results = [
        InlineQueryResultCachedPhoto(
            id=uuid4(),
            photo_file_id=photoinfo["photo"][-1]["file_id"],
            title="Formula"
        )
    ]
    context.bot.answer_inline_query(update.inline_query.id, results)

inline_formula_handler = InlineQueryHandler(callback=inline_formula)
dispatcher.add_handler(inline_formula_handler)

updater.start_polling()