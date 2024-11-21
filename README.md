# Simple Lambda Version Cleaner

**Description**  

This repository provides a script to remove old versions of AWS Lambda functions, keeping only the most recent ones. This helps in managing and reducing the storage costs associated with Lambda function versions.

### Requirements  
- Python 3.10 or later  

### Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/MauricioCBarcelos/simple-lambda-version-cleaner.git
   ```  

2. Navigate to the project directory:
   ```bash
   cd simple-lambda-version-cleaner
   ```

3. Set up a virtual environment (venv) and install dependencies:  
   ```bash
   python -m venv env  
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt  
   ```  

### How to Run  

Inside the project directory, run the following command:  
```bash
python lambda_clean_versions.py <AWS profile> <Lambda region> <Number of latest versions to be maintained>
```  

Example:  
```bash
python lambda_clean_versions.py default us-east-1 5
```

### Debugging

To debug the script using Visual Studio Code, you can use the provided launch configuration. Open the script you want to debug and press `F5` to start debugging with the default arguments.

### Logging

Logs are generated for each run and stored in the `logs` directory. The logs provide detailed information about the Lambda functions processed and the versions deleted.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.