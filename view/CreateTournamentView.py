from django.shortcuts import render
from django.views import View

class CreateTournamentView(View):
    def get(self, request):
        return render(request, 'create_tournament.html')

    def post(self, request):
        # Daten aus dem Formular abrufen
        date = request.POST.get('date')
        tournament_type = request.POST.get('tournament_type')
        tournament_system = request.POST.get('tournament_system')
        double_rounds = request.POST.get('double_rounds')

        # Hier kannst du den Code für die Erstellung des Turniers einfügen
        # Verwende die oben abgerufenen Daten, um das Turnier entsprechend zu erstellen

        return render(request, 'tournament_created.html')
