# Purpose: How to use this repository
### Setup codebase and environment:
###### Step 1 do a github pull 
```
<git clone git@github.com:rogomes/AIWonderGirls-Climate-Change-Mitigation-Assistant.git>
```
###### Step 2 - change directory
```
cd to .. AIWonderGirls-Climate-Change-Mitigation-Assistant/web_scrape_tables_ps folder
```
###### Step 3 - for establishing python virtual environment
- if for the first time then you need to run the virtual environment create command
```
	python -m venv cli_venv
```
- activate the virtual environment
``` 
	cli_venv\Scripts\activate.bat
```
###### Step 4 - Pip installs
- upgrade pip
```
	python -m pip install --upgrade pip***
```
- install all dependencies
```
	pip install -r requirements.txt
```
### For running as a notebook
Just open the notebook in google colab 
```
run_scrape_table_data.ipynb
```
### For running from a command prompt with python script
```
run_scrape_tables.py*** ***-- url_links= "https://drawdown.org/solutions/table-of-solutions" --url_tags= "tableofsolutions" -–path_to_save=./output/ --file_type=csv*** 
```
Parameters:
- --url_links: Url link as strings separated by comma, if more than
                  one link 
- --url_tags: Url tags as strings separated by comma, if more than 
                  one link. Each tag indicates the source i.e. link
- --path_to_save: Path for saving the scraped table data
- --file_type: File save type
