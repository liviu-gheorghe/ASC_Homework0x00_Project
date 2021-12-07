# Proiect ASC 0x01

## Partea 0x00 

Comenzile pt executarea scripturilor de criptare si decriptare au aceeasi forma ca in enuntul proiectului:
 - python3 encrypt.py ```<parola>``` input.txt output
 - python3 decrypt.py output ```<parola>``` input_recuperat.txt
 

## Partea 0x01

- Echipa noastra este BitFlip

- Echipa adversa este [Brabetzii](https://github.com/lowLevelGod/xorEncryptDecryptASC).

- Cheia folosita de echipa adversa este ```beluga420024```.


Mai jos, vom prezenta cele doua metode prin care am aflat cheia cu care a fost criptat output-ul:


### Metoda 1 - Folosind fisierul de intrare (input.txt)

Cum echipa adversa a criptat "corect" outputul, implementarea a fost una simpla. Metoda presupune parcurgerea celor doua fisiere (input.txt si output) octet cu octet 
si aflarea caracterului cu care a fost xorat byte-ul curent din output.txt. Nu trebuie decat sa xoram
byte-ul curent din output cu byte-ul curent din input.txt si vom obtine rezultatul dorit. 
Rezultatul acestei procesari este salvat in fisierul cheie.txt. Din moment ce fisierul de input
are un numar de caractere considerabil mai mare decat lungimea cheii si nu se garanteaza faptul ca lungimea cheii divide lungimea inputului (in octeti), e clar ca in ```cheie.txt``` 
vom obtine parola concatenata cu ea insasi de un numar de ori egal cu len(input) / len (parola) + inca o "bucata din parola" in cazul in care 
len(parola) nu divide len(input).

Script-ul ```crack.py``` implementeaza procesul descris mai sus, prelucrand continutul 
din ```cheie.txt``` si afisand cea mai mica "perioada" a sirului continut. De notat este faptul ca, 
daca echipa adversa ar fi ales o parola ce este obtinuta prin concatenarea
a doua sau mai multe stringuri identice, si acel string reprezinta o parola valida (ex ```abcabcabcabc```, ```AAAAAAAAAA```).
Noi ne oprim atunci cand o gasim pe cea cu lungimea cea mai mica.

Pentru ca inital nu am stiu daca echipa a respectat cerinta de a avea o parola intre 10 si 15 caractere, 
am considerat acest aspect necunoscut. 
Pentru a rula script-ul mai eficient asfel incat sa se caute parole cu lungime >= 10, se poate 
folosi flagul ```--fpc```. 

Apelul scriptului se va face in felul urmator:

```python3 crack.py --fpc```


### Metoda 2 - Folosind doar fisierul criptat (output)

Explicatia pentru aceasta metoda va fi una intuitiva, bazata pe modul in care conceptul de 
"frequency analysis" a fost inteles, si nu va implica vreo demonstratie matematica.

Aceasta metoda este mai complicata decat prima, si presupune folosirea unei tehnici statistice de spargere a criptarilor slabe, numita analiza frecventei.  
Pe scurt, analiza frecventei reprezinta obtinerea de informatii referitoare la cat de des apare 
un anumit caracter intr-un text. De exemplu, cunoastem faptul 
ca primele 12 cele mai folosite caractere in limba engleza sunt, in aceasta ordine, ```ETAOINSHRLDU```. Analog, se estimeaza ca in limba romana primele 
12 cele mai folosite caractere sunt "EIARTNOCSLUM". Asta inseamna ca, daca avem de a face cu un 
text in limba romana, e mult mai probabil ca, la fiecare pas, sa dam de un ```E``` decat de un ```Z```. 
Practic, in tot textul vor fi mai multi ```E``` si ```A``` decat ```Z``` sau ```X```. 



Ideea este ca pentru fiecare "caracter" (sau byte) din output care a fost criptat cu acelasi 
caracter din cheie (deci vom obtine grupuri de forma (```1, k+1, 2k+1,...```), (```2, k+2, 2k+2...```))
sa incercam toate posibilitatile pentru caracterul curent din cheie (in cazul nostru ar fi toate literele mici, mari si toate numerele - insa pentru orice eventualitate am decis sa testam toate caracterele de la 0 la 127).

Daca rezultatul xorarii caracterului curent din output cu alegerea facuta pentru caracterul curent din cheie
duce la obtinerea unui caracter extrem de folosit (care se afla printre primele 12), inseamna ca sunt sanse 
mai mari ca acela sa fie caracterul folosit. Daca am fi obtinut ceva precum un simbol ciudat / caracter non-printabil, ar fi fost mai 
putin probabil ca acel caracter sa faca parte din cheie. Practic, vom parcurge fiecare 
grup de caractere din output care au fost xorate cu acelasi caracter din parola, iar pentru 
fiecare din acestea verificam toate posibilitatile pt caracterul curent din cheie. Pt fiecare 
dintre "candidati", vom retine un scor care ne va spune cat de probabil e ca el sa fie 
caracterul cu adeverat folosit. Daca ```candidatul_curent_pt_grupul_t ^ reprezentatul_curent_al_grupului_t``` se afla printre 
cele mai comune caractere, ii incrementam scorul (unde t ia valori de la 1 la lunigmea parolei). La final, il alegem pe cel mai bun pentru 
fiecare dintre grupuri. 

Pentru a face acest lucru, insa, am avea nevoie de lungimea parolei, pentru a altfel nu am sti 
cum sa grupam caracterele din output. Deci, inainte de a incerca efectiv sa facem 
analiza de frecventa pe textul criptat, trebuie sa "ghicim" cumva lungimea parolei. Stim ca in principiu ar 
trebui sa fie intre 10 si 15 caractere, insa nu ne ajuta foarte mult - cu cat lungimea este 
mai "incerta", cu atat grupurile noastre de caractere s-ar amesteca si mai mult, iar procedeul de 
analiza a frecventei ar deveni din ce in ce mai ineficient. Algoritmul o sa creada ca 
doua caractere din output s-au xorat cu un acelasi caracter din parola, cand de fapt nu e asa. 


Cum aflam lungimea parolei? 

Vom itera prin toate lungimile posibile ale cheii (in cazul nostru ar trebui sa fie intre 10 si 15) si calculam 
distanta Hamming dintre doua blocuri consecutive de lungime k_curent, unde k_curent este 
alegerea curenta pentru lungimea cheii. Distanta Hamming dintre doua blocuri consecutive din output
va fi numarul de biti diferiti situati pe aceeasi pozitie. 

De exemplu daca in output am avea secventa "```ABCXFG```" si k_curent = 3, 
atunci distanta Hamming dintre cele doua blocuri adiacente ("ABC" si "XFG") ar fi egala cu 5:
```
010000010100001001000011  XOR
010110000100011001000111
========================
000110010000010000000100   = 0x190404

```

Lungimea cu cel mai bun scor Hamming castiga - scorul Hamming este obtinut prin normalizarea distantei pt fiecare pereche de grupuri si mai apoi calcularea mediei aritmetice a acestor valori.



Apelul scriptului se va face in felul urmator:

```python3 crack_woi.py```


## Resurse

- https://en.wikipedia.org/wiki/XOR_cipher
- https://en.wikipedia.org/wiki/Frequency_analysis
- https://crypto.stackexchange.com/a/8848
- https://crypto.stackexchange.com/a/8118
- https://carterbancroft.com/breaking-repeating-key-xor-theory/
- https://carterbancroft.com/breaking-repeating-key-xor-programmatically/

