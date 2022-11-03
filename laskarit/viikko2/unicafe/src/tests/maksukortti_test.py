import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
  def setUp(self):
    self.maksukortti = Maksukortti(1000)

  def test_luotu_kortti_on_olemassa(self):
    self.assertNotEqual(self.maksukortti, None)

  def test_kortin_saldo_alussa_on_oikein(self):
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

  def test_rahan_lataaminen_kasvattaa_saldoa_oikein_positiivinen(self):
    self.maksukortti.lataa_rahaa(2000)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 30.00 euroa")

  # kommentti: ohjelmakoodilta hiukan outo ratkaisu olla tarkistamatta, että kortille ladattava summa olisi yli nollan
  def test_rahan_lataaminen_kasvattaa_saldoa_oikein_negatiivinen(self):
    self.maksukortti.lataa_rahaa(-400)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 6.00 euroa")

  def test_saldo_pienenee_maksettaessa_saldo_riittaa(self):
    self.maksukortti.ota_rahaa(400)
    self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 6.00 euroa")
  
  def test_saldo_ei_pienene_pienella_saldolla(self):
    maksukortti = Maksukortti(300)
    maksukortti.ota_rahaa(400)
    self.assertEqual(str(maksukortti), "Kortilla on rahaa 3.00 euroa")
  
  def test_palautus_true_onnistuessa(self):
    self.assertEqual(self.maksukortti.ota_rahaa(400), True)

  def test_palautus_false_epaonnistuessa(self):
    maksukortti = Maksukortti(300)
    self.assertEqual(maksukortti.ota_rahaa(400), False)