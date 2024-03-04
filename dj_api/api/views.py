from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import GlassdoorQuestion
from .serializers import GlassdoorSerializer, EmptySerializer
from scrapers.glassdoor_scraper import GlassdoorScraper


class GlassdoorListView(generics.ListAPIView):
    queryset = GlassdoorQuestion.objects.all()
    serializer_class = GlassdoorSerializer


class GlassdoorCreateView(generics.CreateAPIView):
    serializer_class = EmptySerializer

    def perform_create(self, serializer):
        company = "Google"
        position = "Software Engineering Intern"
        data = GlassdoorScraper.scrape_interview_questions(company, position)

        for question_obj in data:
            GlassdoorQuestion.objects.get_or_create(
                experience=question_obj["experience"], 
                question=question_obj["question"],
                defaults={
                    "date_posted": question_obj["date_posted"], 
                }
            )

        return Response({"message": "Data successfully scraped and saved."}, status=status.HTTP_201_CREATED)
