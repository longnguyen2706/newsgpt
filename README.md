# newsgpt
cloud function implementation for newsgpt site


## Resources: 
- Medium post on azure openai langchai: https://medium.com/microsoftazure/azure-openai-and-langchain-eba69f18f050
- Azure OpenAI service: https://learn.microsoft.com/en-gb/azure/cognitive-services/openai/quickstart?tabs=command-line&pivots=programming-language-python
- Langchain summarized docs: https://python.langchain.com/en/latest/modules/chains/index_examples/summarize.html
- Azure function: https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python

# Run server locally

install requirements
```bash
pip install -r requirements.txt
```

```bash
# terminal 1
azurite

# terminal 2
func start
```

Open UI: http://localhost:7071/api/index

# Deploy to cloud

After testing the functions locally, start the deployment to the cloud by following the steps in [this link](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-cli%2Cbash&pivots=python-mode-decorators#create-supporting-azure-resources-for-your-function)

In our setup:
 - <RESOURCE_GROUP_NAME>: newsgpt
 - <APP_NAME>: newsgpt-ai


Lastly deploy the function to the cloud with the following command:

```bash
# Update app settings
az functionapp config appsettings set --name newsgpt-ai --resource-group newsgpt --settings AzureWebJobsFeatureFlags=EnableWorkerIndexing

# then deploy
func azure functionapp publish  newsgpt-ai
```
