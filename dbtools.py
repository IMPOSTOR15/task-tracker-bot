import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
async def create_pool():
    global POOL
    POOL = await asyncpg.create_pool(DATABASE_URL)


async def get_pool_connection():
    return POOL.acquire()


class PoolConnection:
    async def __aenter__(self):
        self.conn = await POOL.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await POOL.release(self.conn)


async def init_db():
    async with PoolConnection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id BIGINT PRIMARY KEY,
                task_category TEXT,
                task_subcategory TEXT,
                period_date TEXT,
                task_description TEXT,
                competitors_links TEXT,
                goods_sku TEXT,
                goods_info TEXT,
                task_action TEXT,
                add_by_user_id BIGINT,
                chat_id BIGINT,
                task_date TEXT,
                task_report_week TEXT,
                warehouse TEXT
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS incedents (
                id BIGINT PRIMARY KEY,
                type TEXT,
                work_category TEXT,
                incedent_description TEXT
            )
        """)


async def insert_task(
        task_category: str = "-",
        task_subcategory: str = "-",
        period_date: str = "-",
        task_description: str = "-",
        competitors_links: str = "-",
        goods_sku: str = "-",
        goods_info: str = "-",
        task_action: str = "-",
        add_by_user_id: int = None,
        chat_id: int = None,
        task_date: str = "-",
        task_report_week: str = "-",
        warehouse: str = "-",
    ) -> int:
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO tasks (
                task_category,
                task_subcategory,
                period_date,
                task_description,
                competitors_links,
                goods_sku,
                goods_info,
                task_action,
                add_by_user_id,
                chat_id,
                task_date,
                task_report_week,
                warehouse
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
            RETURNING id
            """,
            task_category,
            task_subcategory,
            period_date,
            task_description,
            competitors_links,
            goods_sku,
            goods_info,
            task_action,
            add_by_user_id,
            chat_id,
            task_date,
            task_report_week,
            warehouse
        )
        return row['id']


async def insert_incedent(
        type: str = "-",
        work_category: str = "-",
        incedent_description: str = "-"
    ):
    async with PoolConnection() as conn:
        await conn.execute(
            """
            INSERT INTO incedents (
                type,
                work_category,
                incedent_description
            ) VALUES ($1, $2, $3)
            """,
            type,
            work_category,
            incedent_description
        )

async def insert_file_photo(
        type: str = "photo",
        task_id: int = None,
        file_path: str = "-",
    ):
    async with PoolConnection() as conn:
        await conn.execute(
            """
            INSERT INTO files (
                type,
                task_id,
                file_path
            ) VALUES ($1, $2, $3)
            """,
            type,
            task_id,
            file_path
        )

async def insert_file_document(
        type: str = "document",
        task_id: int = None,
        file_path: str = "-",
    ):
    async with PoolConnection() as conn:
        await conn.execute(
            """
            INSERT INTO files (
                type,
                task_id,
                file_path
            ) VALUES ($1, $2, $3)
            """,
            type,
            task_id,
            file_path
        )

#Запись к строке файла айди его задачи        
async def mark_task_id_file(task_id: int, file_path: str):
    if task_id is None or file_path == "-":
        raise ValueError("task_id and file_path must be provided")

    async with PoolConnection() as conn:
        await conn.execute(
            """
            UPDATE files
            SET task_id = $1
            WHERE file_path = $2
            """,
            task_id,
            file_path
        )