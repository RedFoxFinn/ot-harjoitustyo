# Ohjelmistotekniikka

Kurssiprojektina toteutettu inventaariosovellus Pantry

## Huomio Python-versiosta

Sovelluksen toiminta on testattu Python-versiolla *3.8* ja sen toimintaa ei voida taata tätä aiemmilla versioilla.

## Dokumentaatio

[Vaatimusmäärittely](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/software_requirements_specification.md)

[Työaikakirjanpito](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/working_time.md)

[*CHANGELOG.__md__*](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/CHANGELOG.md)

[arkkitehtuuri](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/arkkitehtuuri.md)

[Käyttöohje](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/manual.md)

[Viikon 5 release](https://github.com/RedFoxFinn/ot-harjoitustyo/releases/tag/viikko5)

[Viikon 6 release](https://github.com/RedFoxFinn/ot-harjoitustyo/releases/tag/viikko6)

[Testausdokumentti](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/documentation/testing.md)

[Viikon 7 release](https://github.com/RedFoxFinn/ot-harjoitustyo/releases/tag/loppupalautus)

## Asentaminen

1. Lataa sovelluksen viimeisin versio [täältä](https://github.com/RedFoxFinn/ot-harjoitustyo/releases)

2. Pura *.zip* tai *.tar.gz*-tiedoston sisältö haluamaasi hakemistoon tietokoneellesi

3. Asenna sovelluksen riippuvuudet komennolla:

```bash
poetry install
```

4. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

### Lähdekoodin muotoilu

Lähdekoodin muotoilussa käytetään [PEP 8](https://www.python.org/dev/peps/pep-0008/) -tyyliohjeiden noudattamiseen [autopep8-kirjastoa](https://pypi.org/project/autopep8/).

Muotoilu suoritetaan komennolla:

```bash
poetry run invoke format
```

### Pylint

Tiedostossa [.pylintrc](https://github.com/RedFoxFinn/ot-harjoitustyo/blob/main/.pylintrc) määritetyt tarkistukset voidaan suorittaa komennolla:

```bash
poetry run invoke lint
```

### Ohjelmakoodin testaus

Ohjelman lähdekoodin testaus suoritetaan komennolla:

```bash
poetry run invoke test
```

### Ohjelmakoodin testikattavuus

Ohjelman lähdekoodin testikattavuuden voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti luodaan hakemistoon *htmlcov*

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:

```bash
poetry run invoke start
```