# tutorial: http://pbpython.com/pdf-reports.html

# import
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

# choose template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("myreport.html")

# define content in the file
template_vars = {"title" : "Workout summary report",
                 "empty_weeks": str(empty_weeks),
                 "nrweeks": str(nrweeks), # qq can i remove this line?
                 #"df_head": df_head.to_html()
                 "stretch_describe": stretch_describe,
                 "recent_entries": recent_entries.to_html(),
                 }

# create html
html_out = template.render(template_vars)

# write html file
with open('report/generated.html', 'w') as f:
    f.write(html_out)

# write pdf file
HTML(string=html_out).write_pdf("report/generated.pdf")
