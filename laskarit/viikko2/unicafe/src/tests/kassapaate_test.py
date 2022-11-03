import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
  def setUp(self):
    self.kassapaate = Kassapaate()
    self.maksukortti = Maksukortti(1000)
  
  def test_luotu_kassapaate_on_olemassa(self):
    self.assertNotEqual(self.kassapaate, None)
  
  def test_kassapaatteen_rahat_alussa_on_oikein(self):
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
  
  def test_kassapaatteella_ei_ole_alussa_myyty_edullisia(self):
    self.assertEqual(self.kassapaate.edulliset, 0)
  
  def test_kassapaatteella_ei_ole_alussa_myyty_maukkaita(self):
    self.assertEqual(self.kassapaate.maukkaat, 0)

  def test_edullisen_kateisosto_tasaraha(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(240), 0)
    self.assertEqual(self.kassapaate.edulliset, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
  
  def test_edullisen_kateisosto_vaihtoraha(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
    self.assertEqual(self.kassapaate.edulliset, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
  
  def test_edullisen_kateisosto_pieni_maksu(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
    self.assertEqual(self.kassapaate.edulliset, 0)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

  def test_maukkaan_kateisosto_tasaraha(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(400), 0)
    self.assertEqual(self.kassapaate.maukkaat, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
  
  def test_maukkaan_kateisosto_vaihtoraha(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)
    self.assertEqual(self.kassapaate.maukkaat, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
  
  def test_maukkaan_kateisosto_pieni_maksu(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
    self.assertEqual(self.kassapaate.maukkaat, 0)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
  
  def test_edullisen_korttiosto_saldo_riittaa(self):
    self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
    self.assertEqual(self.kassapaate.edulliset, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    self.assertEqual(self.maksukortti.saldo, 760)

  def test_edullisen_korttiosto_saldo_ei_riita(self):
    maksukortti = Maksukortti(200)
    self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(maksukortti), False)
    self.assertEqual(self.kassapaate.edulliset, 0)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    self.assertEqual(maksukortti.saldo, 200)

  def test_maukkaan_korttiosto_saldo_riittaa(self):
    self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
    self.assertEqual(self.kassapaate.maukkaat, 1)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    self.assertEqual(self.maksukortti.saldo, 600)
  
  def test_maukkaan_korttiosto_saldo_ei_riita(self):
    maksukortti = Maksukortti(300)
    self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(maksukortti), False)
    self.assertEqual(self.kassapaate.maukkaat, 0)
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
    self.assertEqual(maksukortti.saldo, 300)

  def test_saldon_lataaminen_kortille_onnistuu_positiivinen(self):
    self.assertEqual(self.maksukortti.saldo, 1000)
    self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 1000)
    self.assertEqual(self.maksukortti.saldo, 2000)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 20.00 euroa")
    self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)
  
  def test_saldon_lataaminen_kortille_onnistuu_nolla(self):
    self.assertEqual(self.maksukortti.saldo, 1000)
    self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 0)
    self.assertEqual(self.maksukortti.saldo, 1000)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

  def test_saldon_lataaminen_kortille_onnistuu_positiivinen(self):
    self.assertEqual(self.maksukortti.saldo, 1000)
    self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -1000)
    self.assertEqual(self.maksukortti.saldo, 1000)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)