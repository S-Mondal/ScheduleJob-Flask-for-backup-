from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger
from shutil import copyfile, rmtree
import datetime
from flask import Flask
import os

app = Flask(__name__)

@app.route('/backup/<path:file>')
def dailyBackup(file, max_backup_days=30, backup_folder_path="DBBackup/"):
    if not os.path.exists(file):
        return "File not found"

    print("Back up")

    # check if backup folder exists 
    if not os.path.exists(backup_folder_path):
         os.makedirs(backup_folder_path)

    # delete the folders which are max_backup_days older
    for (root, date_folders, _) in os.walk(backup_folder_path):
        folders = date_folders
        break
    folders.sort()
    for folder in folders[:-max_backup_days]:
        rmtree(os.path.join(backup_folder_path,folder))
        print("Deleted: ",folder)
    # create the backup folder and copy file
    datetime_folder = datetime.datetime.now()
    backupPath = os.path.join(backup_folder_path,str(datetime_folder))
    if not os.path.exists(backupPath):
        os.makedirs(backupPath)
    copyfile(file,os.path.join(backupPath,file))

    return "Backup Taken Successfully"


interval = IntervalTrigger(
    days = 1, # executed once a day
    start_date='2021-06-24 22:01:00',
    end_date='2023-01-01 23:23:59',
    timezone='Asia/Kolkata'
)

scheduler = APScheduler()
scheduler.add_job(func=dailyBackup,args=["demo.db"],kwargs={"max_backup_days":30, "backup_folder_path":"DBBackup/"},run_date='mon-fri', trigger=interval,id='running')
scheduler.start()


if __name__ == '__main__':
    app.run()