from datetime import datetime

import xlwt
from django.http import HttpResponse

MDATA = datetime.now().strftime('%Y-%m-%d')


def export_xlsx(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            if col == 9:
                b = str(val)
                val = str(val).split()
                date = val[0].split('-')
                date_ = date[3::-1]
                hours = val[1][0:8]
                convert_hours = int(hours[0:2]) - 3
                val = f'{"/".join(date_)} {convert_hours}:{hours[3:8]}'
                
            ws.write(row_num, col, str(val), default_style)

    wb.save(response)
    return response