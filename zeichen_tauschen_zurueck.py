tauschen = """
+ ⭐
++ ⭐⭐
+++ ⭐⭐⭐
++++ ⭐⭐⭐⭐
? ❓
A 🇦
B 🇧
C 🇨
D 🇩
E 🇪
F 🇫
G 🇬
H 🇭
I 🇮
J 🇯
K 🇰
L 🇱
M 🇲
N 🇳
O 🇴
P 🇵
Q 🇶
R 🇷
S 🇸
T 🇹
U 🇺
V 🇻
W 🇼
X 🇽
Y 🇾
Z 🇿
"""

import_filename="Kreuzungen.txt"
export_filename="Kreuzungen_zurueck.txt"
comment="#"

tauschen = tauschen.strip()
tauschen_liste = tauschen.split("\n")

for i in range(len(tauschen_liste)):
    tauschen_liste[i] = tauschen_liste[i].split(" ",1)
#tauschen_liste.append([", ",","])

tauschen_liste = sorted(tauschen_liste, key = lambda e: len(e[0]), reverse=True)

def edit_file():
    with open(import_filename, "r", encoding="utf-8-sig") as fh:
        file_content = list(fh)
    
    for i in range(len(file_content)):
        if file_content[i].strip().startswith(comment):
            continue
        for pair in tauschen_liste:
            file_content[i] = file_content[i].replace(pair[1], pair[0])
        
    with open(export_filename, "w", encoding="utf-8-sig") as fh:
        for line in file_content:
            fh.write(line)
        
if __name__ == "__main__":
    edit_file()