from mistralai import Mistral
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--training_file", "-f", type=str, required=True)
args = parser.parse_args()

training_file = args.training_file
api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)

training_data = client.files.upload(
    file={
        "file_name": training_file,
        "content": open(f"samples/{training_file}", "rb"),
    }
) 

created_job = client.fine_tuning.jobs.create(
    model="open-mistral-7b", 
    training_files=[{"file_id": training_data.id, "weight": 1}],
    validation_files=[], 
    hyperparameters={
        "training_steps": 10,
        "learning_rate":0.0001
    },
    auto_start=False,
)

# start a fine-tuning job
job_id = created_job.id
client.fine_tuning.jobs.start(job_id = job_id)

# Wait for the fine-tuning job to complete
while True:
    job = client.fine_tuning.jobs.get(job_id=job_id)
    if job.status == "SUCCESS":
        model_id = job.fine_tuned_model
        print(f"Fine-tuning completed successfully!")
        print(f"Fine-tuned model ID: {model_id}")
        break
    elif job.status == "FAILED":
        print("Fine-tuning failed.")
        break
    else:
        print(f"Current status: {job.status}")