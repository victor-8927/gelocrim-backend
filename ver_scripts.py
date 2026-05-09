path = r'C:\fleet-cloud\gelocrim_v1.html'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print('=== LINHAS 2143-2152 ===')
for i in range(2142, min(2152, len(lines))):
    print(f'{i+1}: {lines[i].rstrip()[:120]}')

content = ''.join(lines)
import re
# Posição de todos os <script>
scripts_pos = [m.start() for m in re.finditer(r'<script', content)]
print(f'\nTotal blocos <script>: {len(scripts_pos)}')

# Posição da função
func_pos = [m.start() for m in re.finditer('function abrirImportacaoBaseClientes', content)]
print(f'Função encontrada em: {func_pos}')

# Posição do </body>
body_pos = [m.start() for m in re.finditer(r'</body>', content)]
print(f'</body> em: {body_pos}')
