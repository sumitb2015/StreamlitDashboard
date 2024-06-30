
# Streamlit Web App Deployment on Google Cloud Platform (GCP)

## Streamlit Dashboard for NSE Stocks (India Stock Market)

In the Streamlit Dashboard, we have created 4 main screens
1) Stock Dashboard for comparing Index's (like Nifty, Banknifty, etc.) & also stock price comparision
2) Price Chart with technical indicators on multiple timeframes. (More development required here)
3) US & European Stock Indices comparision (Normalized Charts)
4) Nifty 50 Stock Scanner for scanning stocks with different filters (eg. Top 10 Gainers, Losers, Highest Volume, Vol Increase in last x days etc..)


## Authors

- [@sumitb2015](https://github.com/sumitb2015)


## Installation

Files Required
Ensure you have the following files in your project directory:

1. Dockerfile
2. app.py (Streamlit application)
3. config.yaml (Configuration for Streamlit Authenticator)
4. app.yaml (App Engine configuration)
5. requirements.txt (Python dependencies)

## 

1. Set Up Google Cloud Project

```bash
gcloud projects create [PROJECT_ID]
gcloud config set project [PROJECT_ID]
```

2. Enable necessary APIs:
```bash
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

3. Create an App Engine application:
```bash
gcloud app create --region=[YOUR_REGION]
```

4. Prepare Your Application
Dockerfile: Ensure your Dockerfile is correctly set up to build the Streamlit application.

5. requirements.txt: Ensure all dependencies are listed.

    
## Deployment

1. app.yaml: Configuration for App Engine.
```yaml
runtime: custom
env: flex

handlers:
  - url: /.*
    script: auto
```

2. Build and Deploy the Docker Image
```bash
docker build -t gcr.io/[PROJECT_ID]/streamlit-app .
```

3. Push the Docker image to Google Container Registry
```bash
docker push gcr.io/[PROJECT_ID]/streamlit-app
```

4. Deploy the Application to App Engine
```bash
gcloud app deploy
```
5. Browse the deployed app
```bash
gcloud app browse
```

## Additional Information
#### Updating the App: 
Make changes to your local files, rebuild the Docker image, push it to the registry, and redeploy:
```bash
docker build -t gcr.io/[PROJECT_ID]/streamlit-app .
docker push gcr.io/[PROJECT_ID]/streamlit-app
gcloud app deploy
```
#### Stopping a Version: If you need to stop a specific version:
```bash
gcloud app versions stop [VERSION_ID] --service=default
```
#### Viewing Logs: To view the logs of your application:
```bash
gcloud app logs tail -s default
```
## Run Locally

#### Clone the project

```bash
  git clone https://github.com/sumitb2015/StreamlitDashboard
```

#### Go to the project directory

```bash
  cd StreamlitDashboard
```

#### Install dependencies

```bash
  pip install -r requirements.txt
```

#### Start the streamlit server

```bash
  streamlit run app.py --server.port 8080 
```

