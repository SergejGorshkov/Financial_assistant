from src.utils import PATH_TO_EXCEL, get_correct_dates, get_period, get_time_greating


# к excel такая дата '01.05.2018 15:00'
# "2018-05-20 15:00"
def main_info(date_time):

    start_date, end_date = get_correct_dates(date_time)
    sorted_df = get_period(PATH_TO_EXCEL, start_date, end_date)

    # 1. Приветствие
    greating = get_time_greating()
    
    return {
        "greating": greating
    }