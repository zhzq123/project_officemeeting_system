import os
import my_config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_name = 'project_office_system.sqlite'

if os.path.exists(db_name) and my_config.clear_all_database:
    os.remove(db_name)
    print("remove database")

engine = create_engine('sqlite:///' + db_name, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def drop_db():
    Base.metadata.drop_all(engine)


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    import dbmodel
    Base.metadata.create_all(bind=engine)
    