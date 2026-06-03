from product_scheduler.core.schedule import Schedule
from product_scheduler.core.dto import ScheduleInfo
from product_scheduler.database.csv.csv_schedule_repository import CSVScheduleRepository


def main():
    csv_file_dir = "datas\\csv\\datas_sample_20260530_00"
    schedule_info: ScheduleInfo = CSVScheduleRepository(csv_file_dir).fetch_all_data()
    schedule: Schedule = Schedule.from_info(schedule_info)
    pass


if __name__ == "__main__":
    main()
