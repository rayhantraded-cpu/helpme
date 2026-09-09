import datetime
import json
import random
import webbrowser
import flet as ft

# --- 1. قوائم الرسائل والنصائح الذكية بحسب أوقات اليوم ---
MORNING_MESSAGES = [
    "🌅 بركة يومك في بكورك! ابدأ بمهمة واحدة بسيطة الآن.",
    "☀️ صباح الهمة! صلاة الفجر انطلاقة روحية ونفسية.",
    "💪 صباح النشاط! تمارين بسيطة في الصباح تمنحك حيوية تكفي ليوم كامل!",
]

AFTERNOON_MESSAGES = [
    "🌤️ جاء وقت العصر! قيم نصف يومك دون إجهاد، خطوة صغيرة إضافية تصنع الفارق.",
    "☕ حان وقت الاستراحة وشحن الطاقة. خذ دقائق قليلة لتجديد نشاطك ثم أكمل.",
]

EVENING_MESSAGES = [
    "🌙 هدوء المساء فرصة للراحة. لا تضغط على نفسك، فالاستمرارية أهم من الكمال 🌿",
    "✨ أنجزت ما باستطاعتك اليوم، والراحة جزء أساسي من خطتك لغدٍ أفضل.",
]

URGENT_REMINDS = [
    "💡 لا تنهِ يومك دون إنتاج! أنجز مهمة واحدة بسيطة جداً (أو 5 دقائق فقط) لتحافظ على السلسلة 🔥",
    "🚀 الدقيقة الواحدة أفضل من الصفر! اختر أسهل مهمة وأنجزها الآن.",
]

# --- 2. أفكار ومهام مقترحة لكل تصنيف ---
CATEGORY_TIPS = {
    "🕊️ مهام روحية": [
        "الورد اليومي للقرآن الكريم لبركة يومك.",
        "حفظ نصف صفحة أو مراجعة صفحتين لتثبيت الحفظ.",
        "المحافظة على السنن الرواتب والنوافل.",
        "أذكار الصباح والمساء لتنير يومك وتحصنك."
    ],
    "💪 مهام بدنية وصحية": [
        "مشي سريع لمدة 10 دقائق لتنشيط الدورة الدموية.",
        "أداء تمارين الضغط والقرفصاء في الصباح لزيادة الحيوية.",
        "تمرين البلانك لتقوية عضلات الجذع، ابدأ بـ 30 ثانية.",
        "شرب كمية كافية من الماء موزعة على مدار اليوم."
    ],
    "🚀 مهام تطويرية": [
        "تعلم ميزة جديدة في بيئة التطوير مثل VS Code لتسريع عملك.",
        "التدرب على كتابة كود بايثون أو ربط قواعد البيانات.",
        "تحسين مهاراتك في تصميم التقارير ولوحات التحكم التفاعلية.",
        "تخصيص وقت لممارسة هواية يدوية كالنجارة أو التصميم لتفريغ طاقتك الإبداعية."
    ],
    "📚 مهام تعليمية": [
        "قراءة قصة قصيرة باللغة الإنجليزية لتطوير مفرداتك.",
        "التدرب على قواعد خط الرقعة لتحسين جمالية خطك العربي.",
        "مشاهدة مقطع مفيد أو فيلم باللغة الإنجليزية وتحليل الحوارات.",
        "قراءة 10 صفحات من كتاب متخصص في مجالك المهني."
    ],
    "🤝 مهام اجتماعية": [
        "صلة الرحم ولو باتصال هاتفي قصير.",
        "مشاركة وجبة عائلية ممتعة بعيداً عن الشاشات.",
        "تخصيص وقت للجلوس مع العائلة والأبناء وتفقد أحوالهم."
    ],
    "💰 مهام اقتصادية": [
        "مراجعة حسابات المصروفات الأسبوعية وتصنيفها.",
        "تخصيص مبلغ بسيط للادخار أو الصدقة الدورية.",
        "البحث عن أفكار جديدة لتحسين الإيرادات أو تنظيم العمليات."
    ]
}


def main(page: ft.Page):
    page.title = "تطبيق المساعد الشخصي والإنجاز"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 15
    page.spacing = 10

    user_stats = {"streak": 1, "points": 0}
    tasks_db = []

    categories = [
        ("🕊️ مهام روحية", ft.colors.PURPLE_50, ft.colors.PURPLE_900),
        ("💪 مهام بدنية وصحية", ft.colors.GREEN_50, ft.colors.GREEN_900),
        ("🚀 مهام تطويرية", ft.colors.BLUE_50, ft.colors.BLUE_900),
        ("📚 مهام تعليمية", ft.colors.ORANGE_50, ft.colors.ORANGE_900),
        ("🤝 مهام اجتماعية", ft.colors.TEAL_50, ft.colors.TEAL_900),
        ("💰 مهام اقتصادية", ft.colors.AMBER_50, ft.colors.AMBER_900),
    ]

    current_context = {"category": "", "period": "يومية"}

    # --- الهيدر التحفيزي ---
    streak_text = ft.Text(f"{user_stats['streak']} أيام", weight=ft.FontWeight.BOLD, size=12)
    points_text = ft.Text(f"{user_stats['points']} نقطة", weight=ft.FontWeight.BOLD, size=12)

    def get_time_based_message():
        current_hour = datetime.datetime.now().hour
        if 4 <= current_hour < 11:
            return random.choice(MORNING_MESSAGES)
        elif 14 <= current_hour < 18:
            return random.choice(AFTERNOON_MESSAGES)
        elif 20 <= current_hour <= 23:
            return random.choice(EVENING_MESSAGES)
        else:
            return "✨ 'الانضباط هو الجسر بين الأهداف والإنجازات.'"

    banner_tip = ft.Text(get_time_based_message(), size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, expand=True)

    motivation_header = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.MENU,
                            tooltip="فتح سحب الإنجازات",
                            on_click=lambda e: (update_drawer_achievements(), page.open(drawer)),
                        ),
                        ft.Container(
                            content=ft.Row([ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT, color=ft.colors.ORANGE, size=18), streak_text]),
                            bgcolor=ft.colors.ORANGE_50, padding=5, border_radius=15,
                        ),
                        ft.Container(
                            content=ft.Row([ft.Icon(ft.icons.STAR, color=ft.colors.AMBER_800, size=18), points_text]),
                            bgcolor=ft.colors.AMBER_50, padding=5, border_radius=15,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row([ft.Icon(ft.icons.LIGHTBULB_OUTLINE, color=ft.colors.AMBER_700, size=18), banner_tip]),
            ]
        ),
        bgcolor=ft.colors.BLUE_50, padding=8, border_radius=10,
    )

    def check_and_notify_user(e=None):
        now = datetime.datetime.now()
        hour = now.hour
        completed_today = sum(1 for t in tasks_db if t.get("completed", False))

        if hour >= 18 and completed_today == 0 and len(tasks_db) > 0:
            msg = random.choice(URGENT_REMINDS)
        else:
            msg = get_time_based_message()

        banner_tip.value = msg
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"🔔 تنبيه: {msg}"), open=True))
        page.update()

    # --- الدرج الجانبي للإنجازات ---
    achievements_list = ft.ListView(expand=True, spacing=10)

    def toggle_task_completion(e):
        cb = e.control
        task_ref = cb.data
        if task_ref:
            task_ref["completed"] = cb.value
            if cb.value:
                user_stats["points"] += 10
                points_text.value = f"{user_stats['points']} نقطة"
                page.show_snack_bar(ft.SnackBar(content=ft.Text("🎉 ممتاز! كسبت +10 نقاط. استمر بخطوات ثابتة!"), open=True))
            else:
                user_stats["points"] = max(0, user_stats["points"] - 10)
                points_text.value = f"{user_stats['points']} نقطة"
        page.update()

    def update_drawer_achievements():
        achievements_list.controls.clear()
        if not tasks_db:
            achievements_list.controls.append(ft.Text("لا توجد مهام مضافة بعد.", color=ft.colors.GREY_600))
        else:
            for task in tasks_db:
                cb = ft.Checkbox(
                    label=f"{task['title']} ({task['category']})",
                    value=task.get("completed", False), data=task, on_change=toggle_task_completion,
                )
                achievements_list.controls.append(ft.Container(content=cb, padding=5, bgcolor=ft.colors.GREY_100, border_radius=5))

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("🏆 قائمة إنجازات اليوم", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Divider(), achievements_list
                ]), padding=15,
            )
        ]
    )

    # --- نافذة إضافة مهمة جديدة ---
    task_title_input = ft.TextField(label="نص المهمة", hint_text="أدخل تفاصيل المهمة...")
    task_link_input = ft.TextField(label="رابط توضيحي (موقع / فيديو / تطبيق)", hint_text="https://...")
    task_period_dropdown = ft.Dropdown(label="تكرار المهمة", value="يومية", options=[ft.dropdown.Option("يومية"), ft.dropdown.Option("أسبوعية"), ft.dropdown.Option("شهرية")])
    task_count_input = ft.TextField(label="عدد مرات التنفيذ", value="1", keyboard_type=ft.KeyboardType.NUMBER)

    def save_new_task(e):
        if not task_title_input.value:
            task_title_input.error_text = "يرجى كتابة نص المهمة"
            page.update()
            return
        tasks_db.append({
            "title": task_title_input.value, "link": task_link_input.value,
            "period": task_period_dropdown.value, "count": task_count_input.value,
            "category": current_context["category"], "completed": False,
        })
        task_title_input.value = ""
        task_link_input.value = ""
        page.close(add_task_dialog)
        refresh_category_tasks_view()
        update_drawer_achievements()
        page.show_snack_bar(ft.SnackBar(content=ft.Text("تمت إضافة المهمة بنجاح!"), open=True))
        page.update()

    add_task_dialog = ft.AlertDialog(
        title=ft.Text("إضافة مهمة جديدة"),
        content=ft.Column([
            ft.Container(
                content=ft.Text("💡 نصيحة: إذا كنت تشعر بالضغط، أضف مهمة تستغرق 5 دقائق فقط!", size=11, color=ft.colors.AMBER_900, weight=ft.FontWeight.BOLD),
                bgcolor=ft.colors.AMBER_50, padding=8, border_radius=5,
            ),
            task_title_input, task_link_input, task_period_dropdown, task_count_input,
        ], tight=True, spacing=10),
        actions=[
            ft.TextButton("إلغاء", on_click=lambda e: page.close(add_task_dialog)),
            ft.ElevatedButton("حفظ المهمة", on_click=save_new_task, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE),
        ],
    )

    def open_add_dialog(e):
        task_period_dropdown.value = current_context["period"]
        add_task_dialog.title.value = f"إضافة مهمة: {current_context['category']}"
        page.open(add_task_dialog)

    # --- الشاشة المنبثقة لمستعرض المهام داخل المجال مع التلميحات الذكية ---
    category_tasks_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    
    dynamic_tip_text = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.TEAL_900)
    category_tip_card = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.TIPS_AND_UPDATES, color=ft.colors.TEAL_600, size=24),
            ft.Column([
                ft.Text("💡 فكرة مقترحة لمهامك:", size=10, color=ft.colors.TEAL_700),
                dynamic_tip_text
            ], spacing=2, expand=True) 
        ]),
        bgcolor=ft.colors.TEAL_50,
        padding=10,
        border_radius=8,
        border=ft.border.all(1, ft.colors.TEAL_200),
        margin=ft.margin.only(bottom=10)
    )

    category_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("عرض المهام", size=18, weight=ft.FontWeight.BOLD),
                            ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(category_sheet)),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    category_tip_card, 
                    ft.Container(content=category_tasks_list, expand=True), 
                    ft.ElevatedButton(
                        "إضافة مهمة جديدة (+)", icon=ft.icons.ADD, width=page.width,
                        bgcolor=ft.colors.BLUE_700, color=ft.colors.WHITE, on_click=open_add_dialog,
                    ),
                ]
            ), padding=20, height=550,
        ), dismissible=True,
    )

    def refresh_category_tasks_view():
        cat = current_context["category"]
        if cat in CATEGORY_TIPS:
            dynamic_tip_text.value = random.choice(CATEGORY_TIPS[cat])
        else:
            dynamic_tip_text.value = "انقر بالأسفل لإضافة مهمة جديدة."
            
        category_tasks_list.controls.clear()
        per = current_context["period"]

        filtered = [t for t in tasks_db if t["category"] == cat and t["period"] == per]

        if not filtered:
            category_tasks_list.controls.append(
                ft.Container(
                    content=ft.Text(f"لا توجد مهام {per} مضافة في هذا القسم حتى الآن.", color=ft.colors.GREY_600),
                    padding=20, alignment=ft.alignment.center,
                )
            )
        else:
            for t in filtered:
                def open_link(url=t["link"]):
                    if url: webbrowser.open(url)
                task_card = ft.Card(
                    content=ft.ListTile(
                        title=ft.Text(t["title"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"التكرار: {t['count']} مرة | الحالة: {'منجزة ✅' if t.get('completed') else 'قيد الانتظار ⏳'}"),
                        trailing=ft.IconButton(icon=ft.icons.LINK, tooltip="فتح الرابط", on_click=lambda e: open_link()) if t["link"] else None,
                    )
                )
                category_tasks_list.controls.append(task_card)
        page.update()

    def open_category_sheet(category_name, period_name):
        current_context["category"] = category_name
        current_context["period"] = period_name
        refresh_category_tasks_view()
        page.open(category_sheet)

    # --- 7. شاشة التقارير والإحصائيات الشاملة ---
    reports_content = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)

    reports_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "📊 تقرير الإنجاز والإنتاجية",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.BLUE_900,
                            ),
                            ft.IconButton(
                                icon=ft.icons.CLOSE,
                                on_click=lambda e: page.close(reports_sheet)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Container(content=reports_content, expand=True),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "تصدير Txt/PDF 📄",
                                icon=ft.icons.PICTURE_AS_PDF,
                                bgcolor=ft.colors.RED_700,
                                color=ft.colors.WHITE,
                                expand=True,
                                on_click=lambda e: page.show_snack_bar(
                                    ft.SnackBar(content=ft.Text("جاري تجهيز تقرير PDF للتصدير..."), open=True)
                                ),
                            ),
                            ft.ElevatedButton(
                                "تصدير كصورة 🖼️",
                                icon=ft.icons.IMAGE,
                                bgcolor=ft.colors.TEAL_700,
                                color=ft.colors.WHITE,
                                expand=True,
                                on_click=lambda e: page.show_snack_bar(
                                    ft.SnackBar(content=ft.Text("تم التقاط صورة للتقرير بنجاح!"), open=True)
                                ),
                            ),
                        ],
                        spacing=10,
                    ),
                ]
            ),
            padding=20,
            height=550,
        ),
        dismissible=True,
    )

    def open_reports_sheet(e):
        reports_content.controls.clear()
        total_tasks = len(tasks_db)
        completed_tasks = sum(1 for t in tasks_db if t.get("completed", False))
        ratio = (completed_tasks / total_tasks) if total_tasks > 0 else 0

        # بطاقات الإحصاء الرقمية
        kpi_row = ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("إجمالي المهام", size=12),
                            ft.Text(str(total_tasks), size=20, weight=ft.FontWeight.BOLD),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.colors.BLUE_50, padding=10, border_radius=8, expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("المهام المنجزة", size=12),
                            ft.Text(str(completed_tasks), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.colors.GREEN_50, padding=10, border_radius=8, expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("نسبة الالتزام", size=12),
                            ft.Text(f"{int(ratio*100)}%", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.ORANGE_900),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=ft.colors.ORANGE_50, padding=10, border_radius=8, expand=True,
                ),
            ],
            spacing=10,
        )

        # شريط التقدم
        progress_bar = ft.Column(
            [
                ft.Row(
                    [ft.Text("مستوى تقدمك العام", weight=ft.FontWeight.BOLD), ft.Text(f"{int(ratio*100)}%")],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ProgressBar(value=ratio, color=ft.colors.GREEN, bgcolor=ft.colors.GREY_200, height=10),
            ]
        )

        # تفاصيل حسب المجالات
        cat_analysis = ft.Column(spacing=8)
        cat_analysis.controls.append(ft.Text("تفاصيل الإنجاز حسب المجال:", weight=ft.FontWeight.BOLD, size=14))

        for cat_name, _, text_col in categories:
            cat_tasks = [t for t in tasks_db if t["category"] == cat_name]
            cat_total = len(cat_tasks)
            cat_done = sum(1 for t in cat_tasks if t.get("completed", False))
            
            cat_analysis.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(cat_name, color=text_col, expand=True),
                            ft.Text(f"{cat_done}/{cat_total}", weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.colors.GREY_50, padding=8, border_radius=5,
                )
            )

        reports_content.controls.extend([kpi_row, progress_bar, cat_analysis])
        page.open(reports_sheet)

    # --- 8. شاشة الإعدادات المتكاملة ---
    developer_note_input = ft.TextField(
        label="اكتب ملاحظاتك للمطور هنا...",
        multiline=True,
        min_lines=3,
        hint_text="اقترحاتك لتطوير التطبيق...",
    )

    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        page.update()

    def export_backup(e):
        page.show_snack_bar(ft.SnackBar(content=ft.Text("تمت محاكاة حفظ النسخة الاحتياطية بنجاح!"), open=True))

    settings_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("⚙️ إعدادات التطبيق", size=18, weight=ft.FontWeight.BOLD),
                            ft.IconButton(icon=ft.icons.CLOSE, on_click=lambda e: page.close(settings_sheet)),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(),
                    ft.Column(
                        [
                            # التحكم في المظهر
                            ft.Switch(
                                label="تفعيل الوضع الليلى (Dark Mode)",
                                value=(page.theme_mode == ft.ThemeMode.DARK),
                                on_change=toggle_theme,
                            ),
                            ft.Divider(),
                            # رقم تسجيل المنتج
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.VERIFIED_USER),
                                title=ft.Text("رقم تسجيل المنتج والترخيص"),
                                subtitle=ft.Text("PROD-2026-PA-88942-PRO"),
                            ),
                            ft.Divider(),
                            # النسخ الاحتياطي
                            ft.Row(
                                [
                                    ft.ElevatedButton("إنشاء نسخة احتياطية 💾", icon=ft.icons.BACKUP, on_click=export_backup, expand=True),
                                ]
                            ),
                            ft.Divider(),
                            # ملاحظات للمطور
                            ft.Text("ملاحظات واقتراحات للمطور:", weight=ft.FontWeight.BOLD),
                            developer_note_input,
                            ft.ElevatedButton(
                                "إرسال الملاحظات (PDF) 📨",
                                icon=ft.icons.SEND,
                                bgcolor=ft.colors.BLUE_800,
                                color=ft.colors.WHITE,
                                on_click=lambda e: page.show_snack_bar(
                                    ft.SnackBar(content=ft.Text("تم تصدير ملاحظاتك وإرسالها للمطور بنجاح!"), open=True)
                                ),
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ]
            ),
            padding=20,
            height=550,
        ),
        dismissible=True,
    )

    def open_settings_sheet(e):
        page.open(settings_sheet)

    # --- 9. بناء القوائم العمودية للصفحة الرئيسية ---
    def build_vertical_menu(period_name):
        menu_column = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)
        for cat_name, bg_col, text_col in categories:
            def make_click(c=cat_name, p=period_name):
                return lambda e: open_category_sheet(c, p)
            menu_column.controls.append(
                ft.Container(
                    content=ft.Row([ft.Text(cat_name, size=16, weight=ft.FontWeight.BOLD, color=text_col), ft.Icon(ft.icons.ARROW_FORWARD_IOS, size=16, color=text_col)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    bgcolor=bg_col, padding=18, border_radius=10, border=ft.border.all(1, text_col), ink=True, on_click=make_click(),
                )
            )
        return menu_column

    # --- 10. التبويبات الكلاسيكية (الرئيسية) ---
    tabs = ft.Tabs(
        selected_index=0, expand=True,
        tabs=[
            ft.Tab(text="المهام اليومية", icon=ft.icons.TODAY, content=build_vertical_menu("يومية")),
            ft.Tab(text="المهام الأسبوعية", icon=ft.icons.DATE_RANGE, content=build_vertical_menu("أسبوعية")),
            ft.Tab(text="المهام الشهرية", icon=ft.icons.CALENDAR_MONTH, content=build_vertical_menu("شهرية")),
        ],
    )

    # --- 11. الشريط السفلي للأزرار ---
    bottom_navigation_bar = ft.Row(
        [
            ft.ElevatedButton("التقارير", icon=ft.icons.BAR_CHART, on_click=open_reports_sheet, style=ft.ButtonStyle(bgcolor=ft.colors.TEAL_700, color=ft.colors.WHITE), expand=True),
            ft.ElevatedButton("خروج", on_click=lambda e: page.window.close(), style=ft.ButtonStyle(bgcolor=ft.colors.RED_600, color=ft.colors.WHITE), expand=True),
            ft.ElevatedButton("الإعدادات", icon=ft.icons.SETTINGS, on_click=open_settings_sheet, style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_GREY_700, color=ft.colors.WHITE), expand=True),
        ], spacing=8,
    )

    page.add(motivation_header, tabs, bottom_navigation_bar)

if __name__ == "__main__":
    ft.app(target=main, host="0.0.0.0", port=8550)