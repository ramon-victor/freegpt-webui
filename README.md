# GPTfree Jailbreak WebUI :unlock:
This project showcases an unlocked version of ChatGPT with WebUI. <br> 🌟 <strong>NOT REQUIRE ANY API KEY</strong> 🌟 <br>
Experience the power of ChatGPT with a user-friendly interface, completely free of charge.

## Incorporated Projects :busts_in_silhouette:
I highly recommend visiting and supporting both projects.

### WebUI
The application interface was incorporated from the [chatgpt-clone](https://github.com/xtekky/chatgpt-clone) repository.

### API freeGPT
The free GPT API was incorporated from the [freeGPT](https://github.com/Ruu3f/freeGPT) repository.

## Table of Contents  
- [To-Do List](#to-do-list-%EF%B8%8F)  
- [Getting Started](#getting-started-white_check_mark)  
  - [Cloning the Repository](#cloning-the-repository-inbox_tray)  
  - [Install Dependencies](#install-dependencies-wrench)  
- [Running the Application](#running-the-application-rocket)  
- [Auto Proxy](#auto-proxy-)
  - [Enable Auto Proxy](#enable-auto-proxy)
- [Docker](#docker-)  
  - [Prerequisites](#prerequisites)  
  - [Running the Docker](#running-the-docker)  

##

## To-Do List ✔️

- [x] Integrate the free GPT API into the WebUI
- [x] Create Docker support
- [x] Auto Proxy
- [ ] Add the GPT-4 model
- [ ] Enhance the user interface
- [ ] Improve the Jailbreak functionality
- [ ] Enable editing and creating Jailbreaks in the WebUI
- [ ] Migrate the interface to React.js (?)

## Getting Started :white_check_mark:  
To get started with this project, you'll need to clone the repository and have [Python](https://www.python.org/downloads/) installed on your system.  
  
### Cloning the Repository :inbox_tray:
Run the following command to clone the repository:  

```
git clone https://github.com/ramonvc/gptfree-jailbreak-webui.git
```

### Install Dependencies :wrench: 
Navigate to the project directory:
```
cd gptfree-jailbreak-webui
```

Install the dependencies:
```
pip install -r requirements.txt
```
## Running the Application :rocket:
To run the application, run the following command:
```
python run.py
```

Access the application in your browser using the URL:
```
http://127.0.0.1:1338
```
or
```
http://172.17.0.2:1338
```
## Auto Proxy 🔑  
The application includes an auto proxy feature that allows it to work with multiple free proxy servers. 
The freeGPT API refuses some connections, especially when hosted in the cloud (Azure, AWS, Google Cloud). 
Auto proxy solves this problem automatically for you. 
When enabled, the application will automatically fetch and test proxy servers, updating the list of working proxies every 30 minutes.  
  
### Enable Auto Proxy
To enable it, just go to the `config.json` file and change the value of the "use_auto_proxy" to `true`.  

```
"use_auto_proxy": true
```
![use-auto-proxy-gif](https://github.com/ramonvc/gptfree-jailbreak-webui/assets/13617054/f83c6217-411c-404c-9f4c-8ae700a486d1)



## Docker 🐳
### Prerequisites
Before you start, make sure you have installed [Docker](https://www.docker.com/get-started) on your machine.

### Running the Docker
Build the Docker image:
```
docker-compose build
```

Run the application using Docker Compose:
```
docker-compose up
```

Access the application in your browser using the URL:
```
http://127.0.0.1:1338
```
or
```
http://172.17.0.2:1338
```

When you're done using the application, stop the Docker containers using the following command:
```
docker-compose down
```
