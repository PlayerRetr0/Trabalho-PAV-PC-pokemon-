import customtkinter as ctk
from api_client import api

RACAS = [
    "BULBASAUR", "IVYSAUR", "VENUSAUR", "CHARMANDER", "CHARMELEON", "CHARIZARD",
    "SQUIRTLE", "WARTORTLE", "BLASTOISE", "PIKACHU", "RAICHU", "CATERPIE",
    "METAPOD", "BUTTERFREE", "WEEDLE", "KAKUNA", "BEEDRILL", "PIDGEY",
    "PIDGEOTTO", "PIDGEOT", "RATTATA", "RATICATE", "SPEAROW", "FEAROW",
    "EKANS", "ARBOK", "SANDSHREW", "SANDSLASH", "NIDORAN_F", "NIDORINA",
    "NIDOQUEEN", "NIDORAN_M", "NIDORINO", "NIDOKING", "CLEFAIRY", "CLEFABLE",
    "VULPIX", "NINETALES", "JIGGLYPUFF", "WIGGLYTUFF", "ZUBAT", "GOLBAT",
    "ODDISH", "GLOOM", "VILEPLUME", "PARAS", "PARASECT", "VENONAT",
    "VENOMOTH", "DIGLETT", "DUGTRIO", "MEOWTH", "PERSIAN", "PSYDUCK",
    "GOLDUCK", "MANKEY", "PRIMEAPE", "GROWLITHE", "ARCANINE", "POLIWAG",
    "POLIWHIRL", "POLIWRATH", "ABRA", "KADABRA", "ALAKAZAM", "MACHOP",
    "MACHOKE", "MACHAMP", "BELLSPROUT", "WEEPINBELL", "VICTREEBEL", "TENTACOOL",
    "TENTACRUEL", "GEODUDE", "GRAVELER", "GOLEM", "PONYTA", "RAPIDASH",
    "SLOWPOKE", "SLOWBRO", "MAGNEMITE", "MAGNETON", "FARFETCHD", "DODUO",
    "DODRIO", "SEEL", "DEWGONG", "GRIMER", "MUK", "SHELLDER",
    "CLOYSTER", "GASTLY", "HAUNTER", "GENGAR", "ONIX", "DROWZEE",
    "HYPNO", "KRABBY", "KINGLER", "VOLTORB", "ELECTRODE", "EXEGGCUTE",
    "EXEGGUTOR", "CUBONE", "MAROWAK", "HITMONLEE", "HITMONCHAN", "LICKITUNG",
    "KOFFING", "WEEZING", "RHYHORN", "RHYDON", "CHANSEY", "TANGELA",
    "KANGASKHAN", "HORSEA", "SEADRA", "GOLDEEN", "SEAKING", "STARYU",
    "STARMIE", "MR_MIME", "SCYTHER", "JYNX", "ELECTABUZZ", "MAGMAR",
    "PINSIR", "TAUROS", "MAGIKARP", "GYARADOS", "LAPRAS", "DITTO",
    "EEVEE", "VAPOREON", "JOLTEON", "FLAREON", "PORYGON", "OMANYTE",
    "OMASTAR", "KABUTO", "KABUTOPS", "AERODACTYL", "SNORLAX", "ARTICUNO",
    "ZAPDOS", "MOLTRES", "DRATINI", "DRAGONAIR", "DRAGONITE", "MEWTWO", "MEW"
]

TIPOS = [
    "NORMAL", "FOGO", "AGUA", "ELETRICO", "GRAMA", "GELO",
    "LUTADOR", "VENENOSO", "TERRESTRE", "VOADOR", "PSIQUICO", "INSETO",
    "PEDRA", "FANTASMA", "DRAGAO", "SOMBRIO", "ACO", "FADA"
]

class PokemonScreen:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.window = ctk.CTkToplevel(parent_window)
        self.window.title("Pokémon")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        self.window.transient(parent_window)
        self.window.grab_set()
        self._center()
        
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Pokémon", font=ctk.CTkFont(size=48, weight="bold"))
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
    
    def editar(self, pokemon):
        self._form(pokemon)
    
    def _form(self, pokemon=None):
        form_window = ctk.CTkToplevel(self.window)
        form_window.title("Adicionar Pokémon" if not pokemon else "Editar Pokémon")
        form_window.geometry("500x600")
        form_window.resizable(False, False)
        
        form_frame = ctk.CTkScrollableFrame(form_window)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        nome_label = ctk.CTkLabel(form_frame, text="Nome (opcional):", font=ctk.CTkFont(size=16))
        nome_label.pack(anchor="w", pady=(0, 5))
        nome_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nome_entry.pack(pady=(0, 15))
        if pokemon:
            nome_entry.insert(0, pokemon.get('nome', ''))
        
        raca_label = ctk.CTkLabel(form_frame, text="Raça:", font=ctk.CTkFont(size=16))
        raca_label.pack(anchor="w", pady=(0, 5))
        raca_combo = ctk.CTkComboBox(form_frame, values=RACAS, width=400, height=40)
        raca_combo.pack(pady=(0, 15))
        if pokemon:
            raca_combo.set(pokemon.get('raca', RACAS[0]))
        else:
            raca_combo.set(RACAS[0])
        
        tipo_label = ctk.CTkLabel(form_frame, text="Tipo:", font=ctk.CTkFont(size=16))
        tipo_label.pack(anchor="w", pady=(0, 5))
        tipo_combo = ctk.CTkComboBox(form_frame, values=TIPOS, width=400, height=40)
        tipo_combo.pack(pady=(0, 15))
        if pokemon:
            tipo_combo.set(pokemon.get('tipo', TIPOS[0]))
        else:
            tipo_combo.set(TIPOS[0])
        
        genero_label = ctk.CTkLabel(form_frame, text="Gênero:", font=ctk.CTkFont(size=16))
        genero_label.pack(anchor="w", pady=(0, 5))
        genero_combo = ctk.CTkComboBox(form_frame, values=["Masculino", "Feminino"], width=400, height=40)
        genero_combo.pack(pady=(0, 15))
        if pokemon:
            genero_combo.set("Masculino" if pokemon.get('genero', True) else "Feminino")
        else:
            genero_combo.set("Masculino")
        
        level_label = ctk.CTkLabel(form_frame, text="Nível (1-100):", font=ctk.CTkFont(size=16))
        level_label.pack(anchor="w", pady=(0, 5))
        level_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        level_entry.pack(pady=(0, 15))
        if pokemon:
            level_entry.insert(0, str(pokemon.get('level', 1)))
        else:
            level_entry.insert(0, "1")
        
        caixas = api.listar_caixas()
        caixa_nomes = [f"{c.get('nome', '')} (ID: {c.get('id', '')})" for c in caixas] if caixas else []
        caixa_nomes.insert(0, "Nenhuma (sem caixa)")
        
        caixa_label = ctk.CTkLabel(form_frame, text="Caixa (opcional):", font=ctk.CTkFont(size=16))
        caixa_label.pack(anchor="w", pady=(0, 5))
        caixa_combo = ctk.CTkComboBox(form_frame, values=caixa_nomes, width=400, height=40)
        caixa_combo.pack(pady=(0, 20))
        if pokemon:
            caixa_id_atual = pokemon.get('caixa_id')
            if caixa_id_atual and caixas:
                for i, c in enumerate(caixas):
                    if c.get('id') == caixa_id_atual:
                        caixa_combo.set(caixa_nomes[i + 1])
                        break
                else:
                    caixa_combo.set(caixa_nomes[0])
            else:
                caixa_combo.set(caixa_nomes[0])
        else:
            caixa_combo.set(caixa_nomes[0])
        
        def salvar():
            nome = nome_entry.get().strip() or None
            raca = raca_combo.get()
            tipo = tipo_combo.get()
            genero = genero_combo.get() == "Masculino"
            
            try:
                level = int(level_entry.get().strip())
                if not (1 <= level <= 100):
                    self._msg("Nível deve estar entre 1 e 100!", "erro")
                    return
            except ValueError:
                self._msg("Nível deve ser um número!", "erro")
                return
            
            caixa_selecionada = caixa_combo.get()
            caixa_id_selecionada = None
            if caixa_selecionada and caixa_selecionada != "Nenhuma (sem caixa)" and caixas:
                for c in caixas:
                    if f"{c.get('nome', '')} (ID: {c.get('id', '')})" == caixa_selecionada:
                        caixa_id_selecionada = c.get('id')
                        break
            
            if pokemon:
                if api.atualizar_pokemon(pokemon['id'], raca=raca, tipo=tipo, nome=nome, genero=genero, level=level):
                    if caixa_id_selecionada is not None:
                        api.atualizar_pokemon_equipe_caixa(pokemon['id'], caixa_id=caixa_id_selecionada, equipe_id=None)
                    elif caixa_selecionada == "Nenhuma (sem caixa)":
                        caixa_id_atual = pokemon.get('caixa_id')
                        equipe_id_atual = pokemon.get('equipe_id')
                        if caixa_id_atual:
                            api.atualizar_pokemon_equipe_caixa(pokemon['id'], caixa_id=None, equipe_id=equipe_id_atual)
                    self._msg("Pokémon atualizado!", "ok")
                    form_window.destroy()
                    self.carregar()
                else:
                    self._msg("Erro ao atualizar!", "erro")
            else:
                result = api.criar_pokemon(raca, tipo, nome, genero, level)
                if result:
                    pokemon_id = result.get('id')
                    if pokemon_id and caixa_id_selecionada is not None:
                        api.atualizar_pokemon_equipe_caixa(pokemon_id, caixa_id=caixa_id_selecionada, equipe_id=None)
                    self._msg("Pokémon criado!", "ok")
                    form_window.destroy()
                    self.carregar()
                else:
                    self._msg("Erro ao criar!", "erro")
        
        btn_salvar = ctk.CTkButton(form_frame, text="Salvar", width=200, height=45, command=salvar)
        btn_salvar.pack(pady=10)
        
        btn_cancelar = ctk.CTkButton(form_frame, text="Cancelar", width=150, height=35, command=form_window.destroy)
        btn_cancelar.pack()
    
    def capturar(self, pokemon):
        capturar_window = ctk.CTkToplevel(self.window)
        capturar_window.title("Capturar Pokémon")
        capturar_window.geometry("500x300")
        capturar_window.resizable(False, False)
        
        capturar_frame = ctk.CTkFrame(capturar_window)
        capturar_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        nome_pokemon = pokemon.get('nome') or pokemon.get('raca', 'Pokémon')
        msg_label = ctk.CTkLabel(capturar_frame, text=f"Selecione a caixa para capturar\n{nome_pokemon}:", font=ctk.CTkFont(size=18))
        msg_label.pack(pady=(0, 20))
        
        caixas = api.listar_caixas()
        if not caixas:
            sem_caixa_label = ctk.CTkLabel(capturar_frame, text="Nenhuma caixa disponível!\nCrie uma caixa primeiro.", font=ctk.CTkFont(size=16))
            sem_caixa_label.pack(pady=20)
            btn_fechar = ctk.CTkButton(capturar_frame, text="Fechar", width=150, height=40, command=capturar_window.destroy)
            btn_fechar.pack(pady=20)
        else:
            caixa_nomes = [f"{c.get('nome', '')} (ID: {c.get('id', '')})" for c in caixas]
            
            caixa_label = ctk.CTkLabel(capturar_frame, text="Caixa:", font=ctk.CTkFont(size=16))
            caixa_label.pack(anchor="w", pady=(0, 5))
            caixa_combo = ctk.CTkComboBox(capturar_frame, values=caixa_nomes, width=400, height=40)
            caixa_combo.pack(pady=(0, 20))
            caixa_combo.set(caixa_nomes[0])
            
            def capturar_confirm():
                caixa_selecionada = caixa_combo.get()
                if not caixa_selecionada:
                    self._msg("Selecione uma caixa!", "erro")
                    return
                
                for c in caixas:
                    if f"{c.get('nome', '')} (ID: {c.get('id', '')})" == caixa_selecionada:
                        caixa_id = c.get('id')
                        if api.atualizar_pokemon_equipe_caixa(pokemon['id'], caixa_id=caixa_id, equipe_id=None):
                            self._msg(f"{nome_pokemon} foi capturado!", "ok")
                            capturar_window.destroy()
                            self.carregar()
                        else:
                            self._msg("Erro ao capturar!", "erro")
                        return
                
                self._msg("Caixa não encontrada!", "erro")
            
            btn_capturar = ctk.CTkButton(capturar_frame, text="Capturar", width=200, height=45, command=capturar_confirm)
            btn_capturar.pack(pady=10)
            
            btn_cancelar = ctk.CTkButton(capturar_frame, text="Cancelar", width=150, height=35, command=capturar_window.destroy)
            btn_cancelar.pack()
    
    def excluir(self, pokemon):
        confirm_window = ctk.CTkToplevel(self.window)
        confirm_window.title("Confirmar Exclusão")
        confirm_window.geometry("400x200")
        confirm_window.resizable(False, False)
        
        confirm_frame = ctk.CTkFrame(confirm_window)
        confirm_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        nome = pokemon.get('nome') or pokemon.get('raca', 'este pokémon')
        msg = ctk.CTkLabel(confirm_frame, text=f"Deseja excluir\n{nome}?", font=ctk.CTkFont(size=16))
        msg.pack(pady=20)
        
        def excluir_confirm():
            if api.deletar_pokemon(pokemon['id']):
                self._msg("Pokémon excluído!", "ok")
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
        pokemons = api.listar_pokemons()
        
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()
        
        if not pokemons:
            empty_label = ctk.CTkLabel(self.scrollable_frame, text="Nenhum pokémon cadastrado!", font=ctk.CTkFont(size=18))
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
                
                raca = pokemon.get('raca', 'Desconhecido')
                raca_label = ctk.CTkLabel(info_frame, text=f"Raça: {raca}", font=ctk.CTkFont(size=16))
                raca_label.pack(anchor="w")
                
                level = pokemon.get('level', 1)
                nivel_label = ctk.CTkLabel(info_frame, text=f"Nível: {level}", font=ctk.CTkFont(size=16))
                nivel_label.pack(anchor="w")
                
                localizacao = "Equipe" if pokemon.get('equipe_id') else ("Caixa" if pokemon.get('caixa_id') else "Sem localização")
                local_label = ctk.CTkLabel(info_frame, text=f"Localização: {localizacao}", font=ctk.CTkFont(size=14))
                local_label.pack(anchor="w")
                
                buttons_frame = ctk.CTkFrame(pokemon_frame)
                buttons_frame.pack(side="right", padx=10)
                
                caixa_id_atual = pokemon.get('caixa_id')
                equipe_id_atual = pokemon.get('equipe_id')
                
                if not caixa_id_atual and not equipe_id_atual:
                    btn_capturar = ctk.CTkButton(buttons_frame, text="Capturar", width=100, height=35, command=lambda p=pokemon: self.capturar(p))
                    btn_capturar.pack(pady=5)
                
                btn_editar = ctk.CTkButton(buttons_frame, text="Editar", width=100, height=35, command=lambda p=pokemon: self.editar(p))
                btn_editar.pack(pady=5)
                
                btn_excluir = ctk.CTkButton(buttons_frame, text="Excluir", width=100, height=35, command=lambda p=pokemon: self.excluir(p))
                btn_excluir.pack(pady=5)
                
                self.frames.append(pokemon_frame)
    
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