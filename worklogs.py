import os
import csv
import pytz
import gspread
from atlassian import Jira
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables
load_dotenv()

# Configuration
jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_password = os.getenv("JIRA_PASSWORD")
jira_account_id_to_search = os.getenv("JIRA_ACCOUNT_ID_TO_SEARCH")
start_date = os.getenv("START_DATE")
end_date = os.getenv("END_DATE")
project = os.getenv("PROJECT")
tz_from = pytz.timezone(os.getenv("TZ_FROM"))
tz_to = pytz.timezone(os.getenv("TZ_TO"))
output_file = os.getenv("OUTPUT_FILE")
google_credentials = os.getenv("GOOGLE_CREDENTIALS") # path to your Google service account file
google_account_email = os.getenv("GOOGLE_ACCOUNT_EMAIL")

# Connect to Jira
jira = Jira(url=jira_url, username=jira_user, password=jira_password)

# Convert dates to datetime objects
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

# Google Sheets API credentials and connection
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
credentials = ServiceAccountCredentials.from_json_keyfile_name(google_credentials, scope)
gc = gspread.authorize(credentials)

# Create a new Google Spreadsheet
sheet = gc.create('Worklog')
sheet.share(google_account_email, perm_type='user', role='writer')

# Get the first sheet of the new Spreadsheet
worksheet = sheet.sheet1

# Function to filter worklogs by dates
def filter_worklogs_by_date(worklogs, start_date, end_date):
    filtered_worklogs = []
    for worklog in worklogs:
        dt = datetime.strptime(worklog["started"][:19], "%Y-%m-%dT%H:%M:%S")
        dt = tz_from.localize(dt)
        dt = dt.astimezone(tz_to)
        dt = datetime.strptime(worklog["started"][:10], "%Y-%m-%d")
        if start_date <= dt <= end_date:
            worklog_date = dt.strftime('%Y-%m-%d')
            filtered_worklogs.append(worklog)
    return filtered_worklogs

# Function to get a user's worklog in Jira
def get_user_worklog(account_id, start_date, end_date):
    # Search issues assigned to the user
    issues = jira.jql(f'project = "{project}" AND (worklogAuthor = {jira_account_id_to_search}) AND worklogDate >= startOfMonth() AND worklogDate <= endOfMonth()')
    # issues = jira.jql(f"assignee = {account_id}")
    total_issues = len(issues["issues"])

    worklogs = []
    for index, issue in enumerate(issues["issues"]):
        issue_key = issue["key"]
        issue_data = jira.issue(issue_key, expand='changelog,renderedFields')
        issue_worklogs = issue_data["fields"]["worklog"]["worklogs"]

        # Show search progress
        print(f"Processing issue {index + 1} of {total_issues}")

        # Filter worklogs by user and dates
        for worklog in issue_worklogs:
            if worklog["author"]["accountId"] == account_id:
                worklogs.append(worklog)

    filtered_worklogs = filter_worklogs_by_date(worklogs, start_date, end_date)
    return filtered_worklogs

# Get user's worklog
user_worklog = get_user_worklog(jira_account_id_to_search, start_date, end_date)

# Write worklog to a CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'issueId', 'date', 'timeSpent', 'timeSpentHours']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for worklog in user_worklog:
        writer.writerow({
            'id': worklog['id'],
            'issueId': worklog['issueId'],
            'date': worklog['started'][:10],
            'timeSpent': worklog['timeSpent'],
            'timeSpentHours': worklog['timeSpentSeconds']/3600
        })

print(f"Worklog saved in the file {output_file}")

# Prepare the data
data = []
fieldnames = ['id', 'issueId', 'date', 'timeSpent', 'timeSpentHours']
data.append(fieldnames)

for worklog in user_worklog:
    row = [
        worklog['id'],
        worklog['issueId'],
        worklog['started'][:10],
        worklog['timeSpent'],
        worklog['timeSpentSeconds']/3600
    ]
    data.append(row)

# Update the sheet
worksheet.update('A1', data)

print(f"Worklog saved in Google Sheets file: {sheet.url}")
