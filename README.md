# Jira Worklog Extractor

Jira Worklog Extractor is a Python script that retrieves a user's worklog from Jira and exports it to a CSV file and a Google Sheets document. You can filter the worklog by date range and project. Please note that this project is still a work in progress, and improvements are continuously being made.

## Installation

To set up and run the Jira Worklog Extractor, follow these steps:

1. Clone the repository or download the project files to your local machine.
2. Make sure you have Python 3.6 or higher installed. You can check your Python version by running `python --version` or `python3 --version` in your terminal. And hey, if you're a Mac user, you already know that you need to use `python3` instead of `python`! 😉 (Just a friendly joke, we love all users equally)
3. Install the required Python packages by running the following command in the terminal:
    ```
    pip3 install -r requirements.txt
    ```
4. Create a `.env` file in the same directory as the script and fill in your Jira credentials, account ID to search, date range, output file, project, and Google service account JSON file path. Use the `.env.example` file as a reference.
5. Run the script using the command:
    ```
    python3 worklogs.py
    ```

## Google Sheets Integration

The script can also create a Google Sheets document and populate it with the extracted worklog. To use this feature, follow these additional steps:

1. Make sure the Google Sheets API is enabled for your Google account. [Here's how](https://developers.google.com/workspace/guides/create-project).
2. Create a service account and download the JSON file. Place it in your project directory. [Here's how](https://developers.google.com/workspace/guides/create-credentials).
3. Share the Google Sheets document with your service account. Use the `client_email` found in the JSON file.
4. Add the path of your service account JSON file to the `.env` file (e.g., `GOOGLE_CREDENTIALS=google_credentials.json`).

## Contributing

As this project is still a work in progress, we welcome any suggestions, improvements, or bug reports. Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
