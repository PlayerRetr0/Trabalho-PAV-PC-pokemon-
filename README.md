● Contexto do sistema: PC Pokemon

# Requisitos
-  O sistema deve cadastrar a raça do Pokémon, tipo e o lvl
-  O sistema so deve permitir Level entre 1 e 100
-  O sistema deve dar acesso a 5 caixas (Boxes) no sistema de armazenamento, e permitir cadastrar 30 Pokémon em cada caixa. 
-  O sistema deve permitir alterar o Level do Pokémon

Considerei que:
Um Jogador pode ter várias Caixas.
Uma Caixa possui vários Pokémon.
Uma Equipe contém vários Pokémon.

 JogadorService:

	Não permite idade ≤ 0

	Não permite nome vazio

PokemonService:

	Não permite level fora do range (1-100)

	Não permite nome com mais de 15 caracteres

	Valida enums (raça e tipo)

CaixaService:

	Não permite nome vazio

	Não permite nome com mais de 20 caracteres

	Não permite criar caixa para jogador inexistente

EquipeService:

	Não permite criar equipe para jogador inexistente

	Não permite criar segunda equipe para o mesmo jogador

	Não permite adicionar mais de 6 pokémons na equipe
