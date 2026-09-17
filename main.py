import os
import json
import datetime
import random
import traceback
import flet as ft

CATEGORY_TIPS = {
    "🕊️ مهام روحية": ["💡 مقترح: أذكار الصباح والمساء.", "💡 مقترح: مقرر الحفظ اليومي.", "💡 مقترح: قراءة ورد.", "💡 مقترح: صلاة الضحى والوتر."],
    "💪 مهام بدنية وصحية": ["💡 أوصيك: بالمشي لمدة 30 دقيقة.", "💡 أوصيك: بشرب ماء كافي.", "💡 أوصيك: بتمارين الضغط والسكوات."],
    "🚀 مهام تطويرية": ["💡 فكرة: قراءة 20 صفحة من كتاب.", "💡 فكرة: تعلم مهارة جديدة.", "💡 فكرة: الاستماع لبودكاست."],
    "📚 مهام تعليمية": ["💡 تذكير: مراجعة الدروس السابقة.", "💡 تذكير: التحضير للدرس القادم."],
    "🤝 مهام اجتماعية": ["💡 مقترح: الاطمئنان على الوالدين.", "💡 مقترح: مكالمة صديق قديم.", "💡 مقترح: إدخال السرور على محتاج."],
    "💰 مهام اقتصادية": ["💡 نصيحة: تسجيل مصروفاتك اليوم.", "💡 نصيحة: مراجعة خطة الادخار."]
}

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
    page.bgcolor = ft.colors.BLUE_50
    page.padding = 0 
    page.spacing = 0

    try:
        saved_stats = page.client_storage.get("user_stats")
        user_stats = json.loads(saved_stats) if saved_stats else {"streak": 1, "points": 0}
        
        saved_tasks = page.client_storage.get("tasks_db")
        tasks_db = json.loads(saved_tasks) if saved_tasks else []

        def save_data():
            page.client_storage.set("user_stats", json.dumps(user_stats))
            page.client_storage.set("tasks_db", json.dumps(tasks_db))

        current_context = {"category": "", "period": "يومية"}
        editing_task_id = [None] # متغير لتتبع ما إذا كنا في وضع الإضافة أو التعديل

        def update_task_states():
            now = datetime.datetime.now()
            changed = False
            for t in tasks_db:
                if "target_count" not in t: t["target_count"] = 1
                if "current_count" not in t: t["current_count"] = 1 if t.get("completed") else 0
                if "last_completed" not in t: t["last_completed"] = None
                if "next_show" not in t: t["next_show"] = None

                if t.get("last_completed"):
                    try:
                        last_time = datetime.datetime.fromisoformat(t["last_completed"])
                        reset = False
                        
                        if t["period"] == "يومية" and now.date() > last_time.date():
                            reset = True
                        elif t["period"] == "أسبوعية":
                            if now.isocalendar()[1] != last_time.isocalendar()[1] or now.year > last_time.year:
                                reset = True
                        elif t["period"] == "شهرية":
                            if now.month != last_time.month or now.year > last_time.year:
                                reset = True
                                
                        if reset:
                            t["current_count"] = 0
                            t["completed"] = False
                            t["next_show"] = None
                            changed = True
                    except Exception:
                        pass
            if changed:
                save_data()

        # ---------------------------------------------------------
        # Header (Top Bar)
        # ---------------------------------------------------------
        streak_text = ft.Text(f"{user_stats['streak']} أيام", weight=ft.FontWeight.BOLD, size=12)
        points_text = ft.Text(f"{user_stats['points']} نقطة", weight=ft.FontWeight.BOLD, size=12)

        MORNING_MESSAGES = ["🌅 بركة يومك في بكورك! ابدأ بمهمة واحدة الآن.", "☀️ صباح الهمة! انطلاقة جديدة ليوم مليء بالإنجاز."]
        AFTERNOON_MESSAGES = ["🌤️ جاء وقت العصر! خطوة صغيرة إضافية تصنع الفارق.", "☕ حان وقت الاستراحة وشحن الطاقة."]
        EVENING_MESSAGES = ["🌙 هدوء المساء فرصة للراحة.", "✨ أنجزت ما باستطاعتك اليوم، غداً يوم أفضل."]

        def get_time_based_message():
            h = datetime.datetime.now().hour
            if 4 <= h < 11: return random.choice(MORNING_MESSAGES)
            elif 14 <= h < 18: return random.choice(AFTERNOON_MESSAGES)
            else: return random.choice(EVENING_MESSAGES)

        banner_tip = ft.Text(get_time_based_message(), size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, expand=True)

        motivation_header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(icon=ft.icons.MENU, on_click=lambda e: (update_drawer_achievements(), page.open(drawer))),
                    ft.Row([
                        ft.Container(content=ft.Row([ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color=ft.colors.ORANGE, size=18), streak_text]), bgcolor=ft.colors.ORANGE_50, padding=5, border_radius=15),
                        ft.Container(content=ft.Row([ft.Icon(ft.icons.STAR, color=ft.colors.AMBER_800, size=18), points_text]), bgcolor=ft.colors.AMBER_50, padding=5, border_radius=15),
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Icon(ft.icons.LIGHTBULB_OUTLINE, color=ft.colors.AMBER_700, size=18), banner_tip]),
            ]),
            bgcolor=ft.colors.WHITE, padding=15, 
            border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
            border=ft.border.only(bottom=ft.BorderSide(2, ft.colors.BLUE_100))
        )

        # ---------------------------------------------------------
        # قائمة الإنجازات (الدرج الجانبي) - هنا يتم التأشير على المهام
        # ---------------------------------------------------------
        achievements_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        def complete_task_action(e):
            task_id = e.control.data
            now = datetime.datetime.now()
            for t in tasks_db:
                if t["id"] == task_id:
                    t["current_count"] = t.get("current_count", 0) + 1
                    t["last_completed"] = now.isoformat()
                    
                    if t["current_count"] < t.get("target_count", 1):
                        t["next_show"] = (now + datetime.timedelta(hours=1)).isoformat()
                        page.open(ft.SnackBar(content=ft.Text("تم الإنجاز! ستظهر مجدداً لاحقاً لإكمال العدد المتبقي.")))
                    else:
                        t["completed"] = True
                        t["next_show"] = None
                        page.open(ft.SnackBar(content=ft.Text("🎉 ممتاز! أكملت المهمة بالكامل.")))
                    
                    user_stats["points"] += 10
                    break
            
            points_text.value = f"{user_stats['points']} نقطة"
            save_data()
            update_drawer_achievements() # تحديث القائمة الجانبية لإخفاء المهمة المنجزة

        def update_drawer_achievements():
            update_task_states()
            achievements_list.controls.clear()
            now = datetime.datetime.now()
            
            # جلب المهام غير المكتملة والتي ليس عليها حظر زمني
            pending_tasks = []
            for t in tasks_db:
                if t.get("current_count", 0) < t.get("target_count", 1):
                    if t.get("next_show") and now < datetime.datetime.fromisoformat(t["next_show"]):
                        continue # تأجيل
                    pending_tasks.append(t)

            if not pending_tasks:
                achievements_list.controls.append(ft.Text("أنجزت جميع المهام المتاحة حالياً! 🌟", color=ft.colors.GREEN_700))
            else:
                achievements_list.controls.append(ft.Text("أشر على المهام المنجزة:", size=12, color=ft.colors.GREY_600))
                for task in pending_tasks:
                    cb = ft.Checkbox(
                        label=f"{task['title']} ({task.get('current_count',0)}/{task.get('target_count',1)})", 
                        value=False, data=task["id"], on_change=complete_task_action
                    )
                    achievements_list.controls.append(ft.Container(content=cb, padding=5, bgcolor=ft.colors.BLUE_50, border_radius=5))
            page.update()

        drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(
                    content=ft.Column([
                        ft.Text("🏆 إنجازات اليوم", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Divider(), 
                        achievements_list
                    ]), padding=15
                )
            ]
        )

        # ---------------------------------------------------------
        # شاشة الإضافة والتعديل (بدون تمدد مزعج)
        # ---------------------------------------------------------
        task_title_input = ft.TextField(label="نص المهمة", width=300)
        task_link_input = ft.TextField(label="الرابط (اختياري)", width=300)
        task_target_count_input = ft.TextField(label="العدد", value="1", keyboard_type=ft.KeyboardType.NUMBER, width=145)
        task_period_dropdown = ft.Dropdown(label="التكرار", value="يومية", options=[ft.dropdown.Option("يومية"), ft.dropdown.Option("أسبوعية"), ft.dropdown.Option("شهرية")], width=145)

        def open_add_edit_dialog(task=None):
            if task:
                editing_task_id[0] = task["id"]
                add_task_dialog.title.value = "تعديل المهمة"
                task_title_input.value = task["title"]
                task_link_input.value = task.get("link", "")
                task_target_count_input.value = str(task.get("target_count", 1))
                task_period_dropdown.value = task.get("period", "يومية")
            else:
                editing_task_id[0] = None
                add_task_dialog.title.value = "إضافة مهمة جديدة"
                task_title_input.value = ""
                task_link_input.value = ""
                task_target_count_input.value = "1"
                task_period_dropdown.value = "يومية"
            
            page.open(add_task_dialog)
            page.update()

        def save_task(e):
            if not task_title_input.value: return
            try:
                t_count = int(task_target_count_input.value)
            except ValueError:
                t_count = 1
                
            if editing_task_id[0]: # حالة التعديل
                for t in tasks_db:
                    if t["id"] == editing_task_id[0]:
                        t["title"] = task_title_input.value
                        t["link"] = task_link_input.value
                        t["period"] = task_period_dropdown.value
                        t["target_count"] = t_count
                        break
                msg = "تم تعديل المهمة بنجاح!"
            else: # حالة الإضافة
                tasks_db.append({
                    "id": str(random.randint(10000, 99999)),
                    "title": task_title_input.value, 
                    "link": task_link_input.value,
                    "period": task_period_dropdown.value, 
                    "category": current_context["category"], 
                    "completed": False,
                    "target_count": t_count,
                    "current_count": 0,
                    "last_completed": None,
                    "next_show": None
                })
                msg = "تم حفظ المهمة بنجاح!"
                
            save_data()
            page.close(add_task_dialog)
            refresh_category_tasks_view()
            page.open(ft.SnackBar(content=ft.Text(msg)))

        add_task_dialog = ft.AlertDialog(
            title=ft.Text("إضافة مهمة", color=ft.colors.BLUE_900),
            content=ft.Column([
                task_title_input, 
                task_link_input, 
                ft.Row([task_target_count_input, task_period_dropdown], spacing=10)
            ], tight=True), # tight=True تمنع التمدد المزعج
            actions=[
                ft.TextButton("إلغاء", on_click=lambda e: page.close(add_task_dialog)),
                ft.ElevatedButton("حفظ", on_click=save_task, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE),
            ],
        )

        # ---------------------------------------------------------
        # شاشة المهام التفصيلية (مرقمة + مقترحات في الشريط)
        # ---------------------------------------------------------
        category_tasks_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO) 
        category_tip_text = ft.Text("", size=11, color=ft.colors.BLUE_700, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER, expand=True)

        category_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    # التوجيهات أصبحت في الوسط بين المهام وزر الإغلاق
                    ft.Row([
                        ft.Text("المهام", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        category_tip_text,
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(category_sheet)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    ft.Container(content=category_tasks_list, expand=True),
                    ft.SafeArea(
                        ft.Row([
                            ft.ElevatedButton("إضافة مهمة (+)", icon=ft.icons.ADD, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, on_click=lambda e: open_add_edit_dialog(), expand=True)
                        ])
                    )
                ]), padding=20, bgcolor=ft.colors.WHITE, border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ), dismissible=True,
        )

        def refresh_category_tasks_view():
            category_tasks_list.controls.clear()
            cat, per = current_context["category"], current_context["period"]
            
            # جلب كل المهام المتعلقة بهذا القسم وهذه الفترة (بدون إخفاء المنجز)
            cat_tasks = [t for t in tasks_db if t["category"] == cat and t["period"] == per]

            if not cat_tasks:
                category_tasks_list.controls.append(ft.Container(content=ft.Text("لا توجد مهام مدرجة هنا بعد.", color=ft.colors.GREY_600), padding=20, alignment=ft.alignment.center))
            else:
                for index, t in enumerate(cat_tasks, 1): # ترقيم المهام 1, 2, 3
                    task_url = t.get("link", "")
                    link_btn = ft.IconButton(icon=ft.icons.LINK, icon_color=ft.colors.BLUE, on_click=lambda e, u=task_url: page.launch_url(u)) if task_url else ft.Container()
                    edit_btn = ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.GREY_600, on_click=lambda e, task=t: open_add_edit_dialog(task))
                    
                    status = "✅" if t.get("current_count",0) >= t.get("target_count",1) else "⏳"
                    
                    task_card = ft.Card(
                        color=ft.colors.WHITE, elevation=1,
                        content=ft.ListTile(
                            leading=ft.Text(f"{index}-", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, size=16),
                            title=ft.Text(t['title'], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(f"مطلوب: {t.get('target_count',1)} مرات {status}", size=11, color=ft.colors.GREY_600),
                            trailing=ft.Row([link_btn, edit_btn], spacing=0, tight=True),
                            on_click=lambda e, task=t: open_add_edit_dialog(task) # يفتح التعديل عند الضغط على المهمة
                        )
                    )
                    category_tasks_list.controls.append(task_card)
            page.update()

        def open_category_sheet(category_name, period_name):
            current_context["category"] = category_name
            current_context["period"] = period_name
            tips_list = CATEGORY_TIPS.get(category_name, ["💡 توكل على الله وابدأ."])
            category_tip_text.value = random.choice(tips_list)
            
            refresh_category_tasks_view()
            page.open(category_sheet)

        # ---------------------------------------------------------
        # شاشة الإعدادات
        # ---------------------------------------------------------
        def toggle_theme(e):
            page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
            page.update()

        settings_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("⚙️ الإعدادات", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(settings_sheet)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    ft.Switch(label="الوضع الليلي (Dark Mode)", value=False, on_change=toggle_theme),
                    ft.ElevatedButton("تسجيل النسخة (قريباً)", icon=ft.icons.SECURITY, disabled=True, expand=True),
                    ft.ElevatedButton("نسخ البيانات احتياطياً", icon=ft.icons.BACKUP, on_click=lambda e: (page.set_clipboard(json.dumps(tasks_db)), page.open(ft.SnackBar(content=ft.Text("تم نسخ البيانات للحافظة!")))), expand=True),
                    ft.ElevatedButton("ملاحظات للمطور", icon=ft.icons.FEEDBACK, expand=True),
                ], spacing=10), padding=20, bgcolor=ft.colors.WHITE, border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ), dismissible=True,
        )

        # ---------------------------------------------------------
        # شاشة التقارير
        # ---------------------------------------------------------
        reports_content = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

        reports_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text("📊 تقرير الإنجاز", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(reports_sheet)),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    ft.Container(content=reports_content, expand=True),
                ]), padding=20, bgcolor=ft.colors.WHITE, border_radius=ft.border_radius.only(top_left=20, top_right=20)
            ), dismissible=True,
        )

        def open_reports_sheet(e):
            update_task_states()
            reports_content.controls.clear()
            total_tasks = len(tasks_db)
            completed_tasks = sum(1 for t in tasks_db if t.get("current_count", 0) >= t.get("target_count", 1))
            ratio = (completed_tasks / total_tasks) if total_tasks > 0 else 0

            kpi_row = ft.Row([
                ft.Container(content=ft.Column([ft.Text("المهام"), ft.Text(str(total_tasks), size=20, weight=ft.FontWeight.BOLD)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor=ft.colors.BLUE_50, padding=10, border_radius=8, expand=True),
                ft.Container(content=ft.Column([ft.Text("المنجزة"), ft.Text(str(completed_tasks), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)], horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor=ft.colors.GREEN_50, padding=10, border_radius=8, expand=True),
            ], spacing=10)

            reports_content.controls.extend([
                kpi_row,
                ft.Row([ft.Text("التقدم العام", weight=ft.FontWeight.BOLD), ft.Text(f"{int(ratio*100)}%")], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.ProgressBar(value=ratio, color=ft.colors.GREEN, bgcolor=ft.colors.GREY_200, height=10),
                ft.Divider(),
            ])

            for cat_name, bg_col, text_col in categories:
                cat_tasks = [t for t in tasks_db if t.get("category") == cat_name]
                if cat_tasks:
                    cat_total = len(cat_tasks)
                    cat_done = sum(1 for t in cat_tasks if t.get("current_count", 0) >= t.get("target_count", 1))
                    cat_ratio = cat_done / cat_total
                    reports_content.controls.append(
                        ft.Column([
                            ft.Row([ft.Text(cat_name, size=13), ft.Text(f"{int(cat_ratio*100)}%", size=13, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.ProgressBar(value=cat_ratio, color=text_col, bgcolor=bg_col, height=6)
                        ], spacing=3)
                    )

            page.open(reports_sheet)
            page.update()

        # ---------------------------------------------------------
        # بناء القائمة الرئيسية (التبويبات)
        # ---------------------------------------------------------
        def build_vertical_menu(period_name):
            menu_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)
            for cat_name, bg_col, text_col in categories:
                menu_column.controls.append(
                    ft.Container(
                        content=ft.Row([ft.Text(cat_name, size=16, weight=ft.FontWeight.BOLD, color=text_col), ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16, color=text_col)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        bgcolor=ft.colors.WHITE, padding=18, border_radius=10, 
                        border=ft.border.all(1, ft.colors.BLUE_100), ink=True, 
                        on_click=lambda e, c=cat_name, p=period_name: open_category_sheet(c, p),
                    )
                )
            return ft.Container(content=menu_column, padding=15)

        tabs = ft.Tabs(
            selected_index=0, expand=True,
            label_color=ft.colors.BLUE_900, indicator_color=ft.colors.BLUE_700,
            tabs=[
                ft.Tab(text="يومية", icon=ft.icons.TODAY, content=build_vertical_menu("يومية")),
                ft.Tab(text="أسبوعية", icon=ft.icons.DATE_RANGE, content=build_vertical_menu("أسبوعية")),
                ft.Tab(text="شهرية", icon=ft.icons.CALENDAR_MONTH, content=build_vertical_menu("شهرية")),
            ],
        )

        # ---------------------------------------------------------
        # شريط الأزرار السفلي (حجم أصغر، وإغلاق حقيقي)
        # ---------------------------------------------------------
        # تصغير الخط والهوامش لمنع التداخل والنزول لسطر جديد
        nav_btn_style = ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=2, vertical=10),
            text_style=ft.TextStyle(size=11, weight=ft.FontWeight.BOLD)
        )
        
        def close_app(e):
            try:
                page.window.close() # الطريقة المعتمدة لإنهاء التطبيق في الإصدارات الحديثة
            except Exception:
                pass

        bottom_navigation_bar = ft.Container(
            content=ft.SafeArea(
                ft.Row([
                    ft.ElevatedButton("التقارير", icon=ft.icons.BAR_CHART, on_click=open_reports_sheet, style=nav_btn_style, bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, expand=True),
                    ft.ElevatedButton("إغلاق", icon=ft.icons.CLOSE, on_click=close_app, style=nav_btn_style, bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, expand=True),
                    ft.ElevatedButton("الإعدادات", icon=ft.icons.SETTINGS, on_click=lambda e: page.open(settings_sheet), style=nav_btn_style, bgcolor=ft.colors.GREY_700, color=ft.colors.WHITE, expand=True),
                ], spacing=6)
            ),
            padding=10, bgcolor=ft.colors.WHITE
        )

        page.add(motivation_header, tabs, bottom_navigation_bar)

    except Exception as e:
        error_details = traceback.format_exc()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("❌ حدث خطأ برمجي:", color=ft.colors.RED_800, weight=ft.FontWeight.BOLD),
                    ft.Text(error_details, size=12, color=ft.colors.RED_900, selectable=True)
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.colors.RED_50, padding=20, border_radius=10, expand=True
            )
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
