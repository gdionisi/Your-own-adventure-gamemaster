from mistralai import Mistral
import os
import time
import argparse
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def upload_dataset(filename: str):
    training_data = client.files.upload(
        file={
            "file_name": filename,
            "content": open(f"samples/{filename}", "rb"),
        }
    ) 

    print(f"Uploaded file {training_data.id}")

    return training_data


def train(files_ids: list[str]):
    """
    Train a new fine-tuned model from some datasets.
    """
    created_job = client.fine_tuning.jobs.create(
        model="open-mistral-7b", 
        training_files=[{"file_id": file_id, "weight": 1} for file_id in files_ids],
        validation_files=[], 
        hyperparameters={
            "training_steps": 10,
            "learning_rate":0.0001
        },
        auto_start=False,
    )

    # start a fine-tuning job
    job_id = created_job.id
    print(f"Created job {job_id}")

    # wait until job has been validated
    while client.fine_tuning.jobs.get(job_id=job_id).status != "VALIDATED":
        print("Job not validated yet, waiting...")
        time.sleep(1)

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
            time.sleep(1)

    return model_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_file", "-f", type=str, required=True)
    args = parser.parse_args()
    training_file = args.training_file

    upload_dataset(training_file)
    train([training_file])