if __name__ == '__main__':
	file = open('scr/tests/test_locked.json', 'w', encoding='utf-8')
	while True: 
		file.seek(0)
		file.write('{\n\t"name":"vovan"\n}')
		file.truncate()
