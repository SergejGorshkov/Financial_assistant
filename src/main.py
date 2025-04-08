from pprint import pprint

from src.views import main_info

# from srs.reports import spending_by_category
# from src.services import anylize_cashback


if __name__ == "__main__":
    date_request = "2018-05-20 15:00:00"
    result_views = main_info(date_request)
    pprint(result_views)
    # result_repors = spending_by_category()
