# Image Datasets Generator

If you want to run this project, follow the instruction below.

1. Open the terminal in your project's folder and install Python libraries:
    ```
    pip install Pillow
    pip install beautifulsoup4
    pip install PyQt5
    ```
2. Register in https://serpapi.com/ to get a key to the API
3. Create file *keys.py* in your project's folder and fill it with this code:
    ```
    API_KEY = "your_personal_api_key_from_serpapi"
    ```
4. If you want to use this app as a desktop application, run ```app/graphicUI/main.py```
5. If you want to use this app from the command line, run ```app/commandLineUI/main.py```
