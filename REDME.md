# Programowanie Obiektowe
## Przeglądarka zdjęć

### Autorzy
* Michał Taszycki 243279
* Kornel Witkowski 249642

### Opis projektu
 Celem projektu było wykonanie prostej internetowej przeglądarki do zdjęć, w której użytkownik mógłby założyć własne konto z możliwością przechowywania plików na serwerze oraz dokonywać podstawowych operacji na zdjęciach. Projekt został zrealizowany w języku python z użyciem biblioteki Django.

### Funkcjonalności
* Tworzenia kont, logowanie, przechowywanie danych bazie danych na serwerze.
* Dodawanie zdjęć wraz z zapisywaniem ich na serwerze. Podział zdjęć na katalogi.
* Przeglądanie zdjęć z użyciem Viewera: zoom, obroty odbicia. 
* Wyświetlanie metadanych wybranych zdjęć.
* Sortowanie zdjęć po metadanych.

### Opis działania
Użytkownik wchodząc do aplikacji może utworzyć konto tak jak na rys 1. Rejestracja przebiega w dobrze znany sposób –  należy podać dane, dwukrotnie powtarzając wybrane hasło. Jeśli podane dane są unikalne następuje utworzenie konta w bazie danych, a użytkownik zostaje zalogowany.

![Rysunek 1](/picsshow_doc/1.jpg "Rysunek1. Rejestracja")

Zalogowany użytkownik poprzez przycisk “Upload image” na górnym pasku po może wejść w podstronę do dodawania zdjęć, która została pokazana na rysunku. 2. W pierwszej kolejności należy stworzyć bądź wybrać istniejący katalog, a następnie można załadować zdjęcia z plików dostępnych na komputerze.

![Rysunek 2](/picsshow_doc/2.jpg "Rysunek 2. Dodawanie zdjęć")

Naciskając przycisk “Catalog” zostaje wyświetlona podstrona z podglądem dodanych zdjęć, tak jak zostało to pokazane na rys. 3. W tym widoku można przeglądać zdjęcia w poszczególnych katalogach oraz je usuwać. Poprzez kliknięcie dowolnego zdjęcia zostanie  włączony viewer umożliwiające bardziej dokładne przejrzenie zdjęć.

![Rysunek 3](/picsshow_doc/3.jpg "Rysunek 3. Przeglądanie zdjęć w poszczególnych katalogach")

Działanie viewera zostało przedstawione na rys. 4. Jego włączenia umożliwia powiększanie zdjęć, obracanie, przerzucanie w poziomie i pionie, a także przełączanie pomiędzy wyświetlonymi w katalogu zdjęciami.

![Rysunek 4](/picsshow_doc/4.jpg "Rysunek 4.  Przeglądanie zdjęć w viewerze")

Na dole podstrony znajduje się tabela z metadanymi wyświetlanych zdjęć z wybranego katalogu, która została pokazana na rys. 5. Klikając na nagłówki odpowiednich kolumn w tabeli zdjęcia zostają uporządkowane względem wybranego parametru, a ponowne kliknięcie spowoduje uporządkowanie w odwrotnej kolejności. Z lewej strony można wybrać wyświetlane zdjęcia zaznaczając odpowiednie pozycje w checkboxie, a następnie używając przycisku “Show”. Z prawej strony listy można usunąć zdjęcia używając przycisk “Delete”, a także zobaczyć pełną listę metadanych używając “Details”.

![Rysunek 5](/picsshow_doc/5.jpg "Rysunek 5. Lista podstawowych metadanych o zdjęciach w wybranym katalogu")

Po użyciu przycisku “Details” zostaje wyświetlona podstrona z pełną listą metadanych wybranego zdjęcia, co zostało pokazane na rys. 6.

![Rysunek 6](/picsshow_doc/6.jpg "Rysunek 6. Wyświetlenie pełnej listy metadanych po naciśnięciu przycisku 'Details'")
