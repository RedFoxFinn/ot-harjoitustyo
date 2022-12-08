# Pantry - changelog

## viikko 3

- sovelluksen taustatoiminnoista tietokannan käsittely luotu:
  - uuden kannan luominen, olemassaolevan yhdistäminen
  - tyyppien (Types) ja alatyyppien (Subtypes) luonti, haku ja laskeminen
  - tuotteiden luominen, hakeminen, laskeminen, vähentäminen ja poistaminen
  - testit yllämainituille
  - alustava UI tuotteiden lisäämiseen

## viikko 4

- sovelluksen lähdekoodin tyylin tarkistus pylint-paketin avulla
- sovelluksen lähdekoodin automaattinen muotoilu autopep8-paketin avulla
- korjattu muotoilu- ja tyylivirheet
- korjattu testit
- tuotteen lisäyksen UI-toiminnallisuus valmis ja sovitettu DatabaseHandleriin
- tuotteen lisäyksen tyypin ja alatyypin valinnan korjaus UI:n taustatoiminnoissa tietokantaan lisäyksen yhteydessä
- tuotetyypin mukaan hakeminen tuotelukua haettaessa + testien päivitys
- alustava pohja tilastoille (UI)
- lisätty mahdollisuus siirtyä tilasto- ja lisäysnäkymien välillä
- muutettu hakemiston alihakemisto database -> services
- korjattu testeistä tietokantatiedoston polku

## viikko 5

- DatabaseHandlerissa lisätty ominaisuus lisätä riville lukumäärään, mikäli lisättävän tuotteen tiedot vastaavat jo kannassa olevaa riviä
- päivitetty testit
- tilastojen esittämiseen lisätty toiminnallisuus vanhenevien ja vanhentuneiden tuotteiden määrän ja rivimäärän näyttämiseksi
  - stats ja DatabaseHandler
- stats.py UI:n muotoiluja siistitty
- aloitettu käyttöohjeiden kirjoittaminen manual.md -tiedostoon
- lisätty toiminnallisuus vaihtaa näkymää listaukseen lisäyksestä ja tilastoinnista
- lisätty listausnäkymä ilman listaustoimintoa
- lisätty listausnäkymään painikkeet suodatusta varten, suodatustoiminnallisuus ei valmistunut vielä
- lisätty listausnäkymään toiminnallisuus näyttää kaikki talletetut tuotteet
  - tuotteen nimi, lukumäärä ja päiväys korostuu punaisella, mikäli vanhentunut ja oranssilla, mikäli päiväys on lähempänä kuin kaksi päivää
- muokattu DatabaseHandlerin get_products palauttamaan kyselyn tuotteet nousevasti päiväyksen mukaan ja toissijaisesti aakkosellisesti nousevasti

## viikko 6

- pantry.py & list_products.py lisätty toiminnallisuus päivittää listanäkymä tietokannan sisällön muuttuessa (tuoterivin poisto / lukumäärän muutos)
- list_products lisätty toiminnallisuus lisätä tai vähentää tuotteiden määrää rivillä
- list_products lisätty toiminnallisuus poistaa tuoterivi
- muokattu listausnäkymän sarakeleveyksiä
- lisätty docstring-dokumentaatio coodiin google-formaatilla