import xlwt
from datetime import datetime
from poll_app import celery_app
from django.contrib.auth.models import User
from django.core.mail import send_mail
from poll_app.models import Poll


@celery_app.task(bind=True)
def make_xls_export(self):
    filename = f'Results_{datetime.now().date()}.xls'
    # filepath = f'/fffolder/{filename}'
    # response = HttpResponse(content_type='application/ms-excel')
    # response['Content-Disposition'] = f'attachment; filename={filename}'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Poll Data')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'Название', 'Дата начала', 'Дата окончания', 'Макс. кол-во голосов', 'Статус голосования', 'Победитель', 'Участники']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    polls = Poll.objects.all()
    rows = []
    for poll in polls:
        lst = []
        lst.append(poll.id)
        lst.append(poll.title)
        lst.append(poll.date_start)
        lst.append(poll.date_end)
        lst.append(poll.max_vote)
        lst.append(poll.is_active)
        lst.append(str(poll.winner))
        pers = poll.persons.all().values('fio')
        s = ''
        for j in pers:
            s += str(j['fio']) + '; '
        lst.append(s)
        rows.append(lst)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(filename)

    return f'Made file {filename}'


@celery_app.task(bind=True)
def send_mail_task(self):
    subject = 'Уведомление'
    text_email = 'Создан файл с результатами голосаний.'
    receiv_email = User.objects.get(username='admin').email
    send_mail(subject, text_email, 'garmatenkoi@yandex.com', [receiv_email])
    return 'Email send...'
