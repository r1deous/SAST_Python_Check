from jira.client import JIRA
import re

login_name = 'login'
login_pass = 'passw'


jira_options = {'server': 'https://sd.v-serv.ru/jira'}  # эту строку оставить
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass))  # логин и пароль от аккаунта JIRA

# JQL-запрос для поиска всех открытых тикетов
jql_query = 'project = GTOPS AND issuetype = "ГТ Инцидент" AND createdDate >= "2023/12/16" AND createdDate <= "2024/05/01"'

# Получаем тикеты по JQL-запросу
issues = jira.search_issues(jql_query, maxResults=0)

# Функция для чтения большого списка из файла
def read_large_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Чтение большого списка
large_list = read_large_list('file_amount_GTOPS.txt')

# Регулярное выражение для поиска GTOPS-xxxx
gtops_pattern = re.compile(r'GTOPS-\d{4}')

tickets_with_comments = {}

# Определяем ключевые слова для причин отклонения
unrelated_reasons = ['отсутствие услуги', 'предоставление доступа']

def is_unrelated_reason(comment_body):
    """Проверяет, содержит ли комментарий причину отклонения, не связанную с отсутствием услуги или доступами"""
    for reason in unrelated_reasons:
        if reason in comment_body.lower():
            return False
    return True

# Проходимся по тикетам и ищем комментарии с ключевыми словами
for issue in issues:
    comments = jira.comments(issue)
    ticket_key = issue.key
    print(ticket_key)
    for comment in comments:
        print(comment.body.lower())
        if 'отклонение' in comment.body.lower() and is_unrelated_reason(comment.body):
            tickets_with_comments[ticket_key] = "Да"
        else:
            tickets_with_comments[ticket_key] = "Нет"
        break

# Функция для сравнения списков
def compare_lists(large_list, current_list):

    comparison_results = {}

    for item in large_list:
        if item in current_list:
            comparison_results[item] = current_list[item]
        else:
            comparison_results[item] = "Не применимо"

    return comparison_results

# Сравниваем списки
comparison_results = compare_lists(large_list, tickets_with_comments)

# Вывод результатов
for key, value in comparison_results.items():
    print(f'{key}: {value}')