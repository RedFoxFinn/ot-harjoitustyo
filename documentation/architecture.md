
# Arkkitehtuurikuvaus

## Rakenne

Ohjelman rakenne noudattelee kolmitasoita kerrosarkkitehtuuria.

Koodin pakkausrakenne on seuraavanlainen:

[kuva tänne]

Pakkaus _ui_ sisältää käyttöliittymänäkymistä, _services_ sovelluslogiikasta ja pysyväistallennuksesta vastaavan koodin. Lisäksi pakkaus _entities_ sisältää luokkia, jotka kuvaavat ja hyödyntävät sovelluksen käyttämien tietueiden sisältöä.

## Käyttöliittymä

Käyttöliittymä sisältää kaksi erillistä näkymää:

- sovelluksen käytössä olevien tietojen tilastotiedot   [valmis]
- uusien tuotteiden lisäys                              [valmis]

Lisäksi toteutettavat näkymät:

- sovelluksen käytössä olevien tietojen listaus         [todo]

Jokainen näkymä on toteutettu omana luokkanaan. Oletuksena sovellus avautuu tilastotietoja esittävään näkymään. Sovelluksen näkymistä näytetään kerrallaan vain yksi. Näkymien esittämisestä vastaa PantryUI-luokka. Käyttöliittymä on pyritty eristämään muusta sovelluslogiikasta omiksi yksiköikseen. Käyttöliittymäluokista kutsutaan services-hakemistoon eriytettyä DatabaseHandler-luokkaa ja sen metodeja, jotka toteuttavat tietokantatoiminnot SQLite-tietokantaan.

Käyttöliittymästä uusia tietoja lisätessä sovelluksen sisäinen tila tilastoissa ei muutu vaan se luodaan aina uudelleen, kun näkymää vaihdetaan tilastonäkymään. Tämä takaa sen, että tilasto on mahdollisimman hyvin ajantasalla. Lisäksi tuotteiden lisäyksestä vastaavassa näkymässä ei tuotteiden alatyyppien valinta ole käytettävissä eikä näkyvissä, mikäli tuotteen tyypiksi ei ole valittu "Raaka-aineet". Tämän tyypin valinnan ollessa aktiivinen, käyttöliittymästä valitaan myös alatyyppi. Tuotteen lisäyksessä tarvitaan seuraavia tietoja:

- Tuote(nimi) - tekstinä
- Tyyppi      - valinta pudotusvalikosta
- Säilyvyys   - päivän valinta kalenterista
- Lukumäärä   - lukuna
- Alatyyppi   - valinta pudotusvalikosta (vain tyypillä "Raaka-aineet")

## Sovelluslogiikka

## Tietojen pysyväistallennus

## Päätoiminnallisuudet