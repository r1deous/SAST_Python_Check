from jira import JIRA
import re

login_name = 'login'
login_pass = 'passw'


'''# Опции подключения к JIRA
jira_options = {'server': 'https://sd.v-serv.ru/jira'}
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass))  # логин и пароль от аккаунта JIRA

# Ваш JQL-запрос
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

# Словарь для хранения тикетов с комментариями
tickets_with_comments = {}

# Определяем ключевые слова для причин отклонения
unrelated_reasons = ['отсутствие услуги', 'предоставление доступов']

def is_unrelated_reason(comment_body):
    """Проверяет, содержит ли комментарий причину отклонения, не связанную с услуга или доступами."""
    for reason in unrelated_reasons:
        if reason in comment_body.lower():
            return False
    return True

# Алгоритм проверки отклонения тикетов
for issue in issues:
    # Получаем все комментарии тикета
    comments = jira.comments(issue.key)
    for comment in comments:
        # Проверяем если комментарий содержит слово "отклонено"
        if 'отклонено' in comment.body.lower():
            # Проверяем причину отклонения
            reason_match = True if is_unrelated_reason(comment.body) else False

            # Сохраняем информацию о тикете и наличии отметки "да" при выполнении условий
            tickets_with_comments[issue.key] = {
                'comment': comment.body,
                'note': 'да' if reason_match else 'нет'
            }
            break  # прекращаем дальнейшую проверку комментариев для этого тикета, раз отклонение уже найдено

# Вывод результата
for ticket, info in tickets_with_comments.items():
    #print({info["note"]})
    print(f'Тикет: {ticket}')
    print(f'Комментарий: {info["comment"]}')
    print(f'Отметка: {info["note"]}')
    print('---------------------------------------')'''

# Опции подключения к JIRA
jira_options = {'server': 'https://sd.v-serv.ru/jira'}
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass))  # Логин и пароль от аккаунта JIRA

# Ваш JQL запрос
jql_query = 'project = GTOPS AND issuetype = "ГТ Инцидент" AND createdDate >= "2023/12/16" AND createdDate <= "2024/05/01"'

# Получаем тикеты по JQL запросу
issues = jira.search_issues(jql_query, maxResults=0)


# Функция для чтения большого списка из файла
def read_large_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]


# Чтение большого списка
large_list = read_large_list('file_amount_GTOPS.txt')

# Регулярное выражение для поиска GTOPS-xxxx
gtops_pattern = re.compile(r'GTOPS-\d{4}')

# Определение ключевых слов для причин отклонения
unrelated_reasons = ['отсутствие услуги', 'предоставление доступов']


def is_unrelated_reason(comment_body):
    """Проверяет, содержит ли комментарий не относящуюся причину."""
    for reason in unrelated_reasons:
        if reason in comment_body.lower():
            return True
    return False


# Обрабатываем каждый тикет
for issue in issues:
    issue_key = issue.key

    if issue_key in large_list:
        comments = jira.comments(issue)
        comment_found = False

        for comment in comments:
            comment_body = comment.body.lower()

            if 'отклонен' in comment_body:
                comment_found = True
                if is_unrelated_reason(comment_body):
                    print("нет")
                else:
                    print("да")
                break

        if not comment_found:
            print("")  # Пустая строка, если комментарий не содержит слово "отклонен"
    else:
        print("")  # Пустая строка, если тикет не в списке