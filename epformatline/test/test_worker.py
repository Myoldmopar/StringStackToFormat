from unittest import TestCase

from epformatline.worker import translate


class TranslateTester(TestCase):

    def test_plain_string_literal_only(self):
        input_string = "\"hello, world\""
        expected_string = "format(\"hello, world\")"
        self.assertEqual(expected_string, translate(input_string))

    def test_two_string_literals(self):
        input_string = "\"hello\" + \", world\""
        expected_string = "format(\"hello, world\")"
        self.assertEqual(expected_string, translate(input_string))

    def test_string_literal_with_alternate_quote(self):
        input_string = " \"hello, 'world'\""
        expected_string = "format(\"hello, 'world'\")"
        self.assertEqual(expected_string, translate(input_string))

    def test_string_literal_with_escaped_quote(self):
        # note that \\\"hi\\\" represents \"hi\" in the original C++ literal
        input_string = "\"hello, \\\"world\\\"\""
        expected_string = "format(\"hello, \\\"world\\\"\")"
        self.assertEqual(expected_string, translate(input_string))

    def test_single_token(self):
        input_string = "variableName"
        expected_string = "format(\"{}\", variableName)"
        self.assertEqual(expected_string, translate(input_string))

    def test_two_tokens(self):
        input_string = "variableName + var2"
        expected_string = "format(\"{}{}\", variableName, var2)"
        self.assertEqual(expected_string, translate(input_string))

    def test_two_tokens_with_delimiter_string(self):
        input_string = "variableName + \", \" + var2"
        expected_string = "format(\"{}, {}\", variableName, var2)"
        self.assertEqual(expected_string, translate(input_string))

    def test_removing_std_string_parentheses(self):
        input_string = "variableName + \", \" + std::string(var2)"
        expected_string = "format(\"{}, {}\", variableName, var2)"
        self.assertEqual(expected_string, translate(input_string))

    def test_removing_std_string_curly(self):
        input_string = "variableName + \", \" + std::string{var2}"
        expected_string = "format(\"{}, {}\", variableName, var2)"
        self.assertEqual(expected_string, translate(input_string))

    def test_removing_complex_std_string(self):
        input_string = "variableName + \", \" + std::string(state.dataChillers.chiller(1).var2)"
        expected_string = "format(\"{}, {}\", variableName, state.dataChillers.chiller(1).var2)"
        self.assertEqual(expected_string, translate(input_string))

    def test_real_example_1(self):
        input_string = "std::string{name} + \"No Air:Duct = [\" + obj + ',' + s.duct->dd_air(DDNum).Name + \"].\" "
        expected_string = "format(\"{}No Air:Duct = [{},{}].\", name, obj, s.duct->dd_air(DDNum).Name)"
        self.assertEqual(expected_string, translate(input_string))

    def test_raw_string_literal(self):
        input_string = "\"Spec:OA=\" + this->Name + R\"(\" Method =\" IAQ\" requires CO2.)\""
        expected_string = "format(\"Spec:OA={}{}\", this->Name, R\"(\" Method =\" IAQ\" requires CO2.)\")"
        self.assertEqual(expected_string, translate(input_string))
