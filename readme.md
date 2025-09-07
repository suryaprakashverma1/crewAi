Dwonload docker and then go to running the crewAi docker image: https://hub.docker.com/r/seemeai/crewai

run the image from docker UI: remember you should have an open API key, if you don't have local llm model setup for this.
<img width="616" height="647" alt="image" src="https://github.com/user-attachments/assets/bce829c1-a1b9-4c99-9fc0-a20460848765" />


now the note book will be ready at the following link:
http://127.0.0.1:8888/tree

where you can create an new notebook to write python code.

============================================================================================
This is how you should setup the local model.

install ollama locally: 
then run ollama by: ollama serve

install the model of your interest:
ollama pull lamma 3.1

check if the ollama is actually running this model:
curl http://localhost:11434/api/tags

running ollama locally and crewAi docker image for running the jupiter note book, you will find the code over here:LocalOllamaDockerCrewAI.py 
