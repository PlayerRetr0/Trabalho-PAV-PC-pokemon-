import customtkinter as ctk
from dados import dados
from api_client import api

class CaixaScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title("Caixa")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        self.window.transient(parent_window)
        self.window.grab_set()
        self._center()
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Caixa", font=ctk.CTkFont(size=48, weight="bold"))
        title.pack(pady=(20, 10))
        
        self.info_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=16))
        self.info_label.pack(pady=(0, 10))
        
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)
        
        btn_adicionar = ctk.CTkButton(btn_frame, text="Adicionar Caixa", width=150, height=40, command=self.adicionar)
        btn_adicionar.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(btn_frame, text="Atualizar", width=150, height=40, command=self.atualizar)
        btn_atualizar.pack(side="left", padx=5)
        
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill="both", expand=True, pady=20)
        
        self.frames = []
        self.scrollable_frame = scrollable_frame
        
        loading_label = ctk.CTkLabel(scrollable_frame, text="Carregando...", font=ctk.CTkFont(size=18))
        loading_label.pack(pady=50)
        self.frames.append(loading_label)
        
        self.window.after(50, self.atualizar)
        
        btn_voltar = ctk.CTkButton(main_frame, text="Voltar", width=200, height=50, command=self.voltar)
        btn_voltar.pack(pady=10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.voltar)
    
    def adicionar(self):
        self._form_caixa()
    
    def editar(self, caixa):
        self._form_caixa(caixa)
    
    def _form_caixa(self, caixa=None):
        form_window = ctk.CTkToplevel(self.window)
        form_window.title("Adicionar Caixa" if not caixa else "Editar Caixa")
        form_window.geometry("500x300")
        form_window.resizable(False, False)
        
        form_frame = ctk.CTkFrame(form_window)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        jogadores = api.listar_jogadores()
        jogador_nomes = [f"{j.get('nome', '')} (ID: {j.get('id', '')})" for j in jogadores] if jogadores else []
        
        nome_label = ctk.CTkLabel(form_frame, text="Nome da Caixa:", font=ctk.CTkFont(size=16))
        nome_label.pack(anchor="w", pady=(0, 5))
        nome_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nome_entry.pack(pady=(0, 15))
        if caixa:
            nome_entry.insert(0, caixa.get('nome', ''))
        
        jogador_label = ctk.CTkLabel(form_frame, text="Jogador:", font=ctk.CTkFont(size=16))
        jogador_label.pack(anchor="w", pady=(0, 5))
        jogador_combo = ctk.CTkComboBox(form_frame, values=jogador_nomes, width=400, height=40)
        jogador_combo.pack(pady=(0, 20))
        if caixa:
            jogador_id = caixa.get('jogador_id')
            if jogador_id and jogadores:
                for i, j in enumerate(jogadores):
                    if j.get('id') == jogador_id:
                        jogador_combo.set(jogador_nomes[i])
                        break
        elif jogador_nomes:
            jogador_combo.set(jogador_nomes[0])
        
        def salvar():
            nome = nome_entry.get().strip()
            if not nome:
                self._msg("Nome é obrigatório!", "erro")
                return
            
            jogador_selecionado = jogador_combo.get()
            if not jogador_selecionado or not jogadores:
                self._msg("Selecione um jogador!", "erro")
                return
            
            jogador_id = None
            for j in jogadores:
                if f"{j.get('nome', '')} (ID: {j.get('id', '')})" == jogador_selecionado:
                    jogador_id = j.get('id')
                    break
            
            if not jogador_id:
                self._msg("Jogador inválido!", "erro")
                return
            
            if caixa:
                if api.atualizar_caixa(caixa['id'], nome=nome):
                    self._msg("Caixa atualizada!", "ok")
                    form_window.destroy()
                    self.atualizar()
                else:
                    self._msg("Erro ao atualizar!", "erro")
            else:
                if api.criar_caixa(nome, jogador_id):
                    self._msg("Caixa criada!", "ok")
                    form_window.destroy()
                    self.atualizar()
                else:
                    self._msg("Erro ao criar!", "erro")
        
        btn_salvar = ctk.CTkButton(form_frame, text="Salvar", width=200, height=45, command=salvar)
        btn_salvar.pack(pady=10)
        
        btn_cancelar = ctk.CTkButton(form_frame, text="Cancelar", width=150, height=35, command=form_window.destroy)
        btn_cancelar.pack()
    
    def excluir(self, caixa):
        confirm_window = ctk.CTkToplevel(self.window)
        confirm_window.title("Confirmar Exclusão")
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        
        confirm_frame = ctk.CTkFrame(confirm_window)
        confirm_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        msg = ctk.CTkLabel(confirm_frame, text=f"Deseja excluir\n{caixa.get('nome', 'esta caixa')}?", font=ctk.CTkFont(size=16))
        msg.pack(pady=20)
        
        def excluir_confirm():
            if api.deletar_caixa(caixa['id']):
                self._msg("Caixa excluída!", "ok")
                confirm_window.destroy()
                self.atualizar()
            else:
                self._msg("Erro ao excluir!", "erro")
                confirm_window.destroy()
        
        btn_frame = ctk.CTkFrame(confirm_frame)
        btn_frame.pack(pady=10)
        
        btn_sim = ctk.CTkButton(btn_frame, text="Sim", width=120, height=40, command=excluir_confirm)
        btn_sim.pack(side="left", padx=10)
        
        btn_nao = ctk.CTkButton(btn_frame, text="Cancelar", width=120, height=40, command=confirm_window.destroy)
        btn_nao.pack(side="left", padx=10)
    
    def atualizar(self):
        try:
            dados.atualizar()
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
        
        try:
            caixas = api.listar_caixas() or []
            pokemons_todos = api.listar_pokemons() or []
            equipe_id = dados.equipe_id
            equipe_pokemons = api.buscar_pokemons_na_equipe(equipe_id) or [] if equipe_id else []
            
            total_pokemons = 0
            pokemons_por_caixa = {}
            
            if caixas and pokemons_todos:
                for caixa in caixas:
                    caixa_id = caixa.get('id')
                    if caixa_id:
                        pokemons_caixa = [p for p in pokemons_todos if p and p.get('caixa_id') == caixa_id]
                        pokemons_por_caixa[caixa_id] = pokemons_caixa
                        total_pokemons += len(pokemons_caixa)
            
            total_equipe = len(equipe_pokemons)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            caixas = []
            total_equipe = 0
            total_pokemons = 0
            pokemons_por_caixa = {}
        
        self.info_label.configure(text=f"Caixas: {len(caixas)} | Pokémons na Caixa: {total_pokemons} | Pokémons na Equipe: {total_equipe}/6")
        
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()
        
        if not caixas:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Nenhuma caixa cadastrada!", font=ctk.CTkFont(size=18))
            empty_label.pack(pady=50)
            self.frames.append(empty_label)
        else:
            for caixa in caixas:
                caixa_frame = ctk.CTkFrame(self.scrollable_frame)
                caixa_frame.pack(fill="x", pady=10, padx=10)
                
                header_frame = ctk.CTkFrame(caixa_frame)
                header_frame.pack(fill="x", padx=20, pady=10)
                
                caixa_nome = caixa.get('nome', 'Sem nome')
                caixa_label = ctk.CTkLabel(header_frame, text=f"{caixa_nome}", font=ctk.CTkFont(size=20, weight="bold"))
                caixa_label.pack(side="left")
                
                pokemons_caixa = pokemons_por_caixa.get(caixa['id'], [])
                total_label = ctk.CTkLabel(header_frame, text=f"({len(pokemons_caixa)} pokémons)", font=ctk.CTkFont(size=14))
                total_label.pack(side="left", padx=10)
                
                btn_editar = ctk.CTkButton(header_frame, text="Editar", width=80, height=30, command=lambda c=caixa: self.editar(c))
                btn_editar.pack(side="right", padx=5)
                
                btn_excluir = ctk.CTkButton(header_frame, text="Excluir", width=80, height=30, command=lambda c=caixa: self.excluir(c))
                btn_excluir.pack(side="right", padx=5)
                
                if pokemons_caixa:
                    pokemons_frame = ctk.CTkFrame(caixa_frame)
                    pokemons_frame.pack(fill="x", padx=20, pady=10)
                    
                    for pokemon in pokemons_caixa:
                        pokemon_item = ctk.CTkFrame(pokemons_frame)
                        pokemon_item.pack(fill="x", pady=5, padx=10)
                        
                        pokemon_info = ctk.CTkFrame(pokemon_item)
                        pokemon_info.pack(side="left", fill="both", expand=True, padx=15, pady=10)
                        
                        nome = pokemon.get('nome') or pokemon.get('raca', 'Sem nome')
                        nome_pokemon = ctk.CTkLabel(pokemon_info, text=nome, font=ctk.CTkFont(size=16, weight="bold"))
                        nome_pokemon.pack(anchor="w")
                        
                        raca = pokemon.get('raca', 'Desconhecido')
                        tipo = pokemon.get('tipo', 'Desconhecido')
                        level = pokemon.get('level', 1)
                        info_text = f"Raça: {raca} | Tipo: {tipo} | Nível: {level}"
                        info_pokemon = ctk.CTkLabel(pokemon_info, text=info_text, font=ctk.CTkFont(size=12))
                        info_pokemon.pack(anchor="w")
                        
                        pokemon_id = pokemon.get('id')
                        btn_mover = ctk.CTkButton(pokemon_item, text="→ Equipe", width=100, height=30, command=lambda pid=pokemon_id: self.mover_equipe(pid))
                        btn_mover.pack(side="right", padx=10)
                
                self.frames.append(caixa_frame)
    
    def mover_equipe(self, pokemon_id):
        sucesso, mensagem = dados.mover_para_equipe(pokemon_id)
        if sucesso:
            dados.atualizar()
            self.atualizar()
            self._msg(mensagem, "ok")
        else:
            self._msg(mensagem, "erro")
    
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
