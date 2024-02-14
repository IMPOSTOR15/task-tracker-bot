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
                warehouse TEXT,
                is_complete TEXT
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS incedents (
                id BIGINT PRIMARY KEY,
                type TEXT,
                work_category TEXT,
                incedent_description TEXT,
                is_complete TEXT
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id BIGINT PRIMARY KEY,
                chat_id BIGINT,
                admin_id BIGINT,
                sheet_name TEXT
            )
        """)

async def get_chat_sheet(chat_id: int):
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            "SELECT sheet_name, table_link FROM chats WHERE chat_id = $1", chat_id
        )
        return row  # Возвращает None, если запись отсутствует


async def insert_chat_sheet(chat_id: int, sheet_name: str, admin_id: int, table_link: str):
    async with PoolConnection() as conn:
        await conn.execute(
            """
            INSERT INTO chats (chat_id, admin_id, sheet_name, table_link)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (chat_id) DO UPDATE
            SET admin_id = EXCLUDED.admin_id,
                sheet_name = EXCLUDED.sheet_name,
                table_link = EXCLUDED.table_link
            """,
            chat_id,
            admin_id,
            sheet_name,
            table_link
        )
        
async def get_sheet_name_by_chat_id(chat_id: int):
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            """
            SELECT sheet_name FROM chats
            WHERE chat_id = $1
            """,
            chat_id
        )
        if row:
            return row['sheet_name']
        else:
            return None
        
async def get_sheet_url_by_chat_id(chat_id: int):
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            """
            SELECT table_link FROM chats
            WHERE chat_id = $1
            """,
            chat_id
        )
        if row:
            return row['table_link']
        else:
            return None
        
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
        is_complete: str = "-"
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
                warehouse,
                is_complete
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
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
            warehouse,
            is_complete
        )
        return row['id']


async def insert_incedent(
        type: str = "-",
        work_category: str = "-",
        incedent_description: str = "-",
        is_complete: str = "-"
    ) -> int:
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO incedents (
                type,
                work_category,
                incedent_description,
                is_complete
            ) VALUES ($1, $2, $3, $4)
            RETURNING id
            """,
            type,
            work_category,
            incedent_description,
            is_complete
        )
        return row['id']

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


async def get_chat_id_to_alert(sheet_name: str):
    async with PoolConnection() as conn:
        row = await conn.fetchrow(
            """
            SELECT chat_id FROM alerts_chats
            WHERE sheet_name = $1
            """,
            sheet_name
        )
        if row:
            return row['chat_id']
        else:
            return None


async def insert_chat_id_to_alert(chat_id: int, sheet_name: str):
    async with PoolConnection() as conn:
        existing_record = await conn.fetchrow(
            """
            SELECT 1 FROM alerts_chats
            WHERE chat_id = $1 AND sheet_name = $2
            """,
            chat_id,
            sheet_name
        )

        if not existing_record:
            await conn.execute(
                """
                INSERT INTO alerts_chats (
                    chat_id,
                    sheet_name
                ) VALUES ($1, $2)
                """,
                chat_id,
                sheet_name
            )



async def delete_chat_id_from_alert(chat_id: int, sheet_name: str):
    async with PoolConnection() as conn:
        existing_record = await conn.fetchrow(
            """
            SELECT 1 FROM alerts_chats
            WHERE chat_id = $1 AND sheet_name = $2
            """,
            chat_id,
            sheet_name
        )

        if existing_record:
            await conn.execute(
                """
                DELETE FROM alerts_chats
                WHERE chat_id = $1 AND sheet_name = $2
                """,
                chat_id,
                sheet_name
            )

async def update_status_and_fetch_differences(items):
    async with PoolConnection() as conn:
        updated_items = []
        print(items)
        for item in items:
            if item['type'] == 'Неизвестно':
                continue
            table_name = 'tasks' if item['type'] == 'Задача' else 'incedents'
            existing_status = await conn.fetchval(
                f"""
                SELECT is_complete FROM {table_name}
                WHERE id = $1
                """,
                int(item['id'])
            )

            existing_status = '' if existing_status == '-' else existing_status
            print(existing_status)
            print(item['status'])
            if existing_status != item['status']:
                await conn.execute(
                    f"""
                    UPDATE {table_name}
                    SET is_complete = $1
                    WHERE id = $2
                    """,
                    item['status'], int(item['id'])
                )
                updated_items.append({
                    "id": item['id'],
                    "type": item['type'],
                    "status": item['status'],
                    "info": item['info']
                })

        return updated_items

async def get_all_chats():
    chats = []
    async with PoolConnection() as conn:
        rows = await conn.fetch(
            """
            SELECT chat_id, sheet_name, table_link
            FROM chats
            """
        )
        for row in rows:
            chats.append({
                "chat_id": row["chat_id"],
                "sheet_name": row["sheet_name"],
                "table_link": row["table_link"],
            })
    return chats