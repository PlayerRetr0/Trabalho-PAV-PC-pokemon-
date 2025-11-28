import customtkinter as ctk
from pokemon import PokemonScreen
from caixa import CaixaScreen
from jogador import JogadorScreen
from equipe import EquipeScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Seu PC Pokémon")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        self._center()
        
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="PC Pokémon", font=ctk.CTkFont(size=48, weight="bold"))
        title.pack(pady=(20, 40))
        
        subtitle = ctk.CTkLabel(main_frame, text="Escolha uma opção:", font=ctk.CTkFont(size=18))
        subtitle.pack(pady=(0, 30))
        
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(pady=20)
        
        btn_pokemon = ctk.CTkButton(buttons_frame, text="Pokémon", font=ctk.CTkFont(size=24, weight="bold"), width=300, height=80, command=self.open_pokemon)
        btn_pokemon.pack(pady=15)
        
        btn_caixa = ctk.CTkButton(buttons_frame, text="Caixa", font=ctk.CTkFont(size=24, weight="bold"), width=300, height=80, command=self.open_caixa)
        btn_caixa.pack(pady=15)
        
        btn_jogador = ctk.CTkButton(buttons_frame, text="Jogador", font=ctk.CTkFont(size=24, weight="bold"), width=300, height=80, command=self.open_jogador)
        btn_jogador.pack(pady=15)
        
        btn_equipe = ctk.CTkButton(buttons_frame, text="Equipe", font=ctk.CTkFont(size=24, weight="bold"), width=300, height=80, command=self.open_equipe)
        btn_equipe.pack(pady=15)
    
    def _center(self):
        self.root.update()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def open_pokemon(self):
        self.root.withdraw()
        PokemonScreen(self.root)
    
    def open_caixa(self):
        self.root.withdraw()
        CaixaScreen(self.root)
    
    def open_jogador(self):
        self.root.withdraw()
        JogadorScreen(self.root)
    
    def open_equipe(self):
        self.root.withdraw()
        EquipeScreen(self.root)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
