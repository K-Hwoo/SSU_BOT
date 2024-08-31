import pymysql, openpyxl

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../config'))
from DatabaseConfig import *

def all_clear_train_data(db) :
    # 기존 학습 데이터 삭제
    sql = '''
        delete from question_answer_pairs
    '''
    with db.cursor() as cursor :
        cursor.execute(sql)
    
    # auto increment 초기화
    sql = '''
        ALTER TABLE question_answer_pairs AUTO_INCREMENT=1
    '''
    
    with db.cursor() as cursor :
        cursor.execute(sql)
        
def insert_data(db, xls_row) :
    intent, query, answer, answer_img_url = xls_row
    
    sql = '''
        INSERT question_answer_pairs (intent, query, answer, answer_image)
        VALUES ('%s', '%s', '%s', '%s')
    ''' % (intent.value, query.value, answer.value, answer_img_url.value)
    
    sql = sql.replace("'None'", "NULL")
    
    with db.cursor() as cursor :
        cursor.execute(sql)
        print(f"\"{query.value}\" 저장")
        db.commit()


train_file = "train_tools/qna/answer_data.xlsx"

db = None
try :
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset="utf8"
    )
    
    all_clear_train_data(db)
    
    wb = openpyxl.load_workbook(train_file)
    sheet = wb["Sheet1"]
    for row in sheet.iter_rows(min_row=2) :
        insert_data(db, row)
        
    wb.close()
    
except Exception as e :
    print(e)
    
finally :
    if db is not None :
        db.close()