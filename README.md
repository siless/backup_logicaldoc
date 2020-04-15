# backup_logicaldoc
Backup routine for logicaldoc community

Logicaldoc community has no (https://www.logicaldoc.com/download-logicaldoc-community) backup functionality to save your data. 
The wiki/forum offers some ideas that is necessary for backing up or restoring your data. However, it does not show you a proper way to do it. 
I made an easy to use program for backing up / [restoring | migration] / installing of your data.

Requirements:
- The script uses mysqldump -> mysql databaase is recommended
- no extra pip installations are needed -> hit n run program
- ./src/conf/backup.ini -> all settings that are needed