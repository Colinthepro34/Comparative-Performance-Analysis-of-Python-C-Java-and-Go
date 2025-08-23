import kagglehub
import os

def download_dataset():
    print("Downloading dataset from Kaggle...")
    path = kagglehub.dataset_download("weitat/sample-sales")
    print("Dataset downloaded at:", path)

    # Optionally, list files inside to find CSV filename
    files = os.listdir(path)
    print("Files available:", files)

    return path

if __name__ == "__main__":
    download_dataset()
