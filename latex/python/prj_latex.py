import pandas as pd

# 1. Carregar o arquivo CSV
df = pd.read_csv('prj.csv')

# 2. Agrupar por IDE, Framework, Board e Code Template, juntando os processadores
grouped = df.groupby(['IDE', 'Framework', 'Board', 'Code Template'])['Processor'].agg(
    lambda x: ', '.join(sorted(x.unique()))
).reset_index()

# 3. Reorganizar colunas e ordenar
grouped = grouped[['IDE', 'Framework', 'Board', 'Processor', 'Code Template']]
grouped = grouped.sort_values(by=['IDE', 'Framework', 'Board', 'Code Template']).reset_index(drop=True)

# 4. Construir o código LaTeX aplicando multirow nas três primeiras colunas
lines = []
lines.append(r"\documentclass{book}")
lines.append(r"\usepackage{graphicx}") 
lines.append(r"\usepackage{multirow}") 
lines.append(r"\begin{document}")
lines.append(r"\resizebox{\textwidth}{!}{%")
lines.append(r"")
lines.append(r"\begin{tabular}{|c|c|c|c|p{8cm}|}")
lines.append(r"\hline")
lines.append(r"\textbf{IDE} & \textbf{Framework} & \textbf{Board} & \textbf{Code Template} & \textbf{Processor} \\")
lines.append(r"\hline \hline")

prev_ide = None
prev_fw = None
prev_board = None

for idx, row in grouped.iterrows():
    ide = row['IDE']
    fw = row['Framework']
    board = row['Board']
    proc = row['Processor']
    temp = row['Code Template']
    
    # Tratamento de caracteres especiais para o LaTeX (ex: sublinhados)
    ide_str = ide.replace('_', r'\_')
    fw_str = fw.replace('_', r'\_')
    board_str = board.replace('_', r'\_')
    proc_str = proc.replace('_', r'\_')
    temp_str = temp.replace('_', r'\_')
    
    # Lógica para a coluna IDE
    if ide != prev_ide:
        count_ide = len(grouped[grouped['IDE'] == ide])
        ide_cell = f"\\multirow{{{count_ide}}}{{*}}{{{ide_str}}}"
        prev_ide = ide
        prev_fw = None      # Reseta o framework quando a IDE muda
        prev_board = None   # Reseta a placa quando a IDE muda
    else:
        ide_cell = ""
        
    # Lógica para a coluna Framework
    if fw != prev_fw or ide != prev_ide:
        count_fw = len(grouped[(grouped['IDE'] == ide) & (grouped['Framework'] == fw)])
        fw_cell = f"\\multirow{{{count_fw}}}{{*}}{{{fw_str}}}"
        prev_fw = fw
        prev_board = None   # Reseta a placa quando o framework muda
    else:
        fw_cell = ""
        
    # Lógica para a coluna Board
    if board != prev_board or fw != prev_fw or ide != prev_ide:
        count_board = len(grouped[(grouped['IDE'] == ide) & (grouped['Framework'] == fw) & (grouped['Board'] == board)])
        board_cell = f"\\multirow{{{count_board}}}{{*}}{{{board_str}}}"
        prev_board = board
    else:
        board_cell = ""
        
    # Adiciona a linha de dados atual
    lines.append(f"{ide_cell} & {fw_cell} & {board_cell}  & \\multirow{{1}}{{*}}{{{temp_str}}} & {proc_str}\\\\")
    
    # --- LOGICA PARA INSERÇÃO DE LINHAS (CLINE / CMIDRULE) ---
    # Verifica se a PRÓXIMA linha existe para decidir qual linha desenhar
    if idx < len(grouped) - 1:
        next_row = grouped.iloc[idx + 1]
        
        if next_row['IDE'] != ide:
            # Se a IDE vai mudar na próxima linha, desenha uma linha completa (exceto se preferir o fechamento natural)
            lines.append(r"\cline{1-5}")
        elif next_row['Framework'] != fw:
            # Se a IDE continua, mas o Framework muda: passa a linha do Framework em diante (colunas 2 a 5)
            lines.append(r"\cline{2-5}")
        elif next_row['Board'] != board:
            # Se IDE e Framework continuam, mas a Placa muda: passa a linha da Placa em diante (colunas 3 a 5)
            lines.append(r"\cline{3-5}")
        else:
            # Se apenas o Code Template mudou, passa a linha apenas nas colunas finais (4 e 5)
            lines.append(r"\cline{4-5}")


lines.append(r"\hline")
lines.append(r"\end{tabular}")
lines.append(r"")
lines.append(r"}")
lines.append(r"\end{document}")

latex_table = "\n".join(lines)
print(latex_table)

# Opcional: Salvar em arquivo .tex
with open('tabela_multi_multirow.tex', 'w', encoding='utf-8') as f:
    f.write(latex_table)