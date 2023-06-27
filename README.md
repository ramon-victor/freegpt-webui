# FreeGPT WebUI 
## GPT 3.5/4

❌ <strong>NOT REQUIRE ANY API KEY</strong> 🔑

This project showcases an unlocked version of ChatGPT with WebUI. <br>
Experience the power of ChatGPT with a user-friendly interface, completely free. <br> <br>

🚧 Known bugs:
- API Provider redirecting GPT-4 model to GPT-3.5;
- Auto Proxy is not working.

_Coding to solve as quickly as possible_

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
- [Incorporated Projects](#incorporated-projects-busts_in_silhouette)
  - [WebUI](#webui) 
  - [API FreeGPT](#api-g4f)
- [Star History](#star-history)
- [Legal Notice](#legal-notice) 

##

## To-Do List ✔️

- [x] Integrate the free GPT API into the WebUI
- [x] Create Docker support
- [x] Improve the Jailbreak functionality
- [x] Add the GPT-4 model
- [x] Enhance the user interface
- [ ] Auto Proxy
- [ ] Enable editing and creating Jailbreaks/Roles in the WebUI
- [ ] Migrate the interface to React.js (?)

## Getting Started :white_check_mark:  
To get started with this project, you'll need to clone the repository and have [Python](https://www.python.org/downloads/) installed on your system.  
  
### Cloning the Repository :inbox_tray:
Run the following command to clone the repository:  

```
git clone https://github.com/ramonvc/gptfree-webui.git
```

### Install Dependencies :wrench: 
Navigate to the project directory:
```
cd gptfree-webui
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
http://localhost:1338
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
![use-auto-proxy-gif](https://github.com/ramonvc/gptfree-webui/assets/13617054/f83c6217-411c-404c-9f4c-8ae700a486d1)



## Docker 🐳
### Prerequisites
Before you start, make sure you have installed [Docker](https://www.docker.com/get-started) on your machine.

### Running the Docker
Pull the Docker image from Docker Hub:
```
docker pull ramonvc/freegpt-webui
```

Run the application using Docker:
```
docker run -p 1338:1338 ramonvc/freegpt-webui
```

Access the application in your browser using the URL:
```
http://127.0.0.1:1338
```
or
```
http://localhost:1338
```

When you're done using the application, stop the Docker containers using the following command:
```
docker stop <container-id>
```

## Incorporated Projects :busts_in_silhouette:
I highly recommend visiting and supporting both projects.

### WebUI
The application interface was incorporated from the [chatgpt-clone](https://github.com/xtekky/chatgpt-clone) repository.

### API G4F
The free GPT-4 API was incorporated from the [GPT4Free](https://github.com/xtekky/gpt4free) repository.

<br>

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=ramonvc/freegpt-webui&type=Timeline)](https://star-history.com/#ramonvc/freegpt-webui&Timeline)

<br>

## Legal Notice
This repository is _not_ associated with or endorsed by providers of the APIs contained in this GitHub repository. This
project is intended **for educational purposes only**. This is just a little personal project. Sites may contact me to
improve their security or request the removal of their site from this repository.

Please note the following:

1. **Disclaimer**: The APIs, services, and trademarks mentioned in this repository belong to their respective owners.
   This project is _not_ claiming any right over them nor is it affiliated with or endorsed by any of the providers
   mentioned.

2. **Responsibility**: The author of this repository is _not_ responsible for any consequences, damages, or losses
   arising from the use or misuse of this repository or the content provided by the third-party APIs. Users are solely
   responsible for their actions and any repercussions that may follow. We strongly recommend the users to follow the
   TOS of the each Website.

3. **Educational Purposes Only**: This repository and its content are provided strictly for educational purposes. By
   using the information and code provided, users acknowledge that they are using the APIs and models at their own risk
   and agree to comply with any applicable laws and regulations.

4. **Copyright**: All content in this repository, including but not limited to code, images, and documentation, is the
   intellectual property of the repository author, unless otherwise stated. Unauthorized copying, distribution, or use
   of any content in this repository is strictly prohibited without the express written consent of the repository
   author.

5. **Indemnification**: Users agree to indemnify, defend, and hold harmless the author of this repository from and
   against any and all claims, liabilities, damages, losses, or expenses, including legal fees and costs, arising out of
   or in any way connected with their use or misuse of this repository, its content, or related third-party APIs.

6. **Updates and Changes**: The author reserves the right to modify, update, or remove any content, information, or
   features in this repository at any time without prior notice. Users are responsible for regularly reviewing the
   content and any changes made to this repository.

By using this repository or any code related to it, you agree to these terms. The author is not responsible for any
copies, forks, or reuploads made by other users. This is the author's only account and repository. To prevent
impersonation or irresponsible actions, you may comply with the GNU GPL license this Repository uses.
