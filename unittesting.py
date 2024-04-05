import unittest
from unittest.mock import MagicMock
from controller import controller
from client import client

class TestControllerMethods(unittest.TestCase):
    def setUp(self):
        self.controller = controller.Controller()
        self.controller.connections = {('192.168.0.1', 1234), ('192.168.0.2', 5678), ('192.168.0.3', 9012)}  # setting fake connections
        self.controller.command_dict = {}  # setting an empty command dictionary initially

    def test_setup_gui(self):
        self.assertIsNotNone(self.controller.root)

    def test_add_widgets(self):
        """
        Test all widgets are present
        :return:
        """
        self.assertIsNotNone(self.controller.title)
        self.assertIsNotNone(self.controller.connected_label)
        self.assertIsNotNone(self.controller.refresh_button)
        self.assertIsNotNone(self.controller.edit_label)
        self.assertIsNotNone(self.controller.view_option)
        self.assertIsNotNone(self.controller.view_option)
        self.assertIsNotNone(self.controller.clear_button)
        self.assertIsNotNone(self.controller.connected_list)
        self.assertIsNotNone(self.controller.connection_output)
        self.assertIsNotNone(self.controller.checkvar)
        self.assertIsNotNone(self.controller.allow_multi)
        self.assertIsNotNone(self.controller.send_button)
        self.assertIsNotNone(self.controller.main_output)

    def test_defult_command_options(self):
        """
        Test command option widgets are present
        :return:
        """
        self.assertIsNotNone(self.controller.check_netinfo_val)
        self.assertIsNotNone(self.controller.check_netinfo)
        self.assertIsNotNone(self.controller.check_processor_val)
        self.assertIsNotNone(self.controller.check_processor)
        self.assertIsNotNone(self.controller.check_usrs_val)
        self.assertIsNotNone(self.controller.check_usrs)
        self.assertIsNotNone(self.controller.check_sudoers_val)
        self.assertIsNotNone(self.controller.check_sudoers)
        self.assertIsNotNone(self.controller.check_proc_val)
        self.assertIsNotNone(self.controller.check_proc)

    def test_on_close(self):
        """"
        Checks that on close runs and it does destroy root
        """

        self.controller.root.destroy = MagicMock()  # mocking the destroy method of the root window
        self.controller.root.quit = MagicMock()
        self.controller.on_close() # attempts destroy

        self.controller.root.destroy.assert_called_once()  # checking destroy method of the root window was called
        self.controller.root.quit.assert_called_once()  # checking quit method of the root window was called

    def test_update_connections(self):
        """
        Testing if update functions are called
        :return:
        """

        # mocking the update_connected_list and update_dropdown_options methods
        self.controller.update_connected_list = MagicMock()
        self.controller.update_dropdown_options = MagicMock()

        # calling the method
        self.controller.update_connections()

        # checking that both update_connected_list and update_dropdown_options were called
        self.controller.update_connected_list.assert_called_once()
        self.controller.update_dropdown_options.assert_called_once()

    def test_update_connected_list(self):
        """
        Testing updating connection list correct number of times
        :return:
        """
        # mocking method
        self.controller.connected_list.insert = MagicMock()

        # calling the method under test
        self.controller.update_connected_list()

        # checking that connected_list.insert was called for each connection
        self.assertEqual(self.controller.connected_list.insert.call_count, len(self.controller.connections))

        #checking that connected_list was cleared and is empty
        self.assertIsNone(self.controller.connected_list.get())

    def test_update_dropdown_options(self):

        # mocking methods
        self.controller.view_option = MagicMock()

        # calling method
        self.controller.update_dropdown_options()

        # checking that ip_options is updated correctly
        ip_options_list = self.controller.ip_options
        ip_options_list.sort()
        self.assertEqual(ip_options_list, ['192.168.0.1', '192.168.0.2', '192.168.0.3'])

        # testing that view_option.configure and view_option.set was called once each
        self.controller.view_option.configure.assert_called_once_with(
            values=['192.168.0.1', '192.168.0.2', '192.168.0.3'])

    def test_main_screen_output(self):
        output_message = "Testing string"
        expected_insert_call = MagicMock()

        # mocking configure and see methods of main_output
        self.controller.main_output.configure = MagicMock()
        self.controller.main_output.see = MagicMock()
        self.controller.main_output = MagicMock()

        # calling the method under test
        self.controller.main_screen_output(output_message)

        # testing the insert method of main_output was called with the correct arguments
        self.controller.main_output.insert.assert_called_once_with("end", "Testing string\n")

        # testing the configure method of main_output was called twice and see method once
        self.assertEqual(self.controller.main_output.configure.call_count, 2)
        self.controller.main_output.see.assert_called_once_with("end")


class TestClientMethods(unittest.TestCase):
    def setUp(self):
        self.client = client.Client("192.168.0.33", 12345)

    def test_setup_gui(self):
        """
        Test if GUI setup initializes correctly
        """
        self.assertIsNotNone(self.client.root)

    def test_add_widgets(self):
        """
        Test if widgets are added successfully
        """

        self.assertIsNotNone(self.client.title)
        self.assertIsNotNone(self.client.indicator)
        self.assertIsNotNone(self.client.textbox)
        self.assertIsNotNone(self.client.settings_button)

    def test_check_valid_ip(self):
        """
        Test if IP validation works correctly
        """

        # ip address so should be true
        self.assertTrue(self.client.check_valid_ip("192.168.0.1"))
        # not an ip address so should be false
        self.assertFalse(self.client.check_valid_ip("not_an_ip"))

    def test_check_valid_port(self):
        """
        Test if port validation works correctly
        """

        self.assertTrue(self.client.check_valid_port(4444)) # valid port
        self.assertFalse(self.client.check_valid_port(0)) # not valid port
        self.assertFalse(self.client.check_valid_port(65536)) # not valid port

    def test_screen_output(self):
        """
        Test if screen output works correctly
        """
        # Assuming the method works as expected
        pass

    def test_screen_output(self):
        output_message = "Testing string"
        expected_insert_call = MagicMock()

        # mocking configure and see methods of main_output
        self.client.textbox.configure = MagicMock()
        self.client.textbox.see = MagicMock()
        self.client.textbox = MagicMock()

        # calling the method under test
        self.client.screen_output(output_message)

        # testing the insert method of main_output was called with the correct arguments
        self.client.textbox.insert.assert_called_with("end", "Testing string\n")

        # testing if the configure see method once
        self.client.textbox.see.assert_called_with("end")

    def test_connect_status(self):
        """
        Test if connect status updates correctly
        """
        self.client.connect_status(True)
        self.assertEqual(self.client.indicator.cget("text"), "Connected")
        self.assertEqual(self.client.indicator.cget("text_color"), "green")

        self.client.connect_status(False)
        self.assertEqual(self.client.indicator.cget("text"), "Disconnected")
        self.assertEqual(self.client.indicator.cget("text_color"), "red")


if __name__ == '__main__':
    unittest.main()


"""
Referances:
Schafer, C. (2017, August 16). Python Tutorial: Unit Testing Your Code with the unittest Module. Www.youtube.com. https://www.youtube.com/watch?v=6tNS--WetLI
"""