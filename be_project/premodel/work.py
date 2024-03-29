from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

doc = SimpleDocTemplate("simple_table.pdf", pagesize=letter)
# container for the 'Flowable' objects
elements = []

data = []
for head, ans1, ans2, ans3 in mapped:
    data.append([head, ans1, ans2, ans3])

'''data = [['00', '01', '02', '03', '04'],
        ['10', '11', '12', '13', '14'],
        ['20', '21', '22', '23', '24'],
        ['30', '31', '32', '33', '34']]'''

t = Table(data)
t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),
                       ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))
elements.append(t)
# write the document to disk
doc.build(elements)