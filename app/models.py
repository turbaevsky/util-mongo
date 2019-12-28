from mongoengine import Document
from flask import Markup, url_for
from flask_appbuilder.filemanager import get_file_original_name
from mongoengine import (
	DateTimeField,
	StringField,
	ReferenceField,
	ListField,
	FileField,
	ImageField,
	URLField,
	FloatField,
	IntField,
)


class Address(Document):
	name = StringField()
	fullAddress = StringField()
	started = DateTimeField()
	ended = DateTimeField()
	scan = FileField()

	def __unicode__(self):
		return '{}'.format(self.name)

	def download(self):
		return Markup(
			'<a href="'
			+ url_for("ProjectFilesModelView.download", filename=str(self.file))
			+ '">Download</a>'
		)

	def file_name(self):
		return get_file_original_name(str(self.file))

class Provider(Document):
	name = StringField()

	def __unicode__(self):
		return '{}'.format(self.name)


class Utilities(Document):
	name = StringField()
	provider = ReferenceField(Provider)

	def __unicode__(self):
		return '{} by {}'.format(self.name, self.provider)


class Payments(Document):
	p_date = DateTimeField()
	paid = FloatField()
	p_scan = FileField()
	p_comm = StringField()
	u_date = DateTimeField()
	units = IntField()
	b_date = DateTimeField()
	bill = FloatField()
	b_scan = FileField()
	b_comm = StringField()
	type = ReferenceField(Utilities)
	addr = ReferenceField(Address)

	def downloadP(self):
		return Markup(
			'<a href="'
			+ url_for("PaymentsView.mongo_download", pk=str(self.id))
			+ '">Download {0}</a>'.format(self.p_scan))

	def file_nameP(self):
		return get_file_original_name(str(self.p_scan))

	def downloadB(self):
		return Markup(
			'<a href="'
			+ url_for("PaymentsView.mongo_downloadB", pk=str(self.id))
			+ '">Download {0}</a>'.format(self.b_scan))

	def file_nameB(self):
		return get_file_original_name(str(self.b_scan))

class Currency(Document):
	code = StringField()
	rate2gbp = FloatField()
	date = DateTimeField()

	def __unicode__(self):
		return '{}'.format(self.code)


class Tariff(Document):
	tariff = FloatField()
	unit = StringField()
	coef = FloatField()
	lmt = IntField()
	correction = FloatField()
	started = DateTimeField()
	ended = DateTimeField()
	comm = StringField()
	doc = FileField()
	type = ReferenceField(Utilities)
	addr = ReferenceField(Address)
	#provider = ReferenceField(Provider)
	web = StringField()
	currency = ReferenceField(Currency)

	def download(self):
		return Markup(
			'<a href="'
			+ url_for("ProjectFilesModelView.download", filename=str(self.file))
			+ '">Download</a>'
		)

	def file_name(self):
		return get_file_original_name(str(self.file))

