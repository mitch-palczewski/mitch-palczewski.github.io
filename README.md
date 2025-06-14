# website-generator

pyinstaller --onefile --add-data "config/config.json;config" --add-data "config/html_validation.json;html_validation" --add-data "piecon.ico;picon" --icon=piecon.ico  main.py          