# backup_logicaldoc
Backup routine for logicaldoc community

Logicaldoc community has no <https://www.logicaldoc.com/download-logicaldoc-community> backup functionality to save your data. 
The wiki/forum offers some ideas that is necessary for backing up or restoring your data. However, it does not show you a proper way to do it. 
I made an easy to use program for backing up / restoring | migration] / installing of your data.

Requirements:
-   The script uses mysql.
-   No extra pip installations are needed. It is a hit and run program.
-   The programm must only be configured in ./src/conf/backup.ini
-   Initial installation of logicaldoc community must be done