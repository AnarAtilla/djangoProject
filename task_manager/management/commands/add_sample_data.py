from django.core.management.base import BaseCommand
from task_manager.models import Task, Category, SubTask
from django.utils import timezone

class Command(BaseCommand):
    help = 'Добавить примеры данных в модели Task и Category'

    def handle(self, *args, **kwargs):
        # Примеры категорий
        categories = [
            'Учеба',
            'Спорт',
            'Домашние дела',
        ]

        # Примеры задач
        tasks = [
            {
                'title': 'Подготовиться к экзамену',
                'description': 'Изучить главы 5-7 по истории',
                'status': 'new',
                'priority': 1,
                'deadline': timezone.now() + timezone.timedelta(days=14),
                'categories': ['Учеба'],
            },
            {
                'title': 'Пробежка утром',
                'description': 'Пробежать 5 км до восхода солнца',
                'status': 'new',
                'priority': 2,
                'deadline': timezone.now() + timezone.timedelta(days=1),
                'categories': ['Спорт'],
            },
            {
                'title': 'Убраться в комнате',
                'description': 'Пропылесосить, помыть пол и сложить вещи',
                'status': 'new',
                'priority': 3,
                'deadline': timezone.now() + timezone.timedelta(days=3),
                'categories': ['Домашние дела'],
            },
            {
                'title': 'Сделать презентацию по проекту',
                'description': 'Подготовить слайды и речь для презентации',
                'status': 'new',
                'priority': 1,
                'deadline': timezone.now() + timezone.timedelta(days=7),
                'categories': ['Учеба'],
            },
            {
                'title': 'Купить новые кроссовки',
                'description': 'Выбрать и заказать кроссовки для бега',
                'status': 'new',
                'priority': 2,
                'deadline': timezone.now() + timezone.timedelta(days=5),
                'categories': ['Спорт'],
            },
            {
                'title': 'Приготовить ужин',
                'description': 'Приготовить спагетти карбонара',
                'status': 'new',
                'priority': 3,
                'deadline': timezone.now() + timezone.timedelta(days=1),
                'categories': ['Домашние дела'],
            },
        ]

        # Создание категорий
        category_objects = {name: Category.objects.get_or_create(name=name)[0] for name in categories}

        # Создание задач
        for task_data in tasks:
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                status=task_data['status'],
                priority=task_data['priority'],
                deadline=task_data['deadline'],
            )
            for category_name in task_data['categories']:
                task.categories.add(category_objects[category_name])

        self.stdout.write(self.style.SUCCESS('Примеры данных успешно добавлены'))