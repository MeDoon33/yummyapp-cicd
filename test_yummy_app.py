import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# Cap do 1: Bo test co ban cho san
class TestEasyLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# Cap do 2: Kiem thu khuyen mai
class TestMediumLevel(unittest.TestCase):
    def test_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "GIAM10"), 90000.0)

    def test_promo_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_special_valid_os_15(self):
        app = YummyApp(network_status="online", os_version=15)
        self.assertAlmostEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000.0)

    def test_promo_special_invalid_os_14_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_promo_invalid_code_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=15)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "INVALID_CODE")


# Cap do 2: Kiem thu Mocking phan cung GPS
class TestHardLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_in_zone(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        )

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_out_of_zone(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError()
        self.assertEqual(self.app.get_nearby_restaurants(), "Khong the xac dinh vi tri.")


if __name__ == '__main__':
    unittest.main()