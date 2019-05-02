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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label 
from kivy.uix.button import Button
from kivy.uix.popup import Popup



global sm, playlist

playlist ='oi'

Builder.load_file('pyfy.kv')


class AddMusica(Screen):
    def add(self):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        playlist = sm.get_screen('addmusica').ids.nome_action.title
        nome = sm.get_screen('addmusica').ids.nome_musica.text
        artista = sm.get_screen('addmusica').ids.nome_artista.text
        genero = sm.get_screen('addmusica').ids.nome_genero.text
        dados = (nome, artista, genero)
        cursor.execute(f"""INSERT INTO {playlist}(nome, artista, genero)VALUES (?, ?, ?)""", dados)
        conn.commit()
        print('----------------------------------------\nMúsica inserida com sucesso!\n----------------------------------------')
    

class Play(Screen):
    global  sm, playlist
    
    

    def detalhes_play(self, instance):
        sm.get_screen('play').ids.nome_playlist.text = instance.text
        sm.current='play'

    def add_musica(self):
        nomeplaylist = sm.get_screen('play').ids.nome_playlist.text
        sm.get_screen('addmusica').ids.nome_action.title = nomeplaylist
        sm.current='addmusica'


    
   

        # sm.get_screen('play').ids.grid_play.clear_widgets()
        # sm.get_screen('play').ids.nome_playlist.text = instance.text
        # box = BoxLayout(orientation='vertical', )
        # musica = Label(text='Nome da música', color=(0,0,0,0))
        # genero = Label(text='genero', color=(0,0,0,0))
        # artista = Label(text='artista', color=(0,0,0,0))
        # box.add_widget(musica)nomeplaylinomeplaylistnomeplaylistnomeplaylistst
        # box.add_widget(artista)
        # box.add_widget(genero)
        # sm.get_screen('play').ids.grid_play.add_widget(box)


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
            bt = Button(text=i[0], on_press=play.detalhes_play)
            sm.get_screen('playlists').ids.grid.add_widget(bt)
        sm.current='playlists'


class Login(Screen):
    global  sm
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.playlists = Playlists

    def iniciarDB(self):
        self.playlists.listar_playlists()
    
class AddPlay(Screen):

    def __init__(self, **kwargs):
        super(AddPlay, self).__init__(**kwargs)
        self.playlists = Playlists

    
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
        sm.add_widget(AddMusica(name='addmusica'))
        return sm


Window.clearcolor = (1, 1, 1, 1)
PyfyApp().run()