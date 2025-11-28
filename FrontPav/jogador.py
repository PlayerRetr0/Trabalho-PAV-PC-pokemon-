import customtkinter as ctk
from api_client import api

class JogadorScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title("Jogador")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        self.window.transient(parent_window)
        self.window.grab_set()
        self._center()
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Jogador", font=ctk.CTkFont(size=48, weight="bold"))
        title.pack(pady=(20, 10))
        
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)
        
        btn_adicionar = ctk.CTkButton(btn_frame, text="Adicionar", width=150, height=40, command=self.adicionar)
        btn_adicionar.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(btn_frame, text="Atualizar", width=150, height=40, command=self.carregar)
        btn_atualizar.pack(side="left", padx=5)
        
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill="both", expand=True, pady=20)
        
        self.frames = []
        self.scrollable_frame = scrollable_frame
        
        loading_label = ctk.CTkLabel(scrollable_frame, text="Carregando...", font=ctk.CTkFont(size=18))
        loading_label.pack(pady=50)
        self.frames.append(loading_label)
        
        self.window.after(10, self.carregar)
        
        btn_voltar = ctk.CTkButton(main_frame, text="Voltar", width=200, height=50, command=self.voltar)
        btn_voltar.pack(pady=10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.voltar)
    
    def adicionar(self):
        self._form()
    
    def editar(self, jogador):
        self._form(jogador)
    
    def _form(self, jogador=None):
        form_window = ctk.CTkToplevel(self.window)
        form_window.title("Adicionar Jogador" if not jogador else "Editar Jogador")
        form_window.geometry("500x300")
        form_window.resizable(False, False)
        
        form_frame = ctk.CTkFrame(form_window)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        nome_label = ctk.CTkLabel(form_frame, text="Nome:", font=ctk.CTkFont(size=16))
        nome_label.pack(anchor="w", pady=(0, 5))
        nome_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nome_entry.pack(pady=(0, 15))
        if jogador:
            nome_entry.insert(0, jogador.get('nome', ''))
        
        idade_label = ctk.CTkLabel(form_frame, text="Idade:", font=ctk.CTkFont(size=16))
        idade_label.pack(anchor="w", pady=(0, 5))
        idade_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        idade_entry.pack(pady=(0, 20))
        if jogador:
            idade_entry.insert(0, str(jogador.get('idade', '')))
        
        def salvar():
            nome = nome_entry.get().strip()
            try:
                idade = int(idade_entry.get().strip())
            except ValueError:
                self._msg("Idade deve ser um número!", "erro")
                return
            
            if not nome:
                self._msg("Nome é obrigatório!", "erro")
                return
            
            if jogador:
                if api.atualizar_jogador(jogador['id'], nome=nome, idade=idade):
                    self._msg("Jogador atualizado!", "ok")
                    form_window.destroy()
                    self.carregar()
                else:
                    self._msg("Erro ao atualizar!", "erro")
            else:
                if api.criar_jogador(nome, idade):
                    self._msg("Jogador criado!", "ok")
                    form_window.destroy()
                    self.carregar()
                else:
                    self._msg("Erro ao criar!", "erro")
        
        btn_salvar = ctk.CTkButton(form_frame, text="Salvar", width=200, height=45, command=salvar)
        btn_salvar.pack(pady=10)
        
        btn_cancelar = ctk.CTkButton(form_frame, text="Cancelar", width=150, height=35, command=form_window.destroy)
        btn_cancelar.pack()
    
    def excluir(self, jogador):
        confirm_window = ctk.CTkToplevel(self.window)
        confirm_window.title("Confirmar Exclusão")
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        
        confirm_frame = ctk.CTkFrame(confirm_window)
        confirm_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        msg = ctk.CTkLabel(confirm_frame, text=f"Deseja excluir\n{jogador.get('nome', 'este jogador')}?", font=ctk.CTkFont(size=16))
        msg.pack(pady=20)
        
        def excluir_confirm():
            if api.deletar_jogador(jogador['id']):
                self._msg("Jogador excluído!", "ok")
                confirm_window.destroy()
                self.carregar()
            else:
                self._msg("Erro ao excluir!", "erro")
                confirm_window.destroy()
        
        btn_frame = ctk.CTkFrame(confirm_frame)
        btn_frame.pack(pady=10)
        
        btn_sim = ctk.CTkButton(btn_frame, text="Sim", width=120, height=40, command=excluir_confirm)
        btn_sim.pack(side="left", padx=10)
        
        btn_nao = ctk.CTkButton(btn_frame, text="Cancelar", width=120, height=40, command=confirm_window.destroy)
        btn_nao.pack(side="left", padx=10)
    
    def carregar(self):
        jogadores = api.listar_jogadores()
        
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()
        
        if not jogadores:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Nenhum jogador cadastrado!", font=ctk.CTkFont(size=18))
            empty_label.pack(pady=50)
            self.frames.append(empty_label)
        else:
            for jogador in jogadores:
                jogador_frame = ctk.CTkFrame(self.scrollable_frame)
                jogador_frame.pack(fill="x", pady=10, padx=10)
                
                info_frame = ctk.CTkFrame(jogador_frame)
                info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
                
                nome = jogador.get('nome', 'Sem nome')
                nome_label = ctk.CTkLabel(info_frame, text=nome, font=ctk.CTkFont(size=24, weight="bold"))
                nome_label.pack(anchor="w")
                
                idade = jogador.get('idade', 'N/A')
                idade_label = ctk.CTkLabel(info_frame, text=f"Idade: {idade}", font=ctk.CTkFont(size=16))
                idade_label.pack(anchor="w")
                
                total_caixas = jogador.get('total_caixas', 0)
                caixas_label = ctk.CTkLabel(info_frame, text=f"Caixas: {total_caixas}", font=ctk.CTkFont(size=16))
                caixas_label.pack(anchor="w")
                
                tem_equipe = jogador.get('tem_equipe', False)
                equipe_label = ctk.CTkLabel(info_frame, text=f"Tem Equipe: {'Sim' if tem_equipe else 'Não'}", font=ctk.CTkFont(size=16))
                equipe_label.pack(anchor="w")
                
                buttons_frame = ctk.CTkFrame(jogador_frame)
                buttons_frame.pack(side="right", padx=10)
                
                btn_editar = ctk.CTkButton(buttons_frame, text="Editar", width=100, height=35, command=lambda j=jogador: self.editar(j))
                btn_editar.pack(pady=5)
                
                btn_excluir = ctk.CTkButton(buttons_frame, text="Excluir", width=100, height=35, command=lambda j=jogador: self.excluir(j))
                btn_excluir.pack(pady=5)
                
                self.frames.append(jogador_frame)
    
    def _msg(self, texto, tipo):
        msg_label = ctk.CTkLabel(self.window, text=texto, font=ctk.CTkFont(size=14))
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        self.window.after(2000, msg_label.destroy)
    
    def _center(self):
        self.window.update()
        width = 900
        height = 700
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def voltar(self):
        self.window.destroy()
        self.parent_window.deiconify()
