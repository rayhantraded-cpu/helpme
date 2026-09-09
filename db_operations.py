import sqlite3
from datetime import datetime

DB_NAME = "personal_assistant.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# 1. جلب القوائم (التبويبات)
def get_all_task_lists():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, frequency_type FROM task_lists ORDER BY id DESC")
    lists = cursor.fetchall()
    conn.close()
    return lists

# 2. إضافة قائمة مهام جديدة
def add_task_list(title, frequency_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO task_lists (title, frequency_type) VALUES (?, ?)", (title, frequency_type))
    conn.commit()
    conn.close()

# 3. جلب التصنيفات الستة الأساسية
def get_categories():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, color_code FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories

# 4. إضافة مهمة جديدة
def add_task(list_id, category_id, title, resource_url, frequency_type, target_count, advice_text):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    INSERT INTO tasks (list_id, category_id, title, resource_url, frequency_type, target_count, advice_text)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (list_id, category_id, title, resource_url, frequency_type, target_count, advice_text))
    conn.commit()
    conn.close()

# 5. جلب المهام لشاشة مجال معين داخل قائمة
def get_tasks_by_list_and_category(list_id, category_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT id, title, resource_url, frequency_type, target_count, advice_text
    FROM tasks
    WHERE list_id = ? AND category_id = ?
    ORDER BY id DESC
    '''
    cursor.execute(query, (list_id, category_id))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# 6. جلب مهام الشريط المنسحب (الإنجاز) غير المكتملة
def get_pending_tasks_for_period(period_id, freq_type):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    SELECT t.id, t.title, t.resource_url, t.target_count, t.advice_text, c.name
    FROM tasks t
    JOIN categories c ON t.category_id = c.id
    LEFT JOIN task_logs l ON t.id = l.task_id AND l.period_identifier = ?
    WHERE t.frequency_type = ? AND (l.is_completed IS NULL OR l.is_completed = 0)
    '''
    cursor.execute(query, (period_id, freq_type))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# 7. تسجيل إنجاز المهمة (لتختفي وتظهر غداً/الفترة القادمة)
def complete_task(task_id, period_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = '''
    INSERT INTO task_logs (task_id, period_identifier, completed_count, is_completed)
    VALUES (?, ?, 1, 1)
    ON CONFLICT(task_id, period_identifier)
    DO UPDATE SET is_completed = 1, completed_count = completed_count + 1, last_updated = CURRENT_TIMESTAMP
    '''
    cursor.execute(query, (task_id, period_id))
    conn.commit()
    conn.close()