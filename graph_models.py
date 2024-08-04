from django_extensions.management.commands.graph_models import Command as GraphModelsCommand

class Command(GraphModelsCommand):
    def handle(self, *args, **options):
        options['outputfile'] = 'project_visualization.png'
        super().handle(*args, **options)