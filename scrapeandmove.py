from modules.scrapedata import get_dn_daily
from modules.filehandling import move_files
import modules.dynamicclass as dynamicclass

User = dynamicclass.create_user()

get_dn_daily(User.headless_mode)
move_files(User.day_meter)
move_files(User.night_meter)