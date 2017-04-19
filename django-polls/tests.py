from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for Question whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for Question whose pub_date is older than 1 days.
        :return: True
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently should return True for Question whose pub_date is within the last day.
        :return: 
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message must be displayed.
        :return: 
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Question with a past pub_date should displayed on the index page.
        :return: 
        """
        create_question(question_text="a past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: a past question>'])

    def test_index_view_with_a_futrue_question(self):
        """
        Question with a pub_date in the future should not be displayed on the page.
        :return: 
        """
        create_question(question_text="Question in future.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_and_a_future_question(self):
        """
        Even if both past and future question exist, only past question should displayed.
        :return: 
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_index_view_with_two_past_question(self):
        """
        The questions index must display multiple questions.
        :return: 
        """
        create_question(question_text='past question 1.', days=-30)
        create_question(question_text='past question 2.', days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: past question 2.>', '<Question: past question 1.>']
                                 )


class QuestionDetailViewTest(TestCase):
    def test_detail_view_with_a_past_question(self):
        """
        Should displayed
        :return: 
        """
        past_question = create_question(question_text="past Q", days=-3)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_detail_view_with_a_future_question(self):
        """
        Should not displayed.
        :return: 
        """
        future_question = create_question(question_text='Future Q', days=3)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)