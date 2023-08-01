from scrape_data import get_dn_daily
from handle_files import move_files
import user_class

User = user_class.create_user()

get_dn_daily(User.headless_mode)
move_files(User.day_meter)
move_files(User.night_meter)
