import frappe
from erpnext.portal.product_configurator.utils import (get_products_for_website, get_product_settings,
	get_field_filter_data, get_attribute_filter_data)
from erpnext.shopping_cart.product_info import get_product_info_for_website

sitemap = 1

def get_shopping_cart(item_code):
        return get_product_info_for_website(item_code, skip_quotation_creation=True)

def get_context(context):

	if frappe.form_dict:
		search = frappe.form_dict.search
		field_filters = frappe.parse_json(frappe.form_dict.field_filters)
		attribute_filters = frappe.parse_json(frappe.form_dict.attribute_filters)
	else:
		search = field_filters = attribute_filters = None

	context.items = get_products_for_website(field_filters, attribute_filters, search)

	for item in context.items:
	    frappe_log_error("[kalla] item found!")
	    context['shopping_cart'] = get_product_info_for_website(item.item_code, skip_quotation_creation=True)
	    break
	
	product_settings = get_product_settings()
	context.field_filters = get_field_filter_data() \
		if product_settings.enable_field_filters else []

	context.attribute_filters = get_attribute_filter_data() \
		if product_settings.enable_attribute_filters else []

	context.product_settings = product_settings
	context.page_length = product_settings.products_per_page

	context.no_cache = 1

def add_cart_to_context(context):
        
        if locals().get('context.items') is not None:
            #frappe_log_error("[kalla] item found!")
            for item in context.items:
                context['shopping_cart'] = get_product_info_for_website(item.item_code, skip_quotation_creation=True)
                break
