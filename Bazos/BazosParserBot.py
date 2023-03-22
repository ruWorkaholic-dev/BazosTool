"""
 /$$$$$$$   /$$$$$$  /$$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$   /$$$$$$  /$$      
| $$__  $$ /$$__  $$|_____ $$  /$$__  $$ /$$__  $$|__  $$__//$$__  $$ /$$__  $$| $$      
| $$  \ $$| $$  \ $$     /$$/ | $$  \ $$| $$  \__/   | $$  | $$  \ $$| $$  \ $$| $$      
| $$$$$$$ | $$$$$$$$    /$$/  | $$  | $$|  $$$$$$    | $$  | $$  | $$| $$  | $$| $$      
| $$__  $$| $$__  $$   /$$/   | $$  | $$ \____  $$   | $$  | $$  | $$| $$  | $$| $$      
| $$  \ $$| $$  | $$  /$$/    | $$  | $$ /$$  \ $$   | $$  | $$  | $$| $$  | $$| $$      
| $$$$$$$/| $$  | $$ /$$$$$$$$|  $$$$$$/|  $$$$$$/   | $$  |  $$$$$$/|  $$$$$$/| $$$$$$$$
|_______/ |__/  |__/|________/ \______/  \______/    |__/   \______/  \______/ |________/
                                                                                                  
channel -> https://t.me/channel_workaholic                                                                                                                                                                                                

DISCLAIMER:

The software is fictional, and the resemblance to real persons and events may be only incidental and unintentional. 

The software is intended for familiarisation, for safety reasons, as "forewarned is forearmed". 

I AM NOT ENCOURAGING ANYONE TO USE THE SOFTWARE TO THEIR DETRIMENT! ALL RESPONSIBILITY RESTS ON YOUR SHOULDERS!

"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold, hcode, hlink
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from driver.bazos import ParserBazosSK
from driver.BazosPhone import BazosSkPhone

from config.config import BOT_API

bot = Bot(BOT_API, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())


dict_for_number = {}
bkod_bazos = []


async def set_default_commands(dp):
	await dp.bot.set_my_commands([types.BotCommand('start', 'Update the bot')])

class Bazos(StatesGroup):
	name_platform,min_price,max_price,view,items,count_dataNewPost,BkodBazos = State(),State(),State(),State(),State(),State(),State()


kb_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🔎 Search", callback_data="🔎 Search")],[KeyboardButton(text="📂 Bkod Bazos", callback_data="📂 Bkod Bazos")],[KeyboardButton(text= "🥷 Info", callback_data="🥷 Info")]],resize_keyboard=True)
kb_token = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📂 Add Bazos Bkod", callback_data="token_app")],[InlineKeyboardButton(text="🗑 Delete Bazos Bkod", callback_data="token_deled")],[InlineKeyboardButton(text="↪️ Remove menu", callback_data="alert")]])


@dp.message_handler(commands="start")
async def command_start(message: types.Message):

	text = f"🔗 {hbold('Buttons updated')}"
	await bot.send_message(message.from_user.id, text=text, reply_markup=kb_menu)

@dp.message_handler(text="🔎 Search")
async def get_platfor(message: types.Message):

	text = f'👀 {hbold("List of links BazosSk")}\n'\
	'[1] Sporting Goods - https://sport.bazos.sk/\n'\
	'[2] Clothes - https://oblecenie.bazos.sk/\n'\
	'[3] Pets - https://zvierata.bazos.sk/\n'\
	'[4] Kids - https://deti.bazos.sk/\n'\
	'[5] Real Estate - https://reality.bazos.sk/\n'\
	'[6] Jobs - https://praca.bazos.sk/\n'\
	'[7] Cars - https://auto.bazos.sk/\n'\
	'[8] Motorcycles - https://motocykle.bazos.sk/\n'\
	'[9] Trucks - https://stroje.bazos.sk/\n'\
	'[10] Home & Garden - https://dom.bazos.sk/\n'\
	'[11] Computer - https://pc.bazos.sk/\n'\
	'[12] Phones - https://mobil.bazos.sk/\n'\
	'[13] Cameras - https://foto.bazos.sk/\n'\
	'[14] Electronics - https://elektro.bazos.sk/\n'\
	'[15] Musical Instruments - https://hudba.bazos.sk/\n'\
	'[16] Tickets - https://vstupenky.bazos.sk/\n'\
	'[17] Books - https://knihy.bazos.sk/\n'\
	'[18] Furniture - https://nabytok.bazos.sk/\n'\
	'[19] Services - https://sluzby.bazos.sk/\n'\
	'[20] Other - https://ostatne.bazos.sk/\n'\
	f'{hbold("Enter the number-link to parser ")}⤵️'

	await bot.send_message(message.from_user.id, text=text, reply_markup=ReplyKeyboardRemove())
	await Bazos.name_platform.set()

@dp.message_handler(state=Bazos.name_platform)
async def get_min_price(message: types.Message, state: FSMContext):
	await state.update_data(name_platform=int(message.text))

	text = f'{hbold("Enter the minimum price of the item ")}⤵️'
	await bot.send_message(message.from_user.id, text=text)
	await Bazos.min_price.set()

@dp.message_handler(state=Bazos.min_price)
async def get_max_price(message: types.Message, state: FSMContext):
	await state.update_data(min_price=int(message.text))

	text = f'{hbold("Enter the maximum price of the item ")}⤵️'
	await bot.send_message(message.from_user.id, text=text)
	await Bazos.max_price.set()

@dp.message_handler(state=Bazos.max_price)
async def get_views(message: types.Message, state: FSMContext):
	await state.update_data(max_price=int(message.text))

	text = f'{hbold("Enter the number of views on the item ")}⤵️'
	await bot.send_message(message.from_user.id, text=text)
	await Bazos.view.set()

@dp.message_handler(state=Bazos.view)
async def get_items(message: types.Message, state: FSMContext):
	await state.update_data(view=int(message.text))

	text = f'{hbold("Enter the number of items on sale at the seller ")}⤵️'
	await bot.send_message(message.from_user.id, text=text)
	await Bazos.items.set()

@dp.message_handler(state=Bazos.items)
async def get_count_dataNewPost(message: types.Message, state: FSMContext):
	await state.update_data(items=int(message.text))

	text = f'{hbold("Enter the number of items you want to find ")}⤵️'
	await bot.send_message(message.from_user.id, text=text)
	await Bazos.count_dataNewPost.set()

@dp.message_handler(state=Bazos.count_dataNewPost)
async def get_parser(message: types.Message, state: FSMContext):

	kb_number = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📞 Number", callback_data="number")]])

	data = await state.get_data()

	name_platform = data.get("name_platform")
	min_price = data.get("min_price")
	max_price = data.get("max_price")
	view = data.get("view")
	items = data.get("items")
	count_dataNewPost = int(message.text)

	await state.finish()

	Bazos_sk = ["https://sport.bazos.sk/", "https://oblecenie.bazos.sk/", "https://zvierata.bazos.sk/", "https://deti.bazos.sk/", "https://reality.bazos.sk/", "https://praca.bazos.sk/"," https://auto.bazos.sk/", "https://motocykle.bazos.sk/", "https://stroje.bazos.sk/", "https://dom.bazos.sk/", 'https://pc.bazos.sk/','https://mobil.bazos.sk/','https://foto.bazos.sk/','https://elektro.bazos.sk/','https://hudba.bazos.sk/','https://vstupenky.bazos.sk/','https://knihy.bazos.sk/','https://nabytok.bazos.sk/','https://sluzby.bazos.sk/','https://ostatne.bazos.sk/']	

	name_platform = Bazos_sk[name_platform-1]

	text = f'{hbold("Strat Search ")}🔎'
	await bot.send_message(message.from_user.id, text=text)

	dataPosts = await ParserBazosSK(name_platform, count_dataNewPost, min_price, max_price, view, items).LogerParser()

	count_phone = f"Found {len(dataPosts)} items"
	text = f"{hbold(count_phone)} 📂"
	await bot.send_message(message.from_user.id, text=text)


	for dataPost in dataPosts:

		news = f"{hbold('Platform Bazos.sk')}\n\n" \
				f"🗂 Product: {hcode(dataPost[0])}\n " \
				f"🕘 Date of publication: {hbold(dataPost[1])}\n" \
				f"💵 Price: {hcode(dataPost[2])}€\n" \
				f"🌍 Location: {hcode(dataPost[3])}\n\n" \
				f"📖 Description:\n{hcode(dataPost[4])}\n\n" \
				f"{hlink('🔗 Link to Product', dataPost[5])}\n" \
				f"{hlink('🔗 Link to photo', dataPost[6])}\n" \
				f"{hlink('🔗 Seller Reference', dataPost[7])}\n\n" \
				f"👁 No. views on the product: {hbold(dataPost[8])}\n"\
				f"📂 No. of seller's listings: {hbold(dataPost[9])}"

		messagetoedit = await bot.send_photo(message.from_user.id, photo=dataPost[6], caption=news, reply_markup=kb_number)
		dict_for_number[messagetoedit.message_id] = dataPost


	text = f'{hbold("Finish Search")} 💤'
	await bot.send_message(message.from_user.id, text=text, reply_markup=kb_menu)

@dp.callback_query_handler(text="number")
async def send_post(call: CallbackQuery):
	if len(bkod_bazos) == 0:
		text = f'❌ {hbold("You need to add bkod Bazos to open the number")} ❌'
		await bot.send_message(call.from_user.id, text=text)

	else:
		dataPost = dict_for_number[call.message.message_id]

		for bkod in bkod_bazos:
			number = await BazosSkPhone(bkod, dataPost[10]).LoggerParserPhone()

			if number == "bkod not valid":
				text = f"{hcode(bkod)}{hbold(' -> bkod not valid')}"
				await bot.send_message(call.from_user.id, text=text)
				bkod_bazos.remove(bkod)

			elif "max" in number:
				text = f"{hcode(bkod)}{hbold(' -> bkod not valid')}"
				await bot.send_message(call.from_user.id, text=text)
				bkod_bazos.remove(bkod)


			else:
				if number[0] == '0':
					number = f"+421{number[1:]}"
				else:
					number = f"+421{number}"

				whatsApp = f"https://api.whatsapp.com/send?phone={number}"
				whatsAppWeb = f"https://web.whatsapp.com/send/?phone={number}" 
				viber = f"https://viber.click/{number[1:]}"
				telegram = f"https://t.me/{number[1:]}"

				news = f"{hbold('Platform Bazos.sk')}\n\n" \
						f"🗂 Product: {hcode(dataPost[0])}\n " \
						f"🕘 Date of publication: {hbold(dataPost[1])}\n" \
						f"💵 Price: {hcode(dataPost[2])}€\n" \
						f"🌍 Location: {hcode(dataPost[3])}\n\n" \
						f"📖 Description:\n{hcode(dataPost[4])}\n\n" \
						f"{hlink('🔗 Link to Product', dataPost[5])}\n" \
						f"{hlink('🔗 Link to photo', dataPost[6])}\n" \
						f"{hlink('🔗 Seller Reference', dataPost[7])}\n\n" \
						f"👁 No. views on the product: {hbold(dataPost[8])}\n"\
						f"📂 No. of seller's listings: {hbold(dataPost[9])}\n\n"\
						f"{hlink('WhatsApp', whatsApp)}\n" \
						f"{hlink('WhatsApp Web', whatsAppWeb)}\n" \
						f"{hlink('Telegram', telegram)}\n" \
						f"{hlink('Viber', viber)}" 
				
				await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, inline_message_id=call.message.message_id, caption=news)
				break

@dp.message_handler(text="📂 Bkod Bazos")
async def get_bkod(message: types.Message):

	token = '\n'.join(bkod_bazos)
	text = f"Bazos Bkod ⤵️\n\n"\
		f"{token}"

	await bot.send_message(message.from_user.id, text=text, reply_markup=kb_token)

@dp.callback_query_handler(text="token_app")
async def send_token(call: CallbackQuery):
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

	text = f"{hbold('Enter bkod BazosSk ')}⤵️"

	await bot.send_message(call.from_user.id, text=text, reply_markup=ReplyKeyboardRemove())
	await Bazos.BkodBazos.set()

@dp.message_handler(state=Bazos.BkodBazos)
async def get_count_dataNewPost(message: types.Message, state: FSMContext):

	if "," in message.text:
		bkodAppend = [bkod_bazos.append(bkod) for bkod in message.text.split(",")]

	elif "\n" in message.text:
		bkodAppend = [bkod_bazos.append(bkod) for bkod in message.text.split("\n")]


	else:
		bkod_bazos.append(message.text)

	await state.finish()
	text = f'{hbold("Bkod successfully added")} ✅'
	await bot.send_message(message.from_user.id, text=text, reply_markup=kb_menu)

	token = '\n'.join(bkod_bazos)
	text = f"Bazos Bkod ⤵️\n\n"\
		f"{token}"
	await bot.send_message(message.from_user.id, text=text, reply_markup=kb_token)

@dp.callback_query_handler(text="token_deled")
async def deled_token(call: CallbackQuery):
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	bkod_bazos.clear()

	token = '\n'.join(bkod_bazos)
	text = f"Bazos Bkod ⤵️\n\n"\
		f"{token}"
	await bot.send_message(call.from_user.id, text=text, reply_markup=kb_token)

@dp.callback_query_handler(text="alert")
async def get_menu(call: CallbackQuery):
	await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

@dp.message_handler(text="🥷 Info")
async def me(message: types.Message):

	kb_me = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🗂 Developer's Channel", url="https://t.me/channel_workaholic")],[InlineKeyboardButton(text="💤 Developer's GitHub", url="https://github.com/ruWorkaholic-dev")],[InlineKeyboardButton(text="↪️ Remove menu", callback_data="alert")]])

	text_me = f"{hbold('The creator of the software -> https://t.me/channel_workaholic')}"
	photo = InputFile("data/photo/workaholic.jpeg")

	messagetoedit = await bot.send_photo(message.from_user.id, photo=photo, caption=text_me, reply_markup=kb_me)

if __name__ == '__main__':
	executor.start_polling(dp, on_startup=set_default_commands, skip_updates=True)



