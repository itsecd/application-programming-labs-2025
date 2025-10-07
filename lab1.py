import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('fname', type=str, help='name of file')
args = parser.parse_args()
filename = args.fname
with open(filename, "r") as file:
	text = file.readlines()
lastname = ''
firstname = ''
sex = ''
birthday = ''
phone = ''
city = ''
k = 0
with open("newdata.txt", "w") as file:
	for i in text:
		if re.search('Фамилия: ', i) != None:
			lastname = re.sub('\n','',re.sub('Фамилия: ','',i))
		elif re.search('Имя: ', i) != None:
			firstname = re.sub('\n','',re.sub('Имя: ','',i))
		elif re.search('Пол: ', i) != None:	
			sex = re.sub('\n','',re.sub('Пол: ','',i))
		elif re.search('Дата рождения: ', i) != None:
			birthday = re.sub('\n','',re.sub('Дата рождения: ','',i))
		elif re.search('Номер телефона или email: ', i) != None:
			phone = re.sub('\n','',re.sub('Номер телефона или email: ','',i))
		elif re.search('Город: ', i) != None:
			city = re.sub('\n','',re.sub('Город: ','',i))
		elif re.search(r'\d\)', i) == None:
			if sex == 'Ж' or sex == 'ж' or sex == 'Женский' or sex == 'женский':
				if firstname[0] == 'А' or firstname[0] == 'a':
					k = k+1
					file.write(str(k)+')\n')
					file.write('Фамилия: '+lastname+'\n')
					file.write('Имя: '+firstname+'\n')
					file.write('Пол: '+sex+'\n')
					file.write('Дата рождения: '+birthday+'\n')
					file.write('Номер телефона или email: '+phone+'\n')
					file.write('Город: '+city+'\n\n')
print(k)
