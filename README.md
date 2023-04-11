# Dvmn service chat bots helper.

### Table of content:
1. [Description](#description)
2. [Objective of project](#objective-of-project)
3. [Installing](#installing)
4. [Enviroment](#enviroment)
5. [Usage](#usage)
6. [Examples](#examples)
7. [Deployment](#deployment-on-a-server)

### Description 

Telegram chatbot and vk group chatbot, that will help answer the same type of questions using DialogFlow.  

DialogFlow -  it's a natural language understanding google cloud service. DialogFlow can analyze the text intent and response to you
by using training phrases which you provide.  

### Objective of project

The script is written for educational purposes within online courses for web developers [dvmn.org](https://dvmn.org/).

### Installing

1. Python3 must be installed. 
Use `pip` (or `pip3`) for install requirements:
```
pip install -r requirements.txt
```  
2. Also needs to install a google cloud CLI: https://cloud.google.com/sdk/docs/install#linux  
3. Create DialogFlow project:  
3.1 https://cloud.google.com/dialogflow/es/docs/quick/setup - how to create  
3.2 https://dialogflow.cloud.google.com/#/getStarted - DialogFlow page 
4. Create DialogFlow Agent: https://cloud.google.com/dialogflow/es/docs/quick/build-agent  
5. Create Intents
6. Enable DialogFlow API: https://cloud.google.com/dialogflow/es/docs/quick/setup#api
7. Create credentials for authenticate within google user accounts. 
Also it needed for google libraries calls, then save it in enviroment variables:  
https://cloud.google.com/dialogflow/es/docs/quick/setup#api 
8. For VK bot needed:  
8.1 Create the group  
8.2 Get VK group token  
8.3 Enable messages in group

### Enviroment

You needs to create .env file for enviroment variables in main folder.

- `GOOGLE_APPLICATION_CREDENTIALS` - path to yours credentials
- `DVMN_TOKEN` - dvmn token, you can get it here: https://dvmn.org/api/docs/  
- `TG_BOT_TOKEN` - needs register a bot in telegram via @BotFather: https://t.me/BotFather
- `TG_CHAT_ID` - yours chat_id / user_id, you can check it via @userinfobot: https://t.me/userinfobot
- `TG_BOT_LOGGER_TOKEN` - register an additional bot for sending logs
- `LOGS_FOLDER` - destination folder for logs
- `LOGS_MAX_SIZE` - bot logs file maximum size in bytes
- `LOGS_BACKUP_COUNT` - bot logs file backup count
- `VK_GROUP_TOKEN` - yours vk group token

### Usage
Before start the script, needs activate your bot via `/start` command in chat.

From scripts folder:
```
python(or python3) main.py
```
Alternate arguments:
- **-h / --help** - display shortly description of script and arguments. 
- **-d / --dest_folder** - destination folder for bot logs (by default use enviroment variable 'LOGS_FOLDER').
- **-m / --max_bytes** - bot logs file maximum size in bytes (by default use enviroment variable 'LOGS_MAX_SIZE').
- **-bc / --backup_count** - logs file backup count (by default use enviroment variable 'LOGS_BACKUP_COUNT').


Running example with arguments:  
`python main.py -bc 3`

### Examples  
* **Example of a Telegram bot helper**

Bot will answer for a common questions in a private telegram chat  
link: https://t.me/vo1ce_c1ty_bot  
![tg_bot](https://user-images.githubusercontent.com/79669407/231001881-74f8416f-0603-46d8-b16c-3ee34cf79be0.gif)  

* **Example of a VK group bot**

Bot will answer for a common questions in a private vk chat if you writting in a group chat  
link: https://vk.com/im?peers=-217501442&sel=c162
![vk_bot](https://user-images.githubusercontent.com/79669407/231004992-ec2d9add-2bad-4f8f-bd76-7281fe9387d9.gif)

### Deployment on a server

1. Log in to a server via username, server IP and password:  
`ssh {username}@{server IP}`
2. Clone repository. Advise to put the code in the `/opt/{project}/` folder
3. Put into the folder file with virtual enviroments `.env`
4. Create a virtual enviroment, use python(or python3):  
`python -m venv venv`
5. Follow Installing section above
6. Create a file(unit) in the `/etc/systemd/system` called like name project, e.g. `chat-bots-no1.service`, use:  
`touch /etc/systemd/system/{project}.service`
7. Write the following config into it:  
    * Execstart - for start the sevice
    * Restart - auto-restart the service if it crashes
    * WantedBy - for start service within server
```
[Service]  
ExecStart=/opt/{project}/venv/bin/python3 /opt/{project}/{main.py}
Restart=always

[Install]
WantedBy=multi-user.target
```  
8. Include the unit in the autoload list  
`systemctl enable {project}`
9. Reload systemctl  
`systemctl daemon-reload`
10. Start the unit  
`systemctl start {project}`
11. Logs will writing by enviroment variable `LOGS_FOLDER` path (for server use `/var/log/` path)
12. You can check the process:  
`ps -aux | grep {project}`  
If the process is running it will show something like this, depends on your project name:  
![image](https://user-images.githubusercontent.com/79669407/228650981-e6f8016a-40e6-4c4f-88ef-a3df6969d2fc.png)
13. if the bot is running bot logger will send a message like this:  
![image](https://user-images.githubusercontent.com/79669407/228651407-0473a366-5cab-4ac8-a346-8e8435ce402d.png)


