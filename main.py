import sqlite3

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


# ==================================================
# DATABASE
# ==================================================

class Database:

    def __init__(self):
        self.conn = sqlite3.connect("whatsapp_lite.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contact TEXT NOT NULL,
                sender TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)

        self.conn.commit()

    def save_message(self, contact, sender, message):

        self.cursor.execute(
            """
            INSERT INTO messages
            (contact, sender, message)
            VALUES (?, ?, ?)
            """,
            (contact, sender, message)
        )

        self.conn.commit()

    def get_messages(self, contact):

        self.cursor.execute(
            """
            SELECT sender, message
            FROM messages
            WHERE contact = ?
            ORDER BY id
            """,
            (contact,)
        )

        return self.cursor.fetchall()


database = Database()


# ==================================================
# LOGIN
# ==================================================

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=15
        )

        title = Label(
            text="💬 WhatsApp Lite",
            font_size=32
        )

        layout.add_widget(title)

        layout.add_widget(
            Label(
                text="🔐 Login",
                font_size=25
            )
        )

        self.username = TextInput(
            hint_text="Username",
            multiline=False,
            font_size=20
        )

        self.password = TextInput(
            hint_text="Password",
            multiline=False,
            password=True,
            font_size=20
        )

        layout.add_widget(self.username)
        layout.add_widget(self.password)

        login = Button(
            text="LOGIN",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        login.bind(on_press=self.login)

        layout.add_widget(login)

        self.status = Label(
            text="",
            font_size=18
        )

        layout.add_widget(self.status)

        self.add_widget(layout)

    def login(self, instance):

        username = self.username.text.strip()

        if username == "":
            self.status.text = "⚠️ Username likho"
            return

        self.manager.current = "home"


# ==================================================
# HOME
# ==================================================

class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        layout.add_widget(
            Label(
                text="🏠 WhatsApp Lite",
                font_size=30
            )
        )

        chats = Button(
            text="💬 Chats",
            font_size=22
        )

        contacts = Button(
            text="👥 Contacts",
            font_size=22
        )

        settings = Button(
            text="⚙️ Settings",
            font_size=22
        )

        logout = Button(
            text="🚪 Logout",
            font_size=22
        )

        chats.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "contacts")
        )

        contacts.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "contacts")
        )

        settings.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "settings")
        )

        logout.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "login")
        )

        layout.add_widget(chats)
        layout.add_widget(contacts)
        layout.add_widget(settings)
        layout.add_widget(logout)

        self.add_widget(layout)


# ==================================================
# CONTACTS
# ==================================================

class ContactsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.contacts = [
            "Rahul",
            "Mohan",
            "Sita",
            "Aman",
            "Akash"
        ]

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        header = BoxLayout(
            size_hint_y=None,
            height=60
        )

        back = Button(
            text="←",
            size_hint_x=0.2,
            font_size=25
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        header.add_widget(back)

        header.add_widget(
            Label(
                text="👥 Contacts",
                font_size=26
            )
        )

        layout.add_widget(header)

        self.search = TextInput(
            hint_text="🔎 Contact search...",
            multiline=False,
            font_size=18,
            size_hint_y=None,
            height=55
        )

        self.search.bind(
            text=self.search_contact
        )

        layout.add_widget(self.search)

        self.list_box = BoxLayout(
            orientation="vertical",
            spacing=8
        )

        layout.add_widget(self.list_box)

        self.add_widget(layout)

        self.show_contacts(self.contacts)

    def show_contacts(self, names):

        self.list_box.clear_widgets()

        for name in names:

            button = Button(
                text="👤 " + name,
                font_size=20,
                size_hint_y=None,
                height=65
            )

            button.bind(
                on_press=lambda x, n=name:
                self.open_chat(n)
            )

            self.list_box.add_widget(button)

    def search_contact(self, instance, text):

        text = text.lower().strip()

        result = [
            name for name in self.contacts
            if text in name.lower()
        ]

        self.show_contacts(result)

    def open_chat(self, name):

        chat = self.manager.get_screen("chat")

        chat.current_contact = name

        chat.load_chat()

        self.manager.current = "chat"


# ==================================================
# CHAT
# ==================================================

class ChatScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_contact = ""

        layout = BoxLayout(
            orientation="vertical"
        )

        # HEADER

        header = BoxLayout(
            size_hint_y=None,
            height=65
        )

        back = Button(
            text="←",
            size_hint_x=0.15,
            font_size=25
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "contacts")
        )

        header.add_widget(back)

        title_box = BoxLayout(
            orientation="vertical"
        )

        self.title = Label(
            text="💬 Chat",
            font_size=23
        )

        self.online = Label(
            text="🟢 Online",
            font_size=14
        )

        title_box.add_widget(self.title)
        title_box.add_widget(self.online)

        header.add_widget(title_box)

        layout.add_widget(header)

        # MESSAGES

        self.messages = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=8
        )

        layout.add_widget(self.messages)

        # BOTTOM BAR

        bottom = BoxLayout(
            size_hint_y=None,
            height=60,
            spacing=5
        )

        self.input_box = TextInput(
            hint_text="Message likho...",
            multiline=False,
            font_size=18
        )

        voice = Button(
            text="🎤",
            size_hint_x=0.18,
            font_size=22
        )

        send = Button(
            text="➤",
            size_hint_x=0.20,
            font_size=25
        )

        voice.bind(
            on_press=self.voice_message
        )

        send.bind(
            on_press=self.send_message
        )

        bottom.add_widget(self.input_box)
        bottom.add_widget(voice)
        bottom.add_widget(send)

        layout.add_widget(bottom)

        self.add_widget(layout)

    def load_chat(self):

        self.title.text = "💬 " + self.current_contact

        self.messages.clear_widgets()

        history = database.get_messages(
            self.current_contact
        )

        if not history:

            self.add_message(
                self.current_contact,
                "Hello 👋"
            )

        else:

            for sender, message in history:

                self.add_message(
                    sender,
                    message
                )

    def add_message(self, sender, message):

        label = Label(
            text=sender + ": " + message,
            font_size=18,
            size_hint_y=None,
            height=45
        )

        self.messages.add_widget(label)

    def send_message(self, instance):

        message = self.input_box.text.strip()

        if message == "":
            return

        database.save_message(
            self.current_contact,
            "You",
            message
        )

        self.add_message(
            "You",
            message
        )

        self.input_box.text = ""

    def voice_message(self, instance):

        self.add_message(
            "You",
            "🎤 Voice Message Sent!"
        )


# ==================================================
# SETTINGS
# ==================================================

class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        layout.add_widget(
            Label(
                text="⚙️ Settings",
                font_size=30
            )
        )

        self.info = Label(
            text=(
                "💾 SQLite Database\n\n"
                "👥 Contacts\n\n"
                "🔎 Contact Search\n\n"
                "💬 Chat System\n\n"
                "🎤 Voice Message UI\n\n"
                "🔐 Login Demo"
            ),
            font_size=20
        )

        layout.add_widget(self.info)

        dark = Button(
            text="🌙 Dark Mode",
            font_size=20,
            size_hint_y=None,
            height=60
        )

        back = Button(
            text="← Back",
            font_size=20,
            size_hint_y=None,
            height=60
        )

        dark.bind(
            on_press=self.dark_mode
        )

        back.bind(
            on_press=lambda x:
            setattr(self.manager, "current", "home")
        )

        layout.add_widget(dark)
        layout.add_widget(back)

        self.add_widget(layout)

    def dark_mode(self, instance):

        instance.text = "🌙 Dark Mode ON"

        self.info.text += (
            "\n\n🌙 Dark Mode Demo Enabled"
        )


# ==================================================
# APP
# ==================================================

class WhatsAppLite(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(
            LoginScreen(name="login")
        )

        sm.add_widget(
            HomeScreen(name="home")
        )

        sm.add_widget(
            ContactsScreen(name="contacts")
        )

        sm.add_widget(
            ChatScreen(name="chat")
        )

        sm.add_widget(
            SettingsScreen(name="settings")
        )

        sm.current = "login"

        return sm


# ==================================================
# START APP
# ==================================================

WhatsAppLite().run()