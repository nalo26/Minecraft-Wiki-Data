import os

bind = f"{os.getenv('WEB_HOST')}:{os.getenv('WEB_PORT')}"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
accesslog = "-"
access_log_format = '%(t)s %({x-forwarded-for}i)s %(l)s "%(r)s" %(s)s'  # "%(a)s"'
