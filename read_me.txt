GITHUB PREDICTION

Given a pull request created at time t, decide if the pull request will be eventually accepted or rejected.
We aim to use machine learning techniques to glean insights into what contributes to a successful pull request.


Before starting the project you have to run below command.

pip install -r requirements.txt
This command is used for install the require modules for this application.

go to "text_gitpredictions" folder.


For creating pull_level CSV from JSON data use below command.
python -m client.fetch_client
For creating file_level CSV from JSON data use below command.
python -m client.fetch_file_client.