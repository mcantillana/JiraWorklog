import os
import csv
from atlassian import Jira
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
jira_url = os.getenv("JIRA_URL")
jira_user = os.getenv("JIRA_USER")
jira_password = os.getenv("JIRA_PASSWORD")
jira_account_id_to_search = os.getenv("JIRA_ACCOUNT_ID_TO_SEARCH")
start_date = os.getenv("START_DATE")
end_date = os.getenv("END_DATE")
output_file = os.getenv("OUTPUT_FILE")
project = os.getenv("PROJECT")


# Conexión a Jira
jira = Jira(url=jira_url, username=jira_user, password=jira_password)

# Convertir las fechas a objetos datetime
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

# Función para filtrar worklogs por fechas
def filter_worklogs_by_date(worklogs, start_date, end_date):
    filtered_worklogs = []
    for worklog in worklogs:
        worklog_date = datetime.strptime(worklog["started"][:10], "%Y-%m-%d")
        if start_date <= worklog_date <= end_date:
            filtered_worklogs.append(worklog)
    return filtered_worklogs

# Función para obtener el worklog de un usuario en Jira
def get_user_worklog(account_id, start_date, end_date):
    # Buscar issues asignados al usuario

    issues = jira.jql(f'project = "{project}" AND (assignee was {jira_account_id_to_search} OR assignee = {jira_account_id_to_search}) AND worklogDate >= startOfMonth()')
    # issues = jira.jql(f"assignee = {account_id}")
    total_issues = len(issues["issues"])
    
    worklogs = []
    for index, issue in enumerate(issues["issues"]):
        issue_key = issue["key"]
        issue_data = jira.issue(issue_key, expand='changelog,renderedFields')
        issue_worklogs = issue_data["fields"]["worklog"]["worklogs"]
        
        # Mostrar el progreso de la búsqueda
        print(f"Procesando issue {index + 1} de {total_issues}")
        
        # Filtrar worklogs por usuario y fechas
        for worklog in issue_worklogs:
            if worklog["author"]["accountId"] == account_id:
                worklogs.append(worklog)
    
    filtered_worklogs = filter_worklogs_by_date(worklogs, start_date, end_date)
    return filtered_worklogs

# Obtener el worklog del usuario
user_worklog = get_user_worklog(jira_account_id_to_search, start_date, end_date)

# Escribir el worklog en un archivo CSV
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

print(f"Worklog guardado en el archivo {output_file}")
