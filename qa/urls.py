from django.urls import path
from qa.views import main, ask_question, single_question

app_name = "qa"

urlpatterns = [
    path('popular/', main),
    path('ask/', ask_question, name="ask_question"),
    path('question/<int:number>/', single_question, name="single_question"),
]
