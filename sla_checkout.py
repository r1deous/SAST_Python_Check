<<<<<<< HEAD
from jira import JIRA
from datetime import datetime, timedelta
import pandas as pd
import re

# Регламентное время решения в часах и режимы обслуживания
service_time_metrics = {
    "Услуга 1": {
        "Критический": {"time": 12, "mode": "24x7"},
        "Высокий": {"time": 24, "mode": "24x7"},
        "Средний": {"time": 45, "mode": "9x5"},
        "Низкий": {"time": 198, "mode": "9x5"}
    },
    "Услуга 2": {
        "Критический": {"time": 4, "mode": "24x7"},
        "Высокий": {"time": 8, "mode": "24x7"},
        "Средний": {"time": 24, "mode": "9x5"},
        "Низкий": {"time": 48, "mode": "9x5"}
    }
}

login_name = 'login'
login_pass = 'passw'


jira_options = {'server': 'https://sd.v-serv.ru/jira'}
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass))  # логин и пароль от аккуанта JIRA

GTOPS_file = 'file_amount_GTOPS.txt'


# Чтение списка IDs запросов из файла и удаление пустых строк
def get_issues_from_file(filename):
    with open(filename, 'r') as file:
        issues = file.read().splitlines()
    issues = [issue for issue in issues if issue]  # удаление пустых строк
    return issues


# Функция для проверки нарушения SLA
def check_sla_violation(issue, service_time_metrics):
    service = issue.fields.customfield_10006  # поле_услуга в запросе
    priority = issue.fields.priority.name  # поле_приоритет в запросе
    created = issue.fields.created
    resolved = issue.fields.resolutiondate

    if not resolved:
        print(f'Запрос {issue.key} еще не решен.')
        return False  # Пропускаем текущий запрос, если он еще не решен

    created_dt = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
    resolved_dt = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z')

    time_diff = resolved_dt - created_dt

    # Преобразование и вычисление времени с учетом режима обслуживания
    if service in service_time_metrics and priority in service_time_metrics[service]:
        sla_time = service_time_metrics[service][priority]["time"]
        mode = service_time_metrics[service][priority]["mode"]

        if mode == "9x5":
            # Преобразование времени в рабочие часы
            work_hours = calculate_work_hours(created_dt, resolved_dt)
            print(f'Запрос {issue.key} имеет {work_hours} рабочих часов, регламент составляет {sla_time} часов.')
            return work_hours > sla_time
        elif mode == "24x7":
            total_hours = time_diff.total_seconds() / 3600
            print(f'Запрос {issue.key} имеет {total_hours} часов, регламент составляет {sla_time} часов.')
            return total_hours > sla_time

    print(f'Сервис или приоритет запроса {issue.key} не найден в метриках.')
    return False


# Вспомогательная функция для расчета рабочих часов
def calculate_work_hours(start, end):
    if start > end:
        return 0

    # Переводим в рабочие дни и часы
    work_day_start = 9
    work_day_end = 17
    total_hours = 0

    current = start
    while current < end:
        if current.weekday() < 5:  # Понедельник-пятница
            current_time = current.time()
            start_of_day = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)
            end_of_day = current.replace(hour=work_day_end, minute=0, second=0, microsecond=0)

            if current_time < start_of_day.time():
                current = start_of_day

            if current_time > end_of_day.time():
                current = current + timedelta(days=1)
                current = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)
                continue

            next_transition = min(end, end_of_day)
            total_hours += (next_transition - current).total_seconds() / 3600
            current = next_transition

        current += timedelta(days=1)
        current = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)

    return total_hours


# Получение списков всех запросов
issues = get_issues_from_file(GTOPS_file)

if not issues:
    print('Файл не содержит запросов.')

# Проверка каждого запроса на нарушение SLA
for issue_id in issues:
    try:
        issue = jira.issue(issue_id)
        if check_sla_violation(issue, service_time_metrics):
            print(f'Запрос {issue_id} нарушил регламентное время.')
    except Exception as e:
        print(f'Ошибка при обработке запроса {issue_id}: {e}')

=======
from jira import JIRA
from datetime import datetime, timedelta
import pandas as pd
import re

# Регламентное время решения в часах и режимы обслуживания
service_time_metrics = {
    "Услуга 1": {
        "Критический": {"time": 12, "mode": "24x7"},
        "Высокий": {"time": 24, "mode": "24x7"},
        "Средний": {"time": 45, "mode": "9x5"},
        "Низкий": {"time": 198, "mode": "9x5"}
    },
    "Услуга 2": {
        "Критический": {"time": 4, "mode": "24x7"},
        "Высокий": {"time": 8, "mode": "24x7"},
        "Средний": {"time": 24, "mode": "9x5"},
        "Низкий": {"time": 48, "mode": "9x5"}
    }
}

login_name = 'login'
login_pass = 'passw'


jira_options = {'server': 'https://sd.v-serv.ru/jira'}
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass))  # логин и пароль от аккуанта JIRA

GTOPS_file = 'file_amount_GTOPS.txt'


# Чтение списка IDs запросов из файла и удаление пустых строк
def get_issues_from_file(filename):
    with open(filename, 'r') as file:
        issues = file.read().splitlines()
    issues = [issue for issue in issues if issue]  # удаление пустых строк
    return issues


# Функция для проверки нарушения SLA
def check_sla_violation(issue, service_time_metrics):
    service = issue.fields.customfield_10006  # поле_услуга в запросе
    priority = issue.fields.priority.name  # поле_приоритет в запросе
    created = issue.fields.created
    resolved = issue.fields.resolutiondate

    if not resolved:
        print(f'Запрос {issue.key} еще не решен.')
        return False  # Пропускаем текущий запрос, если он еще не решен

    created_dt = datetime.strptime(created, '%Y-%m-%dT%H:%M:%S.%f%z')
    resolved_dt = datetime.strptime(resolved, '%Y-%m-%dT%H:%M:%S.%f%z')

    time_diff = resolved_dt - created_dt

    # Преобразование и вычисление времени с учетом режима обслуживания
    if service in service_time_metrics and priority in service_time_metrics[service]:
        sla_time = service_time_metrics[service][priority]["time"]
        mode = service_time_metrics[service][priority]["mode"]

        if mode == "9x5":
            # Преобразование времени в рабочие часы
            work_hours = calculate_work_hours(created_dt, resolved_dt)
            print(f'Запрос {issue.key} имеет {work_hours} рабочих часов, регламент составляет {sla_time} часов.')
            return work_hours > sla_time
        elif mode == "24x7":
            total_hours = time_diff.total_seconds() / 3600
            print(f'Запрос {issue.key} имеет {total_hours} часов, регламент составляет {sla_time} часов.')
            return total_hours > sla_time

    print(f'Сервис или приоритет запроса {issue.key} не найден в метриках.')
    return False


# Вспомогательная функция для расчета рабочих часов
def calculate_work_hours(start, end):
    if start > end:
        return 0

    # Переводим в рабочие дни и часы
    work_day_start = 9
    work_day_end = 17
    total_hours = 0

    current = start
    while current < end:
        if current.weekday() < 5:  # Понедельник-пятница
            current_time = current.time()
            start_of_day = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)
            end_of_day = current.replace(hour=work_day_end, minute=0, second=0, microsecond=0)

            if current_time < start_of_day.time():
                current = start_of_day

            if current_time > end_of_day.time():
                current = current + timedelta(days=1)
                current = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)
                continue

            next_transition = min(end, end_of_day)
            total_hours += (next_transition - current).total_seconds() / 3600
            current = next_transition

        current += timedelta(days=1)
        current = current.replace(hour=work_day_start, minute=0, second=0, microsecond=0)

    return total_hours


# Получение списков всех запросов
issues = get_issues_from_file(GTOPS_file)

if not issues:
    print('Файл не содержит запросов.')

# Проверка каждого запроса на нарушение SLA
for issue_id in issues:
    try:
        issue = jira.issue(issue_id)
        if check_sla_violation(issue, service_time_metrics):
            print(f'Запрос {issue_id} нарушил регламентное время.')
    except Exception as e:
        print(f'Ошибка при обработке запроса {issue_id}: {e}')

>>>>>>> 405a3f6960f10a20f62fe73de34daad390634ee2
print('Проверка завершена.')