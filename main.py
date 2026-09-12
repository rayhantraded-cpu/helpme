import flet as ft

def main(page: ft.Page):
    page.title = "اختبار العزل"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_click(e):
        page.add(ft.Text("التفاعل يعمل بنجاح! ✅", color=ft.colors.GREEN, size=18))
        page.update()

    page.add(
        ft.Text("مرحباً أحمد! الواجهة تعمل بشكل سليم.", size=20, color=ft.colors.BLUE, weight=ft.FontWeight.BOLD),
        ft.ElevatedButton("اضغط هنا لاختبار التفاعل", on_click=on_click)
    )

if __name__ == "__main__":
    ft.app(target=main)
