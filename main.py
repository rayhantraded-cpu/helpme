import flet as ft

def main(page: ft.Page):
    # إعدادات بسيطة للصفحة
    page.title = "المساعد الشخصي"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # رسالة ترحيبية بسيطة
    page.add(
        ft.Text("مرحباً أحمد! التطبيق يعمل بنجاح على أندرويد 🎉", size=20, color=ft.colors.GREEN)
    )

ft.app(target=main)
