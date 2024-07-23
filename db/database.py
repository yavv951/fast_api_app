from sqlalchemy import create_engine, MetaData, text

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Позволяет нескольким потокам работать с одной базой данных
)
metadata = MetaData()


# Установка режима WAL и других параметров
def set_pragmas(engine):
    with engine.connect() as conn:
        conn.execute(text("PRAGMA journal_mode=WAL;"))
        conn.execute(text("PRAGMA synchronous=NORMAL;"))


# Установите PRAGMA после создания метаданных
metadata.create_all(bind=engine)
set_pragmas(engine)
