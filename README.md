# llm-api-connector

## Description

This repository is for the source code handling the web-api call of llm providers as GPT from Open AI

## Features

- "/test" Route - Route used for connection testing 
- Feature 2
- Feature 3
- Add more features as needed

## Installation

Install WSL as instructed here:
    https://learn.microsoft.com/en-us/windows/wsl/install
    - The recommended Distro is Ubuntu 22.04

Install Docker as instructed here:
    https://docs.docker.com/desktop/wsl/

### Prerequisites

### Setting Up Your Local Environment

To set up the local envoronment use these commands:
- Create local environment: 
    From project root folder use:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
- Navigate into the app/backend folder:
    ```bash
    cd app/backend
    ```
- Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

#### Running the Project as docker image

To run the project as docker image, navigate to the backend directory and run the following commands:

```bash
docker build -t my_flask_app .
docker run -p 4000:5000 my_flask_app
```
