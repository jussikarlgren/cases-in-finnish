from math import log
import re
import os
import json
from nltk import word_tokenize
from nltk import sent_tokenize

from logger import logger
debug = False
error = True

stats = None

texts = [
    "Lääkintävahtimestari HYKS Neurokirurgia Lääkintävahtimestari HYKS Neurokirurgia\n\nHUS —\n\nHaemme lääkintävahtimestaria Neurokirurgian leikkaus- ja anestesiaosastolle.\n\nNeurokirurgian erikoisalalla hoidetaan keskushermoston sairauksia. Leikkaukset kohdistuvat aivoihin ja selkäytimeen. Käytössämme on viisi leikkaussalia ja toimimme jatkuvassa päivystysvalmiudessa. Vuosittainen leikkausmäärä on noin 3200, joista päivystysleikkausten osuus on n. 40%. Osastolla toimii 4 lääkintävahtimestaria. Työaikamuoto on päivätyönluontoinen jaksotyö (ma-pe).\n\nLääkintävahtimestari on tärkeä osa sujuvaa ja turvallista leikkaustoimintaa. Työhön sisältyy mm. potilaalle turvallisen leikkausasennon järjestäminen, avustaminen potilassiirroissa, röntgenkuvaus C-kaarella, lääkintälaitteiden toimivuudesta huolehtiminen sekä viallisten laitteiden testaus ja huoltoon lähettäminen. Lisäksi lääkintävahtimestari perehdyttää ja kouluttaa muuta henkilöstöä.\n\nArvostamme hyviä yhteistyötaitoja, aktiivista työotetta, kykyä toimia nopeasti 'muuttuvissa tilanteissa sekä kiinnostusta teknisiin laitteisiin.\n\nTarjoamme erikoissairaanhoidon kehittyvän työympäristön, kannustavan työyhteisön, hyvän ja yksilöllisen perehdytyksen sekä ammatillisen tuen.\n\n Hakukelpoisuus Lääkintävahtimestarin tai lähihoitajan tutkinto.\n\nKohteen aloituspäivämäärä: 2017-2-13 Ensisijainen sijainti: Helsinki-Töölön sairaala Organisaatio: 1143 Neurokirurgian linja Työsuhteen tyyppi: Vakinainen Työpaikan tyyppi: Vakio Aikataulu: Kokopäiväinen Työvuoro: 2-vuorotyö Noudatettava työ- tai virkaehtosopimus: KVTES Osastonhoitaja Arja Räsänen, puh. 050 427 0380 Ylihoitaja Ritva Salmenperä, puh. 050 427 0382\n\nTyönantajakuvaus: HUS on Suomen suurin erikoissairaanhoidon toimija ja työnantaja. Vahvuutemme on osaava ja työssään viihtyvä henkilökunta, joka arvostaa avoimuutta ja yhdenvertaisuutta. Työmme tavoitteena on korkea laatu ja korostamme potilaan parasta. Tervetuloa työkaveriksemme! Hakuaika päättyy: 2017-2-3\n\nHUS Helsinki-Töölön sairaala vakio 21.01.2017 03.02.2017 HUS\n\nHelsinki-Töölön sairaala\n\n Helsingin ja Uudenmaan Sairaanhoitopiirin kuntayhtymä 1567535-0\n\nTämä työpaikka, Lääkintävahtimestari HYKS Neurokirurgia, on ilmoitettu HUS -palvelussa 21.01.2017 ja sen on julkaissut HUS. Kyseessä on vakio työpaikka. Ilmoituksen hakuaika umpeutuu 03.02.2017. Työpaikka sijaitsee paikkakunnalla Helsinki , osoitteessa Helsinki-Töölön sairaala . Ilmoituksen jättäneellä on tällä hetkellä avoimia työpaikkoja Duunitorilla yhteensä 113 kappaletta",
    "Ben-Hur on ilmeisesti jonkinlainen amerikkalaisten Tuntematon sotilas: jokainen sukupolvi tarvitsee siitä oman versionsa. Alun perin vuonna 1880 julkaistusta romaanista on ehditty tehdä niin Broadway-näytelmää kuin kolme eri filmatisointiakin. Vuoden 2016 tulkinta on uskollisempi alkuperäisteokselle verrattuna huomattavasti tunnetumpaan antiikkispektaakkeliin vuodelta 1959, jonka Jori arvioi Gamereactorissa täyden kympin arvoiseksi .\n\nJuuda Hurinpoika eli Judah ben Hur ( Jack Huston ) on Jerusalemissa asuva juutalainen prinssi. Hänen talossaan kasvaa mieheksi myös roomalainen orpopoika Messala Severus ( Toby Kebbell ). Rooman kansalaisena Messala liittyy armeijaan, ja kohoaa vuosien varrella arvoasteikossa tribuuniksi asti. Samaan aikaan Ben-Hur pääsee kokemaan prinssinä kansansa tuskan roomalaisen miehitysvallan alla. Pasifistina hän on tiukasti väkivaltaa vastaan, mutta asemansa vuoksi hänen on hyvin vaikea pysyä puolueettomana. Messala palaa Jerusalemiin Rooman vallan edustajana, mikä asettaa kasvattiveljekset auttamatta poliittisen tilanteen eri puolille.\n\nBen-Hurin ja Messalan keskinäinen tarina liittyy keskeisesti kolmanteen henkilöhahmoon, vaikkei se käykään selväksi aivan alusta asti. Samoissa maisemissa liikkuu puuseppä Jeesus Nasaretilainen ( Rodrigo Santoro ), jonka elämä ja varsinkin kuolema tekevät lähtemättömän vaikutuksen Ben-Hurin ja Messalan suhteeseen. Elokuvan aikana Ben-Hur saa myös maailmanpolitiikan suhteen aimo annoksen realistisuutta afrikkalaiselta pohatalta nimeltä Ilderim ( Morgan Freeman ). Hänen ansiostaan leffa lopulta huipentuu tunnetuimpaan toimintakohtaukseensa eli hevosilla käytäviin väkivaltaisiin kilpa-ajoihin.\n\nBen-Hur on ilmeisesti jonkinlainen amerikkalaisten Tuntematon sotilas: jokainen sukupolvi tarvitsee siitä oman versionsa. Alun perin vuonna 1880 julkaistusta romaanista on ehditty tehdä niin Broadway-näytelmää kuin kolme eri filmatisointiakin. Vuoden 2016 tulkinta on uskollisempi alkuperäisteokselle verrattuna huomattavasti tunnetumpaan antiikkispektaakkeliin vuodelta 1959, jonka Jori arvioi Gamereactorissa täyden kympin arvoiseksi .\n\nJuuda Hurinpoika eli Judah ben Hur ( Jack Huston ) on Jerusalemissa asuva juutalainen prinssi. Hänen talossaan kasvaa mieheksi myös roomalainen orpopoika Messala Severus ( Toby Kebbell ). Rooman kansalaisena Messala liittyy armeijaan, ja kohoaa vuosien varrella arvoasteikossa tribuuniksi asti. Samaan aikaan Ben-Hur pääsee kokemaan prinssinä kansansa tuskan roomalaisen miehitysvallan alla. Pasifistina hän on tiukasti väkivaltaa vastaan, mutta asemansa vuoksi hänen on hyvin vaikea pysyä puolueettomana. Messala palaa Jerusalemiin Rooman vallan edustajana, mikä asettaa kasvattiveljekset auttamatta poliittisen tilanteen eri puolille.\n\nTämä on mainos:\n\nBen-Hurin ja Messalan keskinäinen tarina liittyy keskeisesti kolmanteen henkilöhahmoon, vaikkei se käykään selväksi aivan alusta asti. Samoissa maisemissa liikkuu puuseppä Jeesus Nasaretilainen ( Rodrigo Santoro ), jonka elämä ja varsinkin kuolema tekevät lähtemättömän vaikutuksen Ben-Hurin ja Messalan suhteeseen. Elokuvan aikana Ben-Hur saa myös maailmanpolitiikan suhteen aimo annoksen realistisuutta afrikkalaiselta pohatalta nimeltä Ilderim ( Morgan Freeman ). Hänen ansiostaan leffa lopulta huipentuu tunnetuimpaan toimintakohtaukseensa eli hevosilla käytäviin väkivaltaisiin kilpa-ajoihin.\n\nTämä on mainos:\n\nTämä on mainos:\n\nMoniin muihin elokuviin verrattuna Ben-Hurissa ei ole selvää pahista. Kyse on enemmänkin syntyperän ja ympäristön aiheuttamasta tilanteesta, jossa ihmiset asettuvat konfliktin eri puolille. Naisten rooli on kokonaisuudessa hyvin pieni. Olisi ollut huomattavan helppoa tehdä Ben-Hurista ja Messalasta nopeasti ja lopullisesti verivihollisia laittamalla heidät kilpailemaan saman naisen suosiosta, mutta onneksi moista konstia ei käytetty. Mielenkiintoinen sivuseikka on, että Ben-Hurin äitiä Naomia näyttelee Ayelet Zurer , jonka itse muistan parhaiten Man of Steel -elokuvasta Teräsmiehen äitinä.\n\nTunnettu ja aikakausien koettelema lähdemateriaali yhdessä riittävän tuotantobudjetin kanssa ovat siis taanneet ohjaaja Timur Bekmambetoville mahtavat puitteet hyvään elokuvaan. Pääasiassa hän onnistuukin tehtävässään. Lavasteet ovat mahtavia, puvustus pomppaa hyvällä tavalla silmille ruudulta ja digitaalitehosteetkin pysyttelevät yleensä taka-alalla. Ongelmiksi muodostuvat suhtautuminen toimintakohtauksien toteutukseen, loppuratkaisun laimeus ja Jeesuksen huono sovittaminen kokonaisuuteen.\n\nToiminta on yleensä kuvattu liian läheltä heiluvalla kameralla. Moinen paitsi ärsyttää, myös vie tehon kokonaan suuren mittakaavan taistelukohtauksilta. Rahanpuutteesta ei ole ollut kyse, joten ehkä ohjaajan ammattitaito ei vain riittänyt tarpeeksi näyttävän toteutuksen tekemiseen. Elokuvan loppuratkaisua on muutettu yhden erittäin keskeisen asian suhteen. Tämä laimistaa katsomiskokemuksen \"ihan ok\" -tasolle, kun sillä olisi ollut kaikki mahdollisuudet kohota suorastaan sykähdyttäviin mittasuhteisiin. Jeesuksen osuus on keskeinen tarinan kannalta, mutta raina ei onnistu liittämään sitä elokuvan keinoin osaksi kertomusta Ben-Hurista ja Messalasta. Jeesus vain ajoittain ilmestyy, tekee osuutensa ja häipyy sitten taas joksikin aikaa. Nasaretilaisen hahmoa olisi pitänyt kuljettaa selvästi paremmin mukana halki koko elokuvan.\n\nLisämateriaalit ovat pääosin onnistuneita. Perinteisen rinkikehun ohella kiinnostavaa on kuvausryhmän valmistautuminen kilpa-ajokohtaukseen. Paras pätkä on kuitenkin lyhyt katsaus, jossa Ben-Hurin tarinan synty kerrotaan aloittaen alkuperäisestä kirjailijasta itsestään 1800-luvun jälkipuoliskolla.\n\nBen-Hurin kolmas filmatisointi ei onnistu tekemään samaa vaikutusta kuin edeltäjänsä vuonna 1959. Toisaalta se ei myöskään ole kelvoton tekele, vaan ammattitaidolla toteutettu elokuva jokseenkin ikivihreästä tarinasta. Hyvä lähdemateriaali yhdessä mittavan tuotantobudjetin kanssa tekevät leffasta ehdottomasti katsomisen arvoisen."]

filterterms = None

urlpatternexpression = re.compile(r"https?://[/A-Za-z0-9\.\-\?_]+", re.IGNORECASE)
handlepattern = re.compile(r"@[A-Za-z0-9_\-±.]+", re.IGNORECASE)


def getfilelist(resourcedirectory="/home/jussi/data/1.case/fixtext", pattern=re.compile(r".*01.*")):
    filenamelist = []
    for filenamecandidate in os.listdir(resourcedirectory):
        if pattern.match(filenamecandidate):
            logger(filenamecandidate, debug)
            filenamelist.append(os.path.join(resourcedirectory,filenamecandidate))
    logger(filenamelist, debug)
    return sorted(filenamelist)


def readtexts(filename: str = None) -> list:
    filenamelist = getfilelist()
    dorawtextfiles(filenamelist)
    return texts


def dorawtextfiles(filenamelist1, loglevel=False):
    tweetantal = 0
    sentencelist = []
    filenamelist = sorted(filenamelist1)
    logger("Starting tweet file processing ", loglevel)
    logger(str(filenamelist), loglevel)
    for filename in filenamelist:
        sl = doonetextfile(filename, loglevel)
        sentencelist = sentencelist + sl
        tweetantal += len(sl)

def doonetextfile(filename, loglevel=False):
    logger(filename, loglevel)
    sentencelist = []
    with open(filename, errors="replace", encoding='utf-8') as tweetfile:
        logger("Loading " + filename, loglevel)
        try:
            data = json.load(tweetfile)
        except json.decoder.JSONDecodeError as e:
            logger("***" + filename + "\t" + str(e.msg), error)
            print(e)
            data = []
        logger("Loaded", loglevel)
        for tw in data:
            try:
                text = tw["rawText"]
                text = urlpatternexpression.sub("URL", text)
                text = handlepattern.sub("HANDLE", text)
                words = word_tokenize(text.lower())
#                if set(words).isdisjoint(filterterms):
#                    continue
                if len(words) > 1 and words[0] == "rt":
                    continue
                else:
                    sents = sent_tokenize(text)
                    for sentence in sents:
                        question = False
                        logger(sentence, debug)
                        words = word_tokenize(sentence)
                        sentencelist = sentencelist + sents
            except KeyError:
                if str(tw) != "{}":  # never mind empty strings, no cause for alarm
                    logger("**** " + str(tw) + " " + str(len(sentencelist)), error)
    return sentencelist




def readstats(filename: str = "/home/jussi/data/resources/finfreqcountwoutdigits.list") -> None:
    global stats
    stats = {}
    with open(filename) as statsfile:
        for statsline in statsfile:
            values = statsline.strip().split("\t")
            stats[values[2]] = float(values[1])

def weight(word:str) -> float:
    if word in stats:
        w = -log(stats[word])
        return w
    else:
        return 0.3



