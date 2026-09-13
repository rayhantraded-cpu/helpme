import os
import sqlite3
import traceback
from pathlib import Path
import flet as ft

# ==========================================
# 1. إعدادات قاعدة البيانات (النسخة الآمنة لأندرويد)
# ==========================================
APP_DIR_NAME = "personal_productivity_app"
DB_FILE_NAME = "personal_assistant.db"

def get_storage_path() -> Path:
    # الدرع الواقي: في أندرويد المجلد الحالي هو المساحة الوحيدة المسموحة للكتابة
    cwd = Path(os.getcwd())
    app_dir = cwd / APP_DIR_NAME
    try:
        app_dir.mkdir(parents=True, exist_ok=True)
        return app_dir
    except Exception:
        # إذا رفض النظام إنشاء مجلد فرعي، نستخدم المجلد الجذري للتطبيق مباشرة
        return cwd

DB_NAME = str(get_storage_path() / DB_FILE_NAME)

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    # تم تغيير WAL إلى DELETE لضمان استقرار أندرويد ومنع تجميد الملفات
    conn.execute("PRAGMA journal_mode = DELETE")
    return conn

def init_db():
    with connect_db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                icon_name TEXT NOT NULL DEFAULT 'category',
                color_code TEXT NOT NULL DEFAULT '#607D8B'
            );

            CREATE TABLE IF NOT EXISTS task_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                frequency_type TEXT NOT NULL
                    CHECK(frequency_type IN ('DAILY','WEEKLY','MONTHLY')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                list_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                resource_url TEXT DEFAULT '',
                frequency_type TEXT NOT NULL
                    CHECK(frequency_type IN ('DAILY','WEEKLY','MONTHLY')),
                target_count INTEGER NOT NULL DEFAULT 1,
                advice_text TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(list_id) REFERENCES task_lists(id) ON DELETE CASCADE,
                FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE RESTRICT
            );

            CREATE TABLE IF NOT EXISTS task_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                period_identifier TEXT NOT NULL,
                completed_count INTEGER NOT NULL DEFAULT 0,
                is_completed INTEGER NOT NULL DEFAULT 0,
                last_updated TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(task_id, period_identifier),
                FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_tasks_period
                ON tasks(frequency_type);

            CREATE INDEX IF NOT EXISTS idx_tasks_category
                ON tasks(category_id);

            CREATE INDEX IF NOT EXISTS idx_logs_period
                ON task_logs(period_identifier);
            """
        )

        categories = [
            ("مهام روحية", "auto_awesome", "#7E57C2"),
            ("مهام بدنية وصحية", "fitness_center", "#43A047"),
            ("مهام تطويرية", "rocket_launch", "#1E88E5"),
            ("مهام تعليمية", "menu_book", "#FB8C00"),
            ("مهام اجتماعية", "groups", "#00897B"),
            ("مهام اقتصادية", "payments", "#F9A825"),
        ]
        conn.executemany(
            """
            INSERT OR IGNORE INTO categories(name, icon_name, color_code)
            VALUES (?, ?, ?)
            """,
            categories,
        )

        lists = [
            ("المهام اليومية", "DAILY"),
            ("المهام الأسبوعية", "WEEKLY"),
            ("المهام الشهرية", "MONTHLY"),
        ]
        for title, freq in lists:
            conn.execute(
                """
                INSERT INTO task_lists(title, frequency_type)
                SELECT ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM task_lists WHERE frequency_type = ?
                )
                """,
                (title, freq, freq),
            )

        defaults = {
            "points": "0",
            "streak": "0",
            "last_completion_date": "",
            "theme_mode": "light",
            "version": "2",
        }
        for key, value in defaults.items():
            conn.execute(
                "INSERT OR IGNORE INTO app_state(key, value) VALUES (?, ?)",
                (key, value),
            )

# ==========================================
# 2. واجهة التطبيق وصائد الأخطاء
# ==========================================
def main(page: ft.Page):
    page.title = "المساعد الشخصي"
    page.rtl = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # عنوان ترحيبي
    page.add(
        ft.Text("مرحباً أحمد! نظام كشف الأخطاء يعمل 🔍", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
    )

    try:
        # هنا السحر: نقوم بتشغيل قاعدة البيانات "بعد" أن تفتح الشاشة وليس قبلها!
        init_db()
        
        # إذا نجح السطر السابق، ستظهر هذه الرسالة الخضراء
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("✅ قاعدة البيانات (SQLite) تعمل بنجاح تام!", color=ft.colors.GREEN_800, weight=ft.FontWeight.BOLD),
                    ft.Text(f"تم حفظ الملف في المسار التالي:\n{DB_NAME}", size=12, color=ft.colors.BLUE_700, selectable=True)
                ]),
                bgcolor=ft.colors.GREEN_50,
                padding=15,
                border_radius=10
            )
        )
        
    except Exception as e:
        # إذا حدث أي خطأ برمجياً أو في الصلاحيات، لن ينهار التطبيق! بل سيكتب لك الخطأ على الشاشة لتقرأه
        error_details = traceback.format_exc()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("❌ حدث خطأ منع تشغيل قاعدة البيانات:", color=ft.colors.RED_800, weight=ft.FontWeight.BOLD),
                    ft.Text(error_details, size=11, color=ft.colors.RED_900, selectable=True)
                ]),
                bgcolor=ft.colors.RED_50,
                padding=15,
                border_radius=10
            )
        )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
