# Widgets antigos
from tkinter.ttk import Combobox, Progressbar, Separator

# Botões
from tkinter import Button

# Widgets
from tkinter import Label, Entry, Frame, Spinbox, LabelFrame

# Outros
from tkinter import Menu, PhotoImage

# Caixas de menssagem
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno

from tkinter.filedialog import askopenfilename


class Construtor:
    """
    Serve para criar de forma mais prática
    :return:
    """

    @classmethod
    def __posiciona(cls, nw_widget, kwargs, widget):
        if kwargs[widget].get('place', False):
            nw_widget.place(**kwargs[widget]['place'])
        elif kwargs[widget].get('grid', False):
            nw_widget.grid(**kwargs[widget]['grid'])
        elif kwargs[widget].get('pack', False):
            if not kwargs[widget]['pack']:
                nw_widget.pack()
            else:
                nw_widget.pack(**kwargs[widget]['pack'])

    @classmethod
    def label(cls, kwargs=None):
        for label in kwargs:
            nw_widget = Label(**kwargs[label]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=label)

    @classmethod
    def entry(cls, kwargs=None):
        for entry in kwargs:
            nw_widget = Entry(**kwargs[entry]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=entry)

    @classmethod
    def combobox(cls, kwargs=None):
        for combo_box in kwargs:
            nw_widget = Combobox(**kwargs[combo_box]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=combo_box)

    @classmethod
    def button(cls, kwargs=None):
        for botao in kwargs:
            nw_widget = Button(**kwargs[botao]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=botao)

    @classmethod
    def frame(cls, kwargs=None):
        for frame in kwargs:
            nw_widget = Frame(**kwargs[frame]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=frame)

    @classmethod
    def spinbox(cls, kwargs=None):
        for spinbox in kwargs:
            nw_widget = Spinbox(**kwargs[spinbox]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=spinbox)

    @classmethod
    def labelframe(cls, kwargs=None):
        for labelframe in kwargs:
            nw_widget = LabelFrame(**kwargs[labelframe]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=labelframe)

    @classmethod
    def progressbar(cls, kwargs=None):
        for progressbar in kwargs:
            nw_widget = Progressbar(**kwargs[progressbar]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=progressbar)

    @classmethod
    def separator(cls, kwargs=None):
        for separator in kwargs:
            nw_widget = Separator(**kwargs[separator]['param'])
            cls.__posiciona(nw_widget=nw_widget, kwargs=kwargs, widget=separator)

    @classmethod
    def abrir_arquivo(cls, titulo='Abrir', extenssoes=None, options=None):
        return askopenfilename(title=titulo, filetypes=extenssoes, options=options)

    @classmethod
    def menu(cls, **kwargs):
        Menu(master=None, title='None', name='none', tearoff=0)

    @classmethod
    def show_info(cls, titulo='info', mensagem=None):
        showinfo(title=titulo, message=mensagem)
