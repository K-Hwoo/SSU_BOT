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


"""

질문 / 답변 데이터셋을 MySQL에 올리기 전,
TABLE을 생성하는 프로그랩입니다. (TABLE명 - question_answer_pairs)

- MySQL에 ssu_bot 데이터베이스가 존재해야함
- config/DatabaseConfig.py에 DB관련 정보 저장

"""
