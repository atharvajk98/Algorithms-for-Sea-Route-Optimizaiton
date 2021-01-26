from django.db import migrations,models

def insert_default_ports(apps,schema_editor):
	import pandas as pd
	import logging
	logger = logging.getLogger(__name__)
	NavalPort = apps.get_model("ports", "NavalPort")
	db_alias = schema_editor.connection.alias
	logger.info('Starting loading for ports.csv into NavalPort model.')
	df = pd.read_csv('./ports/migrations/ports.csv')
	df['world_port_index'] = df['world_port_index_number']
	df['main_port_name'] = df['main_port_name'].apply(lambda x: x.capitalize())
	df['lat'] = df['Latitude']
	df['lon'] = df['Longitude']
	df = df.set_index(['world_port_index_number','id','Latitude','Longitude'])
	rows = df.to_dict('records');
	logger.info('CSV parsing complete, inserting into DB.')
	batch = []
	idx = 0
	for row in rows:
		idx+=1
		batch.append(NavalPort(**row))
		if len(batch) > 100:
			NavalPort.objects.using(db_alias).bulk_create(batch)
			batch = []
			logger.info('Inserted {:5d} rows.'.format(idx))
	logger.info('Insertion complete. Inserted {:5d} rows.'.format(idx))

class Migration(migrations.Migration):

	dependencies = [
		('ports','0001_initial')
    ]
    
	operations = [
		migrations.RunPython(insert_default_ports)
	]