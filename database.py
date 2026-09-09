import sqlite3
import os

# اسم ملف قاعدة البيانات
DB_NAME = "personal_assistant.db"

def connect_db():
    """إنشاء اتصال بقاعدة البيانات وتفعيل قيود المفاتيح الأجنبية (Foreign Keys)"""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_tables():
    """إنشاء جداول التطبيق"""
    conn = connect_db()
    cursor = conn.cursor()

    # 1. جدول التصنيفات/المجالات الرئيسية
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        icon_name TEXT,
        color_code TEXT
    );
    ''')

    # 2. جدول قوائم المهام (التي تظهر في التبويبات)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_lists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        frequency_type TEXT NOT NULL CHECK (frequency_type IN ('DAILY', 'WEEKLY', 'MONTHLY')),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # 3. جدول المهام التفصيلية
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        list_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        resource_url TEXT,
        frequency_type TEXT NOT NULL CHECK (frequency_type IN ('DAILY', 'WEEKLY', 'MONTHLY')),
        target_count INTEGER DEFAULT 1,
        advice_text TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (list_id) REFERENCES task_lists(id) ON DELETE CASCADE,
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
    ''')

    # 4. جدول تتبع الإنجاز اليومي والدوري (للشاشة المنسحبة والتقارير)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        period_identifier TEXT NOT NULL, -- صيغة التاريخ: YYYY-MM-DD أو YYYY-Www أو YYYY-MM
        completed_count INTEGER DEFAULT 0,
        is_completed BOOLEAN DEFAULT 0 CHECK (is_completed IN (0, 1)),
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
        UNIQUE(task_id, period_identifier)
    );
    ''')

    # إدخال التصنيفات الستة الأساسية افتراضياً
    default_categories = [
        ("مهام روحية", "spiritual_icon", "#8E44AD"),
        ("مهام بدنية وصحية", "health_icon", "#2ECC71"),
        ("مهام تطويرية", "development_icon", "#3498DB"),
        ("مهام تعليمية", "education_icon", "#F39C12"),
        ("مهام اجتماعية", "social_icon", "#E67E22"),
        ("مهام اقتصادية", "economic_icon", "#1ABC9C")
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO categories (name, icon_name, color_code)
    VALUES (?, ?, ?);
    ''', default_categories)

    conn.commit()
    conn.close()
    print(" تم إنشاء قاعدة البيانات والجداول بنجاح.")

if __name__ == "__main__":
    create_tables()