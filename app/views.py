from flask import render_template
from flask_appbuilder import ModelView
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface
from flask_appbuilder import expose, has_access, permission_name
from flask import make_response, Response
from app import appbuilder
from .models import *
import logging

class ProviderView(ModelView):
	datamodel = MongoEngineInterface(Provider)

class UtilitiesView(ModelView):
	datamodel = MongoEngineInterface(Utilities)

class CurrencyView(ModelView):
	datamodel = MongoEngineInterface(Currency)

class PaymentsView(ModelView):
	datamodel = MongoEngineInterface(Payments)

	list_columns = [
	'addr',
	'type',
	'p_date',
	'paid',
	#'p_scan',
	'downloadP',
	'file_nameP',
	'p_comm',
	'u_date',
	'units',
	'b_date',
	'bill',
#	'b_scan',
	'downloadB',
	'file_nameB',
	'b_comm',
	]

	base_order = ('p_date','asc')

	label_columns = {'addr':'Address',
	'type':'Utility type',
	'p_date':'Date of payment',
	'paid':'Sum been paid',
	'downloadP': 'Download payment doc',
	'file_nameP': 'File of payment',
	'p_comm':'Commentary for payment',
	'u_date':'Date of reading meter',
	'units':'Meter reading',
	'b_date': 'Date receiving bill',
	'bill': 'Sum of bill received',
	'downloadB': 'Download bill file',
	'file_nameB': 'Name of bill file',
	'b_comm': 'Commentary for bill'
	}

	@expose("/mongo_download/<pk>")
	#@has_access
	def mongo_download(self, pk):
		item = self.datamodel.get(pk)
		file = item.p_scan.read()
		response = make_response(file)
		response.headers["Content-Disposition"] = "attachment; filename={0}".format(
			item.p_scan.name
		)
		return response

	@expose("/mongo_downloadB/<pk>")
	#@has_access
	def mongo_downloadB(self, pk):
		item = self.datamodel.get(pk)
		file = item.b_scan.read()
		response = make_response(file)
		response.headers["Content-Disposition"] = "attachment; filename={0}".format(
			item.b_scan.name
		)
		return response


class AddressView(ModelView):
	datamodel = MongoEngineInterface(Address)
	list_columns = [
	'name',
	'fullAddress',
	'started',
	'ended',
	'scan',
	]

class TariffView(ModelView):
	datamodel = MongoEngineInterface(Tariff)
	list_columns = [
	'tariff',
	'unit',
	'coef',
	'lmt',
	'correction',
	'started',
	'ended',
	'comm',
	'doc',
	'type',
	'addr',
	#'provider',
	'web',
	'currency',
	]


logging.debug('all models view loaded')

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


appbuilder.add_view(
	PaymentsView,
	"PaymentsView",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)


appbuilder.add_view(
	AddressView,
	"AddressView",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)


appbuilder.add_view(
	TariffView,
	"TariffView",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)

appbuilder.add_view(
	ProviderView,
	"provider",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)

appbuilder.add_view(
	UtilitiesView,
	"Utilities",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)

appbuilder.add_view(
	CurrencyView,
	"Currency",
	icon="fa-folder-open-o",
	category="Util",
	category_icon="fa-envelope",
)

#appbuilder.security_cleanup()