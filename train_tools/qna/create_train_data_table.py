import pymysql

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../config'))
from DatabaseConfig import *

db = None
try :
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset="utf8"
    )
    
    sql = '''
        CREATE TABLE IF NOT EXISTS `question_answer_pairs` (
        `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
        `intent` VARCHAR(45) NULL,
        `query` TEXT NULL,
        `answer` TEXT NOT NULL,
        `answer_image` VARCHAR(2048) NULL,
        PRIMARY KEY(`id`)
        ) ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''
    
    with db.cursor() as cursor :
        cursor.execute(sql)
        
except Exception as e :
    print(e)
    
finally :
    if db is not None :
        db.close()
