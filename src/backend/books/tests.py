from django.test import TestCase, Client
from .models import *
from api.public_test_module import *
# Create your tests here.

class ModelTest(TestCase):
    def setUp(self):
        # create_unit_word()
        create_category()
        # create_classification()
        # create_example_sentence()

    def test_edition_models(self):
        result = Edition.objects.get(id=1)
        self.assertEqual(result.create_time, '2019-08-15')

    def tearDown(selfselef):
        Category.objects.filter(id=1).delete()
        print('lmh')

    # def test_category_models(self):
    #     result = Category.objects.get(id=1)
    #     self.assertEqual(result.category, '新高中课程')

    # def test_unitInfo_models(self):
    #     result = UnitInfo.objects.get(pk=1)
    #     self.assertEqual(result.total_number, 4)

    # def test_word_models(self):
    #     result = Word.objects.get(pk=1)
    #     self.assertEqual(result.create_time, '2019-08-15',)
    #
    # def test_classification_models(self):
    #     result = Classification.objects.get(id=1)
    #     self.assertEqual(result.sequence, 1)
    #
    # def test_exampleSentence_models(self):
    #     result = ExampleSentence.objects.get(id=1)
    #     self.assertEqual(result.example_sentence_ch, '中文例句')
    #
    # def test_unitword_models(self):
    #     result = UnitWord.objects.get(pk=1)
    #     self.assertEqual(result.unit, UnitInfo.objects.get(pk=1))
    #
    # def test_get_word(self):
    #     cli = Client()
    #     res = cli.get('/books/get_word?student_id=1&category=1')
    #     self.assertEqual(res.status_code, 200)
    #     # self.assertContains(res, "hello")
    #     response_method_failed = cli.post(
    #         '/books/get_word', {})
    #     self.assertEqual(
    #         response_method_failed.content.decode('utf-8'),
    #         'get word failed')
    #
    # def test_generate_question(self):
    #     cli = Client()
    #     res = cli.get('/books/generate_question')
    #     self.assertEqual(res.status_code, 200)
    #     response_method_failed = cli.post(
    #         '/books/get_word', {})
    #     self.assertEqual(
    #         response_method_failed.content.decode('utf-8'),
    #         'generate_question failed')