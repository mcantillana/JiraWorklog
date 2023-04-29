# Jira Worklog Extractor

Jira Worklog Extractor is a Python script that retrieves a user's worklog from Jira and exports it to a CSV file. You can filter the worklog by date range and project. Please note that this project is still a work in progress, and improvements are continuously being made.

## Installation

To set up and run the Jira Worklog Extractor, follow these steps:

1. Clone the repository or download the project files to your local machine.

2. Make sure you have Python 3.6 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal.

3. Install the required Python packages by running the following command in the terminal:

~~~
pip install -r requirements.txt
~~~


4. Create a `.env` file in the same directory as the script and fill in your Jira credentials, account ID to search, date range, output file, and project. Use the `.env.example` file as a reference.

5. Run the script using the command:
~~~
python worklogs.py

~~~


