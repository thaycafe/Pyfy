#coding: utf-8
import kivy
import sqlite3
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionItem   
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.popup import Popup

global sm, playlist

Builder.load_file('pyfy.kv')

class SearchBar(TextInput, ActionItem):
    def __init__(self, *args, **kwargs):
        super(SearchBar, self).__init__(*args, **kwargs)
        self.font_size = 20
        self.hint_text='Digite o nome da playlist'
        self.font_name='src/Roboto-Light.ttf'
    def search(self):
        request = self.text
        return str(request)


class Login(Screen):
    global  sm

    def iniciarDB(self):
        sm.current = 'playlists'
    
class Play(Screen):
    global  sm
    
    def teste(self, instance):
        
        
        sm.current='play'

class Playlists(Screen):
    global sm
    
    
    def __init__(self, **kwargs):
        super(Playlists, self).__init__(**kwargs)
        
        
    def listar_playlists():
        play = Play()
        sm.get_screen('playlists').ids.grid.clear_widgets()
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';''')
        for i in cursor:
            bt = Button(text=i[0], on_press=play.teste)
            sm.get_screen('playlists').ids.grid.add_widget(bt)
        sm.current='playlists'

    
    
    
class AddPlay(Screen):

    def __init__(self, **kwargs):
        super(AddPlay, self).__init__(**kwargs)
        self.playlists = Playlists

    playlists = Playlists
    def criar_play(self, playlist):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE {playlist} (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR (30) NOT NULL,
                artista VARCHAR (30) NOT NULL,
                genero VARCHAR (30) NOT NULL
        );
        """)
        print(f'Playlist {playlist} criada com sucesso.')
        self.playlists.listar_playlists()



class PyfyApp(App):
    def build(self):
        global sm
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(Login(name='login'))
        sm.add_widget(Playlists(name='playlists'))
        sm.add_widget(AddPlay(name='addplay'))
        sm.add_widget(Play(name='play'))
        return sm


Window.clearcolor = (1, 1, 1, 1)
PyfyApp().run()