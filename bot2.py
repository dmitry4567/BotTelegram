import telebot
import os
import datetime
from telebot.types import Message

m = ['0','1','2','3','4','0','0']

weekend = ['0','1','2','3','4','5']

date = {
    '0': [
        'понедельник',
        '1.География',
        '2.Химия',
        '3.Общество',
        '4.Информатика',
        '5.Информатика',
        '6.Литература',
        '7.Литература',
        '8.Проектная деятельность'
    ],
    '1': [
        'вторник',
        '1.География',
        '2.Химия',
        '3.Общество',
        '4.Информатика',
        '5.Информатика',
        '6.Литература',
        '7.Литература',
        ''
    ],
    '2': [
        'среду',
        '1.Английский язык',
        '2.Физика',
        '3.Физика',
        '4.Алгебра',
        '5.Алгебра',
        '6.Химия',
        '7.Литература',
        ''
    ],
    '3': [
        'четверг',
        '1.Русский',
        '2.Алгебра',
        '3.Алгебра',
        '4.Информатика',
        '5.Информатика',
        '6.Физ-ра',
        '7.История',
        ''
    ],
    '4': [
        'пятницу',
        '1.Биология',
        '2.Физика',
        '3.Физика',
        '4.Алгебра',
        '5.Алгебра',
        '6.ОБЖ',
        '7.Физ-ра',
        ''
    ],
    '5': [
        'субботу',
        '1.Английский язык',
        '2.Математика с/к',
        '3.Математика с/к',
        '',
        '',
        '',
        '',
        ''
    ]
}

dz = {'алгебра':'ничего',
	  'геометрия':'ничего',
	  'физика':'ничего',
      'химия':'ничего',
      'английский':'ничего',
      'информатика':'ничего',
      'история':'ничего',
      'Общество':'ничего',
      'география':'ничего',
      'биология':'ничего',
      'русский':'ничего',
      'литература':'ничего',}

bot = telebot.TeleBot("956327323:AAGSa8M6CqiAZ3pW2qx0SN0Cku4Orjssk4U")

def checkF(value):
    for k,v in date.items():
        if v[0] == value:
            return k

def checkR(value):
    for k,v in date.items():
        if v[0] == value:
            return True

def check(value):
    for k, v in dz.items():
        if value != "":
            if k == value:
                return True
            if value == 'дз':
                return True

@bot.message_handler(commands=['start,help'])
def command_handler(message: Message):
	bot.send_message(message.chat.id,"""Я могу записывать и отправлять дз:\n  -Скинь дз {предмет}\n  -Добавь дз {предмет} {дз} -Скинь все дз\n\nЯ могу запоминать и отправлять фото дз:\n -Прикрепленное фото + {предмет}\n\nЯ могу отправлять расписание:\n -Расписание на завтра\n -Расписание на {день недели}""")

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    message.caption = message.caption.lower()
    dz[message.caption] = 'фото'
    if check(message.caption):
    	print('Сохраняю фото',message.caption)
    	with open(message.caption + ".jpg", 'wb') as new_file:
        	new_file.write(downloaded_file)
        	bot.send_message(message.chat.id,'Дз добавлено')

@bot.message_handler(content_types=['text'])
def echo_digits(message: Message):

	message.text = message.text.lower()

	if 'скинь дз' in message.text:
		if check(message.text.split()[2].strip()):
			if dz[message.text.split()[2].strip()] == 'фото':
				directory = '../'
				all_files_in_directory = os.listdir(directory)
				for name in all_files_in_directory:
					if name == message.text.split()[2].strip()+".jpg":
						print('Скидываю фото',message.text.split()[2].strip()+".jpg")
						img = open(directory+'/'+name,'rb')
						bot.send_chat_action(message.from_user.id,'upload_photo')
						bot.send_photo(message.from_user.id,img,message.text.split()[2].strip())
						img.close()
			else:
				bot.send_message(message.chat.id,dz[message.text.split()[2].strip()])

	elif 'расписание' in message.text:

		if 'на' in message.text:
			if checkR(message.text.split()[2].strip()):
				y = checkF(message.text.split()[2].strip())
				f = date.get(y)
				bot.send_message(message.chat.id,"Расписание на {0}:\n {1}\n {2}\n {3}\n {4}\n {5}\n {6}\n {7}\n {8}\n".format(f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8]))

		if 'на завтра' in message.text:
			x = datetime.datetime.now()
			y = x.strftime("%w")
			y = m[int(y)]
			c = date.get(y)
			bot.send_message(message.chat.id,"Расписание на {0}:\n {1}\n {2}\n {3}\n {4}\n {5}\n {6}\n {7}\n {8}\n".format(c[0],c[1],c[2],c[3],c[4],c[5],c[6],c[7],c[8]))

	elif 'скинь все дз' in message.text:
		if check(message.text.split()[2].strip()):
			for k, v in dz.items():
				print(v)
				if v == 'фото':
					directory = '../'
					all_files_in_directory = os.listdir(directory)
					for name in all_files_in_directory:
						if name == k+".jpg":
							print('Скидываю фото',k+".jpg")
							img = open(directory+'/'+name,'rb')
							bot.send_chat_action(message.from_user.id,'upload_photo')
							bot.send_photo(message.from_user.id,img,k)
							img.close()
				else:
					bot.send_message(message.chat.id,k+' '+v)

	elif 'добавь дз' in message.text:
		if check(message.text.split()[2].strip()):
			l = len(message.text.split()[2].strip())
			dz[message.text.split()[2].strip()] = message.text[11+l:] 
			bot.send_message(message.chat.id,'Дз добавлено')

	elif 'удалить дз' in message.text:
		if check(message.text.split()[2].strip()):
			dz[message.text.split()[2].strip()] = 'ничего'
			os.remove(message.text.split()[2].strip()+".jpg")
			bot.send_message(message.chat.id,'Дз удалено')

	else:	
		bot.send_message(message.chat.id,'Я незнаю эту команду')

bot.polling(none_stop=True)
