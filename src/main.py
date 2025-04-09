# from pprint import pprint

from src.views import main_info

# from srs.reports import spending_by_category
# from src.services import anylize_cashback


if __name__ == "__main__":
    date_request = "2025-04-10 20:30:00"
    result_views = main_info(date_request)
    print(result_views)
    # result_repors = spending_by_category()
