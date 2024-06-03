from jira.client import JIRA
from datetime import datetime

login_name = 'login'
login_pass = 'passw'


jira_options = {'server': 'https://sd.v-serv.ru/jira'} # эту строку оставлсять
jira = JIRA(options=jira_options, basic_auth=(login_name, login_pass)) # логин и пароль от аккуанта JIRA

issue = jira.issue('GTOPS-6386', expand='changelog')

'''#custom_file = 'custom_field.txt'
for field_name in issue.fields.__dict__:
    print(field_name, ":", getattr(issue.fields, field_name))'''

'''status_changes = []
for history in issue.changelog.histories:
    for item in history.items:
        if item.field == 'status':
            status_changes.append({
                'from': item.fromString,
                'to': item.toString,
                'date': history.created
            })
'''
# Выводим статусы
#for change in status_changes:
    #print(f"Статус изменился с '{change['from']}' на '{change['to']}' в {change['date']}")

with open('test.txt', 'r') as file:
    for line in file:
        tmp = line.strip()
        custom_field_value = issue.raw['fields'][tmp]
        print(tmp, ': ', custom_field_value)
'''
#Вывод всех комментов
for j in range(comm_count):
    comment_created = issue.fields.comment.comments[j].created # дата и время создания тикета
    print(comment_created)
    comment_body = issue.fields.comment.comments[j].body # тело комменатрия
    print(comment_body)
    # file_comments_GTOPS.write(comment_created + '\n' + comment_body + '\n')
    print('')
'''


'''with open(custom_file, 'r') as file:
    for line in file:
        tmp = line.strip()
        custom_field_value = issue.fields.__dict__.get(tmp)
        print(tmp, ' - ' ,custom_field_value)
        print(dir(custom_field_value))

fields = issue.fields
for field_name in issue.fields.__dict__:
    print(field_name, ":", dir(issue.fields))
print(' ')
print(dir(issue.fields))
print(" ")
print(dir(issue.fields.resolution))
print(" ")
print(issue.fields.resolution.__dir__())'''


'''print(' ')
custom_field_value = issue.fields.__dict__.get('customfield_23703')
print(dir(custom_field_value))
print(custom_field_value.name)'''

'''
#transitions = jira.transitions('GTOPS-6386')

description_GTOPS = issue.fields.activity

#print(transitions)

transitions = jira.transitions('GTOPS-6386')
for transition in transitions:
    print(f'ID: {transition["id"]}, Name: {transition["name"]}')


custom_field_id = ('customfield_23709')  # id поле с видом услуги
custom_field_value = issue.raw['fields'][custom_field_id]
print(f"Приоритет СРО: {custom_field_value}")'''