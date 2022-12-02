
# Inventaariosovellus Pantryn käyttöohje

Pantry on sovellus talouden juomien, ruokien ja raaka-aineiden inventaarion ylläpitoon.

Sovelluksen tarkoituksena on helpottaa talouden ruokahuoltoa ja osaltaan vähentää ruokahävikkiä pitämällä tuotteiden säilyvyystiedot yhdessä paikassa.

## Näkymät

Pantryssa on kolme näkymää erilaisilla toiminnallisuuksilla: Tilastointi, Lisäys, Listaus

### Tilastointi

Näkymässä näytetään sovellukseen talletettujen tietojen tilastointia seuraavasti:

- Tuotteita
  - Talletettujen tuoterivien määrä
- Tuotteet tyypeittäin
  - jako tyyppien mukaan (Juomat, Ruoat, Raaka-aineet)
  - jokaiselle tyypille näytetään talletettujen tuotteiden kokonaismäärä (ei rivimäärää)
- Pian vanhenevat tuotteet
  - kahden (2) päivän sisällä vanhenevien tuoterivien lukumäärä
  - kahden (2) päivän sisällä vanhenevien tuotteiden kokonaismäärä
- Vanhentuneet tuotteet
  - vanhentuneiden tuoterivien lukumäärä
  - vanhentuneiden tuotteiden kokonaismäärä

Lisäksi näkymässä on painike, jolla voidaan siirtyä lisäysnäkymään sekä painike, jolla voidaan siirtyä listausnäkymään

### Lisäys

Näkymässä näytetään sovellukseen lisättävien tuotteiden lisäyslomake, jossa on seuraavat kentät:

- Tekstikenttä Tuote (tuotteen nimikkeen syöttö)
- Pudotusvalikko Tyyppi (tuotteen tyypin valinta)
- Päivävalitsin Säilyvyys (tuotteen säilyvyysajan valinta, parasta ennen / viimeinen käyttöpäivä)
- Numerokenttä Lukumäärä (tuotteiden määrän riville syöttö)
- Pudotusvalikko Alatyyppi (tuotteen alatyypin valinta, HUOM: käytössä ja esillä vain, jos tyypiksi on valittu 03 - Raaka-aineet)

Lisäksi näkymässä on painike, jolla voidaan siirtyä tilastointinäkymään sekä painike, jolla voidaan siirtyä listausnäkymään

### Listaus [kehitys kesken]

Näkymässä näytetään sovelluksen tietokantaan lisättyjen tuotteiden listauksen. Järjestys on vanhenemisjärjestyksessä ensimmäisenä vanhentuvat edellä nousevalla päiväyksellä ja toissijaisesti aakkosellisesti nousevasti.

Näkymän tuotteen nimike, lukumäärä ja päiväys korostetaan oranssilla, mikäli päiväys on enintään kahden päivän päässä nykyhetkestä ja punaisella, mikäli tuoterivi on vanhentunut.

Tuoterivien suodatukseen on painikkeet, mutta toiminnallisuus ei ole valmis vielä.

Lisäksi näkymässä on painike, jolla voidaan siirtyä tilastointinäkymään sekä painike, jolla voidaan siirtyä lisäysnäkymään

Tuotteista listausnäkymässä näytetään seuraavat tiedot:

- Nimike
- Lukumäärä
- Päiväys
- Tyyppi tai alatyyppi