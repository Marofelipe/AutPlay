from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle,Color
from time import gmtime, strftime
from kivy.core.window import Window 
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from unicodedata import normalize
from random import choice
import time
import json
import kivy
import data.lista


kivy.require('1.9.1')
palavras = data.lista.aleatorias

# GERENCIADOR DE TELAS
class Gerenciador(ScreenManager):
    pass

# TELA DE INICIO
class Inicio(Screen):
    # SORTEIA UMA PALAVRA, CHAMA A TELA DO JOGO
    def jogar(self):
        Jogo().sortear_palavra()
        self.manager.get_screen('jogo').lbl_certas = str((','.join(certas)).replace(',',' '))

# TELA DO JOGO
class Jogo(Screen):

    lbl_certas = StringProperty('')
    lbl_tentativas = StringProperty('Tentativas:')

    # Necessario para função mudar valor da label "certas".
    def __init__(self, *args, **kwargs):
        super(Jogo, self).__init__(*args, **kwargs)

    # Remover acentuação das palavras.
    def tratar_acentos(self,txt):
        return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

    # Realiza o sorteio da palavra
    def sortear_palavra(self):

        global palavra, certas, erros, sorteio, contador
        palavra = []
        certas = []
        erros = ['Erros:\n']
        contador = 1

        sorteio = choice(palavras).upper()
        escolha = self.tratar_acentos(sorteio)
        

        # Adiciona cada letra na lista palavra
        for letra in escolha:
            palavra.append(letra)

        # Para cada letra na lista palavra adiciona "_"
        for letra in range(0, len(palavra)):
            certas.append("_")

        # Inicia com a imagem da forca vazia
        self.ids.image.source = "image/1.jpg"
        # Atualiza as labels
        self.atualizar_label()

    # Letra do jogador
    def chute(self):

        chute = self.ids.txt_chute.text.upper()
        # Se a palavra possuir a letra substitui o "_"
        for letra in range(0, len(palavra)):
            if chute == palavra[letra]:
                certas[letra] = chute
        # Substituir por elif, mesmo efeito
        for letra in range(0, len(palavra)):
            if chute != palavra[letra]:
                # Se a letra não pertencer a certas
                if chute not in certas:
                    # Se não é erro repetido
                    if chute not in erros:
                        erros.append(chute)
                        self.trocar_imagem()

        self.ids.txt_chute.text = ""
        self.ids.txt_chute.focus = True
        self.atualizar_label()

    # Atualiza as Labels para saber os erros e acertos
    def atualizar_label(self):
    
        global contador
        if contador <= 7:
            self.lbl_certas = str((','.join(certas)).replace(',',' '))
            self.lbl_tentativas = str((','.join(erros)).replace(',', ' '))

            # Condição de vitória
            if "_" not in certas:
                self.ids.image.source = "image/1.jpg"
                self.lbl_certas = '[color=008000]%s[/color]'%(sorteio)
                self.lbl_tentativas = '[color=008000]Você acertou![/color]'

    # Troca a imagem do boneco
    def trocar_imagem(self):
        global contador
        if contador == 1:
            self.ids.image.source = "image/2.jpg"
        elif contador == 2:
            self.ids.image.source = "image/3.jpg"
        elif contador == 3:
            self.ids.image.source = "image/4.jpg"
        elif contador == 4:
            self.ids.image.source = "image/5.jpg"
        elif contador == 5:
            self.ids.image.source = "image/6.jpg"
        elif contador == 6:
            self.ids.image.source = "image/7.jpg"
        elif contador == 7:
            self.ids.image.source = "image/8.jpg"
            self.lbl_certas = '[color=B22222]%s[/color]'%(sorteio)
            self.lbl_tentativas = '[color=B22222]Você perdeu![/color]'
        contador += 1

    # Fecha o programa


class Time(Label):
	Horario = []
	def updateTime(self,*args):
		self.text = time.strftime("%H:%M")
	def Aviso(self,*args):
		self.text = time.strftime("%H:%M")
		with open('datas.json','r') as datas:
			self.Horario = json.load(datas)
			
		for i in range (0,len(self.Horario)):
			
			if self.text in self.Horario[i]:
				print('ok')
				Time().AvisoPop(self.Horario[i])
	def AvisoPop(self,Horario):
			PopBoX = BoxLayout(orientation='vertical')
			botoes = BoxLayout()
			pop = Popup(title=Horario,content=PopBoX,size_hint=(None,None),size=(300,180))
			sim = Button(text='Entendi',size_hint=(None,None),size=(260,50),on_release=pop.dismiss)
			atencao = Label(text='Hora da Atividade')
			botoes.add_widget(sim)
			
			PopBoX.add_widget(atencao)
			PopBoX.add_widget(botoes)

				
			pop.open()
class Atividades(Screen):
	Atividades = []
	def on_pre_enter(self):
		self.ids.box.clear_widgets()
		self.loadData()
		Window.bind(on_keyboard=self.Voltar)
		for atividade in self.Atividades:
			self.ids.box.add_widget(Atividade(text=atividade))
	def Voltar(self,window,key,*args):
		if key == 27:
			App.get_running_app().root.current = 'Menu'
			return True
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.Voltar)
	def saveData(self,*args):
		with open('datas.json','w') as data:
			json.dump(self.Atividades,data)
        
	def AddWidget(self):
		texto = self.ids.text_Atividade.text
		Hora = self.ids.Hora_Atividade.text
		self.ids.box.add_widget(Atividade(text=texto+'-'+Hora))
		self.ids.text_Atividade.text = ''
		self.ids.Hora_Atividade.text = ''
		self.Atividades.append(texto+'-'+Hora)
					
		self.saveData()
	def RemoveWdd(self,Atividade):
		texto = Atividade.ids.label.text
		self.ids.box.remove_widget(Atividade)
		self.Atividades.remove(texto)
		self.saveData()
	def loadData(self,*args):
		try:
			with open('datas.json','r') as data:
				self.Atividades = json.load(data)
	
		except FileNotFoundError:
			pass			


			
class Atividade(BoxLayout):
	def __init__(self,text='',**kwargs):
		super().__init__(**kwargs)
		self.ids.label.text = text
class Jogar(Screen):
	pass
class Menu(Screen):
	pass
class Comunicar(Screen):
	pass
class Quero(Screen):
    pass
class Nao_quero(Screen):
    pass
class Comer(Screen):
    pass
class Beber(Screen):
    pass
class jogar(Screen):
    pass
class Brincar(Screen):
    pass
class Certo(Screen):
    pass
class Errado(Screen):
    pass
class Dormir(Screen):
    pass
class Banho(Screen):
    pass
class Dentes(Screen):
    pass
class Mal(Screen):
    pass
    pass			
class SigninWindow(Screen):
    def __init__(self,**kwargs):
    	super().__init__(**kwargs)

    def validate_user(self):
    		user = self.ids.username_field	
    		pwd = self.ids.pwd_field
    		info = self.ids.info
    		button = self.ids.btn
    		uname = user.text
    		passw = pwd.text	

    		if uname == '' or passw == '':
    			info.text = '[color=#FF0000]username and/or password required'
    		else:
    			if uname == "Marcos" and passw == 'Marcos':
    				info.text = '[color=#00FF00]Logged in Successfully'
    				
    			else:
    				info.text = '[color=#FF0000]Invalid Username and/or password'
    				 	



class SigninApp(App):
    
    def loadLevel(self):
        fileName =  join(App.get_running_app().user_data_dir,'level.dat')
        try:
            with open(fileName) as fd:
                userData={}
                userData = json.load(fd)
                return userData["items"],userData["level"]
        except:
            return DEFAULT_NBITEMS , DEFAULT_SHOWTIME
        
   
    def build(self):
    	Clock.schedule_interval(Time().updateTime,1)
    	Clock.schedule_interval(Time().Aviso,10)
    	return Gerenciador()
        
            
SigninApp().run()


