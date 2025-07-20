# 🏰 Medieval Quest

**Medieval Quest** é um jogo de plataforma 2D desenvolvido com **Pygame Zero**, onde o jogador controla um herói em uma jornada para resgatar uma princesa, enfrentando inimigos e superando desafios.

## 🎮 Como Jogar

- Use as **setas esquerda/direita** para se mover.
- Pressione **barra de espaço** para pular.
- Resgate a princesa para vencer.
- Cuidado com os inimigos: colidir com eles resulta em derrota!

## 📜 Conceitos Utilizados

### 🔁 Game Loop
O jogo utiliza o loop principal do Pygame Zero com duas funções essenciais:
- `update()`: atualiza a lógica do jogo a cada frame.
- `draw()`: desenha todos os elementos na tela.

### 🧍 Personagens e Animações
- **Herói**: possui animações para idle e caminhada, com movimentação suave e detecção de colisão.
- **Inimigos**: patrulham uma área fixa, com animações de caminhada.
- **Princesa**: animação idle contínua e detecção de resgate.

### 🧠 Lógica de Física
- Simulação de gravidade e pulo com `vy` (velocidade vertical).
- Detecção de chão ajustada com base na altura do sprite.

### 🎨 Sistema de Câmera
- A câmera acompanha o herói suavemente, com limites para não ultrapassar as bordas do mundo.

### 🧱 Parallax Scrolling
- O fundo das montanhas se move mais devagar que o chão, criando profundidade visual (parallax).

### 🔊 Música e Sons
- Música de fundo e efeitos sonoros ativáveis/desativáveis.
- Sons específicos para pulo, colisão com inimigos e resgate da princesa.

### 🖱️ Menu Inicial
- Tela com botões clicáveis: Iniciar, Som On/Off e Sair.

### 🔁 Reinício do Jogo
- Após ganhar ou perder, um botão "RESTART" aparece na tela para recomeçar.

### 🕹️ Estados do Jogo
- `MENU`: Tela inicial.
- `PLAYING`: Jogo ativo.
- `EXIT`: Fecha o jogo.

### 🧪 Modo Debug
- Quando ativado, exibe as hitboxes circulares dos personagens.

## 🧩 Requisitos

- Python 3
- [Pygame Zero](https://pygame-zero.readthedocs.io/en/stable/)
- Pygame

Para instalar:
```bash
pip install pgzero pygame
```

## 🚀 Executando o Jogo

Salve o arquivo como `game.py` e execute com:

```bash
pgzrun game.py
```
