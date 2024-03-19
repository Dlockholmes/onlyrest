import os, schedule, time

def job():
    os.system("git pull origin main")
    os.system("cp /home/ignisytb/rest/app/static/dictionary data/todaylist /home/ignisytb/rest_git/app/static/dictionary data/todaylist")
    os.system("cp -r /home/ignisytb/rest_git/app/* /home/ignisytb/rest/app/")
    os.system("cp -r /home/ignisytb/rest_git/wsgi/* /home/ignisytb/rest/wsgi/")
    os.system("git add .")
    os.system("git commit -m '[server]'")
    os.system("git push origin main")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
