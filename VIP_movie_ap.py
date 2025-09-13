# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.utils import platform
from kivy.core.text import LabelBase
import webbrowser
import os

# 设置窗口大小
Window.size = (600, 400)


# 注册中文字体
def register_chinese_font():
    try:
        # Windows系统字体路径
        if platform == 'win':
            font_path = 'C:/Windows/Fonts/simhei.ttf'  # 黑体
            if os.path.exists(font_path):
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
            else:
                # 尝试其他中文字体
                font_path = 'C:/Windows/Fonts/msyh.ttc'  # 微软雅黑
                if os.path.exists(font_path):
                    LabelBase.register(name='ChineseFont', fn_regular=font_path)

        # Android系统 - 使用默认字体
        elif platform == 'android':
            LabelBase.register(name='ChineseFont', fn_regular='DroidSansFallback.ttf')

        # 其他系统（Linux/Mac）
        else:
            # 尝试常见中文字体
            common_fonts = [
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Linux
                '/Library/Fonts/PingFang.ttc'  # Mac
            ]
            for font in common_fonts:
                if os.path.exists(font):
                    LabelBase.register(name='ChineseFont', fn_regular=font)
                    break
            else:
                LabelBase.register(name='ChineseFont', fn_regular='Arial')
    except Exception as e:
        print(f"字体注册失败: {e}")
        # 失败时不中断程序，使用默认字体


# 注册中文字体
register_chinese_font()


class VIPVideoApp(App):
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 顶部按钮布局
        button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        # 平台按钮
        btn_iqiyi = Button(text='爱奇艺', font_name='ChineseFont')
        btn_iqiyi.bind(on_press=self.open_iqiyi)
        button_layout.add_widget(btn_iqiyi)

        btn_tx = Button(text='腾讯视频', font_name='ChineseFont')
        btn_tx.bind(on_press=self.open_tx)
        button_layout.add_widget(btn_tx)

        btn_youku = Button(text='优酷视频', font_name='ChineseFont')
        btn_youku.bind(on_press=self.open_youku)
        button_layout.add_widget(btn_youku)

        main_layout.add_widget(button_layout)

        # 输入区域
        input_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        lbl_url = Label(text='视频网址:', size_hint=(0.3, 1), font_name='ChineseFont')
        input_layout.add_widget(lbl_url)

        self.entry_url = TextInput(multiline=False, size_hint=(0.7, 1), font_name='ChineseFont')
        input_layout.add_widget(self.entry_url)

        main_layout.add_widget(input_layout)

        # 操作按钮区域
        action_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        btn_clear = Button(text='清空', font_name='ChineseFont')
        btn_clear.bind(on_press=self.clear_input)
        action_layout.add_widget(btn_clear)

        btn_play = Button(text='播放', background_color=(0.5, 0.8, 1, 1), font_name='ChineseFont')
        btn_play.bind(on_press=self.play_video)
        action_layout.add_widget(btn_play)

        main_layout.add_widget(action_layout)

        # 警告标签
        warning_label = Label(
            text='小心使用',
            color=(1, 0, 0, 1),  # 红色
            size_hint=(1, 0.1),
            font_size=16,
            font_name='ChineseFont'
        )
        main_layout.add_widget(warning_label)

        return main_layout

    def open_iqiyi(self, instance):
        self.open_url("https://www.iqiyi.com")

    def open_tx(self, instance):
        self.open_url("https://v.qq.com")

    def open_youku(self, instance):
        self.open_url("https://www.youku.com")

    def clear_input(self, instance):
        self.entry_url.text = ''

    def play_video(self, instance):
        video_url = self.entry_url.text.strip()  # 去除首尾空格
        if video_url:
            # 自动补充协议头（如果没有）
            if not video_url.startswith(('http://', 'https://')):
                video_url = f'https://{video_url}'
            parsed_url = f"https://jx.xmflv.cc/?url={video_url}"
            self.open_url(parsed_url)
        else:
            self.show_popup("提示", "请输入视频网址")

    def open_url(self, url):
        """统一使用webbrowser在所有平台打开链接"""
        try:
            # 尝试打开链接
            webbrowser.open(url)
        except Exception as e:
            # 针对不同平台显示更具体的错误信息
            if platform == 'android':
                self.show_popup("错误", "无法打开链接，请确保已安装浏览器")
            else:
                self.show_popup("错误", f"无法打开链接: {str(e)}")

    def show_popup(self, title, message):
        """显示弹出消息"""
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        message_label = Label(text=message, font_name='ChineseFont')
        popup_layout.add_widget(message_label)

        close_button = Button(text='关闭', size_hint=(1, 0.4), font_name='ChineseFont')
        popup_layout.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.8, 0.4)
        )

        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    VIPVideoApp().run()