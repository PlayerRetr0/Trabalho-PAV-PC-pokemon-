import customtkinter as ctk
from dados import dados
from api_client import api

class EquipeScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title("Equipe")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        self.window.transient(parent_window)
        self.window.grab_set()
        self._center()
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(pady=(0, 20))
        
        title = ctk.CTkLabel(title_frame, text="Equipe", font=ctk.CTkFont(size=48, weight="bold"))
        title.pack(side="left", padx=10)
        
        self.contador = ctk.CTkLabel(title_frame, text="(0/6)", font=ctk.CTkFont(size=24))
        self.contador.pack(side="left", padx=10)
        
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)
        
        btn_criar = ctk.CTkButton(btn_frame, text="Criar Equipe", width=150, height=40, command=self.criar)
        btn_criar.pack(side="left", padx=5)
        
        btn_atualizar = ctk.CTkButton(btn_frame, text="Atualizar", width=150, height=40, command=self.atualizar)
        btn_atualizar.pack(side="left", padx=5)
        
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill="both", expand=True, pady=20)
        
        self.frames = []
        self.scrollable_frame = scrollable_frame
        
        loading_label = ctk.CTkLabel(scrollable_frame, text="Carregando...", font=ctk.CTkFont(size=18))
        loading_label.pack(pady=50)
        self.frames.append(loading_label)
        
        self.window.after(10, self.atualizar)
        
        btn_voltar = ctk.CTkButton(main_frame, text="Voltar", width=200, height=50, command=self.voltar)
        btn_voltar.pack(side="right", padx=10, pady=10)
        
        self.window.protocol("WM_DELETE_WINDOW", self.voltar)
    
    def criar(self):
        jogadores = api.listar_jogadores()
        if not jogadores:
            self._msg("Nenhum jogador cadastrado! Crie um jogador primeiro.", "erro")
            return
        
        criar_window = ctk.CTkToplevel(self.window)
        criar_window.title("Criar Equipe")
        criar_window.geometry("500x300")
        criar_window.resizable(False, False)
        
        criar_frame = ctk.CTkFrame(criar_window)
        criar_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        msg_label = ctk.CTkLabel(criar_frame, text="Selecione o jogador para criar a equipe:", font=ctk.CTkFont(size=18))
        msg_label.pack(pady=(0, 20))
        
        jogador_nomes = [f"{j.get('nome', '')} (ID: {j.get('id', '')})" for j in jogadores]
        
        jogador_label = ctk.CTkLabel(criar_frame, text="Jogador:", font=ctk.CTkFont(size=16))
        jogador_label.pack(anchor="w", pady=(0, 5))
        jogador_combo = ctk.CTkComboBox(criar_frame, values=jogador_nomes, width=400, height=40)
        jogador_combo.pack(pady=(0, 20))
        jogador_combo.set(jogador_nomes[0])
        
        def criar_confirm():
            jogador_selecionado = jogador_combo.get()
            if not jogador_selecionado:
                self._msg("Selecione um jogador!", "erro")
                return
            
            for j in jogadores:
                if f"{j.get('nome', '')} (ID: {j.get('id', '')})" == jogador_selecionado:
                    jogador_id = j.get('id')
                    if api.criar_equipe(jogador_id):
                        self._msg("Equipe criada!", "ok")
                        criar_window.destroy()
                        dados.atualizar()
                        self.atualizar()
                    else:
                        self._msg("Erro ao criar equipe! O jogador já pode ter uma equipe.", "erro")
                    return
            
            self._msg("Jogador não encontrado!", "erro")
        
        btn_criar = ctk.CTkButton(criar_frame, text="Criar Equipe", width=200, height=45, command=criar_confirm)
        btn_criar.pack(pady=10)
        
        btn_cancelar = ctk.CTkButton(criar_frame, text="Cancelar", width=150, height=35, command=criar_window.destroy)
        btn_cancelar.pack()
    
    def atualizar(self):
        try:
            dados.atualizar()
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")
        
        try:
            pokemons = api.buscar_pokemons_na_equipe(dados.equipe_id) or [] if dados.equipe_id else []
        except Exception as e:
            print(f"Erro ao buscar pokémons: {e}")
            pokemons = []
        
        self.contador.configure(text=f"({len(pokemons)}/6)")
        
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()
        
        if not pokemons:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Sua equipe está vazia!\nVá até a Caixa para adicionar pokémons.", font=ctk.CTkFont(size=18))
            empty_label.pack(pady=50)
            self.frames.append(empty_label)
        else:
            for pokemon in pokemons:
                pokemon_frame = ctk.CTkFrame(self.scrollable_frame)
                pokemon_frame.pack(fill="x", pady=10, padx=10)
                
                info_frame = ctk.CTkFrame(pokemon_frame)
                info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
                
                nome = pokemon.get('nome') or pokemon.get('raca', 'Sem nome')
                nome_label = ctk.CTkLabel(info_frame, text=nome, font=ctk.CTkFont(size=24, weight="bold"))
                nome_label.pack(anchor="w")
                
                tipo = pokemon.get('tipo', 'Desconhecido')
                tipo_label = ctk.CTkLabel(info_frame, text=f"Tipo: {tipo}", font=ctk.CTkFont(size=16))
                tipo_label.pack(anchor="w")
                
                level = pokemon.get('level', 1)
                nivel_label = ctk.CTkLabel(info_frame, text=f"Nível: {level}", font=ctk.CTkFont(size=16))
                nivel_label.pack(anchor="w")
                
                pokemon_id = pokemon.get('id')
                buttons_frame = ctk.CTkFrame(pokemon_frame)
                buttons_frame.pack(side="right", padx=10)
                
                btn_enviar = ctk.CTkButton(buttons_frame, text="Enviar para Caixa", width=140, height=40, command=lambda pid=pokemon_id: self.enviar_caixa(pid))
                btn_enviar.pack(pady=5)
                
                self.frames.append(pokemon_frame)
    
    def enviar_caixa(self, pokemon_id):
        caixas = api.listar_caixas()
        if not caixas:
            self._msg("Nenhuma caixa disponível! Crie uma caixa primeiro.", "erro")
            return
        
        pokemon = api.buscar_pokemon(pokemon_id)
        if not pokemon:
            self._msg("Pokémon não encontrado!", "erro")
            return
        
        if len(caixas) == 1:
            caixa_id = caixas[0].get('id')
            sucesso, mensagem = api.mover_pokemon_para_caixa(pokemon_id, caixa_id)
            if sucesso:
                dados.atualizar()
                self.atualizar()
                self._msg(mensagem, "ok")
            else:
                self._msg(mensagem, "erro")
        else:
            self._selecionar_caixa(pokemon_id, pokemon, caixas)
    
    def _selecionar_caixa(self, pokemon_id, pokemon, caixas):
        selecao_window = ctk.CTkToplevel(self.window)
        selecao_window.title("Enviar para Caixa")
        selecao_window.geometry("500x300")
        selecao_window.resizable(False, False)
        
        selecao_frame = ctk.CTkFrame(selecao_window)
        selecao_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        nome_pokemon = pokemon.get('nome') or pokemon.get('raca', 'Pokémon')
        msg_label = ctk.CTkLabel(selecao_frame, text=f"Selecione a caixa para enviar\n{nome_pokemon}:", font=ctk.CTkFont(size=18))
        msg_label.pack(pady=(0, 20))
        
        caixa_nomes = [f"{c.get('nome', '')} (ID: {c.get('id', '')})" for c in caixas]
        
        caixa_label = ctk.CTkLabel(selecao_frame, text="Caixa:", font=ctk.CTkFont(size=16))
        caixa_label.pack(anchor="w", pady=(0, 5))
        caixa_combo = ctk.CTkComboBox(selecao_frame, values=caixa_nomes, width=400, height=40)
        caixa_combo.pack(pady=(0, 20))
        caixa_combo.set(caixa_nomes[0])
        
        def enviar():
            caixa_selecionada = caixa_combo.get()
            if not caixa_selecionada:
                self._msg("Selecione uma caixa!", "erro")
                return
            
            for c in caixas:
                if f"{c.get('nome', '')} (ID: {c.get('id', '')})" == caixa_selecionada:
                    caixa_id = c.get('id')
                    sucesso, mensagem = api.mover_pokemon_para_caixa(pokemon_id, caixa_id)
                    if sucesso:
                        dados.atualizar()
                        self._msg(mensagem, "ok")
                        selecao_window.destroy()
                        self.atualizar()
                    else:
                        self._msg(mensagem, "erro")
                    return
            
            self._msg("Caixa não encontrada!", "erro")
        
        btn_enviar = ctk.CTkButton(selecao_frame, text="Enviar", width=200, height=45, command=enviar)
        btn_enviar.pack(pady=10)
        
        btn_cancelar = ctk.CTkButton(selecao_frame, text="Cancelar", width=150, height=35, command=selecao_window.destroy)
        btn_cancelar.pack()
    
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
