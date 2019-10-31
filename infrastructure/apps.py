from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
	name = 'infrastructure'

	def ready(self):
		import infrastructure.signals