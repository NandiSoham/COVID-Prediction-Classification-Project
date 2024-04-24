import os
import requests
import zipfile
import gdown
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import (DataIngestionConfig)



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    
    def download_file(self) -> str:
        '''
        Fetch data from the url
        '''

        try:
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = 'https://drive.google.com/uc?/export=download&id='
            download_url = prefix + file_id
            
            # Download the file
            response = requests.get(download_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                with open(zip_download_dir, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Downloaded data from {dataset_url} into file {zip_download_dir}")
            else:
                logger.error(f"Failed to download data from {dataset_url}. Status code: {response.status_code}")

        except Exception as e:
            raise e

    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        
        try:
            with zipfile.ZipFile(self.config.local_data_file, 'r+b') as zip_ref:
                zip_ref.extractall(unzip_path)
        except zipfile.BadZipFile:
            logger.error("The file is not a valid zip file.")
        except Exception as e:
            logger.error(f"An error occurred while extracting the zip file: {e}")

