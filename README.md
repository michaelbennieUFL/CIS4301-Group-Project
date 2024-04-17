# CIS4301-Group-Project

![ER diagram.png](ER%20diagram.png)

Our data comes from two sources:
https://github.com/ip2location/ip2location-iata-icao/blob/master/iata-icao.csv
https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents

To run the front-end:

1. Ensure that you have Python3 installed locally. If not, https://packaging.python.org/en/latest/tutorials/installing-packages/

2. Run `pip install mercury` to use Mercury for the transformation of the Jupyter Notebook into a web application

3. Run `pip install oracledb --upgrade` to be able to link Oracle to the Jupyter Notebook

4. Run `pip install voila`, `pip install ipywidgets`, and `pip install plotly` to be able to use Viola to run the local web server and display the graphs.

5. Once everything is installed, run `viola frontEnd` to run and host the Jupyter Notebook application.

6. After running the Jupyter Notebook application, click on `website.ipynb` to begin navigating the home page and various queries!