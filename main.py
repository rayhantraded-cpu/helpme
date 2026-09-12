import datetime
import random
import flet as ft

# --- قوائم الرسائل التحفيزية ---
MORNING_MESSAGES = [
    "🌅 بركة يومك في بكورك! ابدأ بمهمة واحدة بسيطة الآن.",
    "☀️ صباح الهمة! انطلاقة جديدة ليوم مليء بالإنجاز.",
    "💪 صباح النشاط! تمارين بسيطة تمنحك حيوية تكفي ليوم كامل!",
]
AFTERNOON_MESSAGES = [
    "🌤️ جاء وقت العصر! خطوة صغيرة إضافية تصنع الفارق.",
    "☕ حان وقت الاستراحة وشحن الطاقة. ثم أكمل مسيرتك.",
]
EVENING_MESSAGES = [
    "🌙 هدوء المساء فرصة للراحة. الاستمرارية أهم من الكمال 🌿",
    "✨ أنجزت ما باستطاعتك اليوم، غداً يوم أفضل بإذن الله.",
]

# --- تصنيفات المهام ---
categories = [
    ("🕊️ مهام روحية", ft.colors.PURPLE_50, ft.colors.PURPLE_900),
    ("💪 مهام بدنية وصحية", ft.colors.GREEN_50, ft.colors.GREEN_900),
    ("🚀 مهام تطويرية", ft.colors.BLUE_50, ft.colors.BLUE_900),
    ("📚 مهام تعليمية", ft.colors.ORANGE_50, ft.colors.ORANGE_900),
    ("🤝 مهام اجتماعية", ft.colors.TEAL_50, ft.colors.TEAL_900),
    ("💰 مهام اقتصادية", ft.colors.AMBER_50, ft.colors.AMBER_900),
]

def main(page: ft.Page):
    page.title = "المساعد الشخصي"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0 
    page.spacing = 0

    # الذاكرة المؤقتة (تم إيقاف الحفظ المحلي مؤقتاً لاختبار الواجهة)
    user_stats = {"streak": 1, "points": 0}
    tasks_db = []
    current_context = {"category": "", "period": "يومية"}

    # --- الهيدر التحفيزي ---
    streak_text = ft.Text(f"{user_stats['streak']} أيام", weight=ft.FontWeight.BOLD, size=12)
    points_text = ft.Text(f"{user_stats['points']} نقطة", weight=ft.FontWeight.BOLD, size=12)

    def get_time_based_message():
        h = datetime.datetime.now().hour
        if 4 <= h < 11: return random.choice(MORNING_MESSAGES)
        elif 14 <= h < 18: return random.choice(AFTERNOON_MESSAGES)
        else: return random.choice(EVENING_MESSAGES)

    banner_tip = ft.Text(get_time_based_message(), size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, expand=True)

    motivation_header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.IconButton(icon=ft.icons.MENU, tooltip="إنجازات اليوم", on_click=lambda e: page.open(drawer)),
                ft.Container(content=ft.Row([ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color=ft.colors.ORANGE, size=18), streak_text]), bgcolor=ft.colors.ORANGE_50, padding=5, border_radius=15),
                ft.Container(content=ft.Row([ft.Icon(ft.icons.STAR, color=ft.colors.AMBER_800, size=18), points_text]), bgcolor=ft.colors.AMBER_50, padding=5, border_radius=15),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([ft.Icon(ft.icons.LIGHTBULB_OUTLINE, color=ft.colors.AMBER_700, size=18), banner_tip]),
        ]),
        bgcolor=ft.colors.WHITE70, padding=15, border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
        border=ft.border.only(bottom=ft.BorderSide(2, ft.colors.BLUE_100))
    )

    # --- الدرج الجانبي لتأكيد المهام ---
    achievements_list = ft.Column(spacing=10)

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("🏆 قائمة إنجازات المهام", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Divider(), 
                    ft.Column([achievements_list], scroll=ft.ScrollMode.AUTO, expand=True)
                ], expand=True), 
                padding=15, expand=True
            )
        ]
    )

    # --- النوافذ المنبثقة (إضافة مهمة) ---
    task_title_input = ft.TextField(label="نص المهمة", hint_text="أدخل تفاصيل المهمة...")
    task_link_input = ft.TextField(label="الرابط (اختياري)", expand=True)
    
    def paste_from_clipboard(e):
        try:
            if page.get_clipboard():
                task_link_input.value = page.get_clipboard()
                page.update()
        except:
            pass
            
    paste_btn = ft.IconButton(icon=ft.icons.CONTENT_PASTE, on_click=paste_from_clipboard, icon_color=ft.colors.BLUE_700)
    task_period_dropdown = ft.Dropdown(label="تكرار المهمة", value="يومية", options=[ft.dropdown.Option("يومية"), ft.dropdown.Option("أسبوعية"), ft.dropdown.Option("شهرية")])

    def save_new_task(e):
        if not task_title_input.value: return
        tasks_db.append({
            "id": str(random.randint(1000, 9999)),
            "title": task_title_input.value, 
            "link": task_link_input.value,
            "period": task_period_dropdown.value, 
            "category": current_context["category"], 
            "completed": False,
        })
        task_title_input.value = ""
        task_link_input.value = ""
        page.close(add_task_dialog)
        refresh_category_tasks_view()
        page.open(ft.SnackBar(content=ft.Text("تم حفظ المهمة بنجاح!")))

    add_task_dialog = ft.AlertDialog(
        title=ft.Text("إضافة مهمة جديدة", color=ft.colors.BLUE_900),
        content=ft.Column([task_title_input, ft.Row([task_link_input, paste_btn]), task_period_dropdown], tight=True, spacing=10),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: page.close(add_task_dialog)),
            ft.ElevatedButton("حفظ", on_click=save_new_task, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
        ],
    )

    # --- استعراض المهام داخل المجال ---
    category_tasks_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

    category_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("عرض المهام", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(category_sheet)),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Container(content=category_tasks_list, expand=True), 
                ft.Row([ft.ElevatedButton("إضافة مهمة جديدة (+)", icon=ft.icons.ADD, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, on_click=lambda e: page.open(add_task_dialog), expand=True)])
            ]), padding=20, height=550, bgcolor=ft.colors.WHITE, border_radius=ft.border_radius.only(top_left=20, top_right=20)
        ), dismissible=True,
    )

    def refresh_category_tasks_view():
        category_tasks_list.controls.clear()
        cat, per = current_context["category"], current_context["period"]
        filtered = [t for t in tasks_db if t["category"] == cat and t["period"] == per]
        if not filtered:
            category_tasks_list.controls.append(ft.Container(content=ft.Text("لا توجد مهام مضافة هنا.", color=ft.colors.GREY_600), padding=20, alignment=ft.alignment.center))
        else:
            for t in filtered:
                category_tasks_list.controls.append(
                    ft.Card(content=ft.ListTile(title=ft.Text(t["title"], weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)))
                )
        page.update()

    def open_category_sheet(category_name, period_name):
        current_context["category"] = category_name
        current_context["period"] = period_name
        refresh_category_tasks_view()
        page.open(category_sheet)

    # --- القوائم والتبويبات بخلفية متدرجة ---
    def build_vertical_menu(period_name):
        menu_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, padding=15)
        for cat_name, bg_col, text_col in categories:
            menu_column.controls.append(
                ft.Container(
                    content=ft.Row([ft.Text(cat_name, size=16, weight=ft.FontWeight.BOLD, color=text_col), ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16, color=text_col)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=ft.colors.WHITE, padding=18, border_radius=10, 
                    border=ft.border.all(1, ft.colors.BLUE_100), ink=True, 
                    on_click=lambda e, c=cat_name, p=period_name: open_category_sheet(c, p),
                )
            )
        return menu_column

    tabs = ft.Tabs(
        selected_index=0, expand=True, label_color=ft.colors.BLUE_900, indicator_color=ft.colors.BLUE_700,
        tabs=[
            ft.Tab(text="يومية", content=build_vertical_menu("يومية")),
            ft.Tab(text="أسبوعية", content=build_vertical_menu("أسبوعية")),
            ft.Tab(text="شهرية", content=build_vertical_menu("شهرية")),
        ],
    )

    # حاوية رئيسية بتدرج لوني أزرق فاتح
    main_layout = ft.Container(
        content=ft.Column([motivation_header, tabs], spacing=0, expand=True),
        expand=True,
        gradient=ft.LinearGradient(begin=ft.alignment.top_center, end=ft.alignment.bottom_center, colors=[ft.colors.BLUE_50, ft.colors.WHITE])
    )

    page.add(main_layout)

if __name__ == "__main__":
    ft.app(target=main)
