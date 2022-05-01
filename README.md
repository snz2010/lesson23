# lesson23 : "Функциональное программирование"

### Сервис на Flask, реализующий функционал команд Linux:


	cat otherfile | grep 'something'
		
	Данная запись выводит все содержимое файла otherfile (cat otherfile), а затем ищет в нем строки, которые содержат something (grep 'something')

	* на входе для метода GET нужна строка типа: /perform_query?query=filter:GET|map:0|unique|sort:desc|file_name:apache_logs.txt

	* на входе для метода POST нужны пары типа: /perform_query?cmd1=map&cmd2=unique&val1=0&val2=""&file_name=apache_logs.txt	