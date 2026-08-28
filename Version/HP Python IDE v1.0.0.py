# HP Python IDE™

# کتابخانه‌ها
import os
import sys
import tempfile
import subprocess

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class HPPythonIDE(App):
    # عنوان پنجره
    title = "HP Python IDE™"

    def build(self):
        # لایهٔ اصلی
        root = BoxLayout(
            orientation="vertical",
            spacing=5,
            padding=5
        )

        # نوار ابزار
        toolbar = BoxLayout(
            size_hint_y=0.1,
            spacing=5
        )

        # دکمهٔ اجرا
        run_button = Button(text="Run")
        run_button.bind(on_press=self.run_code)

        toolbar.add_widget(run_button)

        # ویرایشگر کد
        self.editor = TextInput(
            text='print("Hello, World!")',
            multiline=True
        )

        # بخش نمایش خروجی
        self.output = TextInput(
            readonly=True,
            multiline=True,
            size_hint_y=0.3
        )

        # افزودن بخش‌ها به پنجره
        root.add_widget(toolbar)
        root.add_widget(self.editor)
        root.add_widget(self.output)

        return root

    def run_code(self, *args):
        # دریافت کد نوشته‌شده
        code = self.editor.text

        # ساخت فایل موقت
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".py",
            mode="w",
            encoding="utf-8"
        ) as file:

            file.write(code)
            filename = file.name

        try:
            # اجرای کد با همان مفسر پایتون
            result = subprocess.run(
                [sys.executable, filename],
                capture_output=True,
                text=True
            )

            # نمایش خروجی یا خطا
            output = result.stdout + result.stderr

            if output.strip():
                self.output.text = output
            else:
                self.output.text = "Program finished successfully."

        except Exception as error:
            # نمایش خطای احتمالی
            self.output.text = str(error)

        finally:
            # حذف فایل موقت
            try:
                os.remove(filename)
            except OSError:
                pass

HPPythonIDE().run()
