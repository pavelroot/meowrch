import os
import json
import psutil
import GPUtil
import argparse
import pyamdgpuinfo
import configparser
from os.path import expandvars
from dataclasses import dataclass


# ┏━━━┳━━┳━┓┏━┳━━━┳┓╋╋┏━━┳━┓┏━┓
# ┗┓┏┓┣┫┣┫┃┗┛┃┃┏━━┫┃╋╋┗┫┣┻┓┗┛┏┛
# ╋┃┃┃┃┃┃┃┏┓┏┓┃┗━━┫┃╋╋╋┃┃╋┗┓┏┛
# ╋┃┃┃┃┃┃┃┃┃┃┃┃┏━━┫┃╋┏┓┃┃╋┏┛┗┓
# ┏┛┗┛┣┫┣┫┃┃┃┃┃┃╋╋┫┗━┛┣┫┣┳┛┏┓┗┓
# ┗━━━┻━━┻┛┗┛┗┻┛╋╋┗━━━┻━━┻━┛┗━┛
# The program was created by DIMFLIX (Modified by K1rsN7)
# Github: https://github.com/DIMFLIX-OFFICIAL


@dataclass
class ValIcons:
	percent_icon: str
	percent_critical: bool
	temp_icon: str
	temp_critical: bool


def get_icon(percent_val: int, temp_val: int) -> ValIcons:
	percent_critical = False
	temp_critical = False

	if percent_val < 40:
		percent_icon = "󰾆 "
	elif percent_val < 70:
		percent_icon = "󰾅 "
	elif percent_val < 90:
		percent_icon = "󰓅 "
	else:
		percent_critical = True
		percent_icon = " "

	if temp_val < 40:
		temp_icon = " "
	elif temp_val < 70:
		temp_icon = " "
	elif temp_val < 90:
		temp_icon = " "
	else:
		temp_critical = True
		temp_icon = " "

	return ValIcons(percent_icon, percent_critical, temp_icon, temp_critical)


def get_cpu_info(label_mode: str):
	"""
	label_mode: str = utilization - Вывод загруженности в процентах
	label_mode: str = temp - Вывод температуры в градусах Цельсия
	"""

	with open("/proc/cpuinfo", "r") as cpu_info:
		lines = cpu_info.readlines()
	
	for line in lines:
		if "name" in line:
			cpu_name = line.split(":")[1].strip()
			break

	cpu_percent = int(psutil.cpu_percent(interval=1))
	# Ограничиваем максимум до 99% и форматируем как двузначное число
	cpu_percent_display = min(cpu_percent, 99)
	cpu_percent_formatted = f"{cpu_percent_display:02d}"

	try:
		cpu_temp = int(psutil.sensors_temperatures()['coretemp'][0].current)
	except:
		cpu_temp = "N/A"

	icons = get_icon(cpu_percent, 0 if cpu_temp == "N/A" else cpu_temp)
	percent_icon = icons.percent_icon
	percent_critical = icons.percent_critical
	temp_icon = icons.temp_icon
	temp_critical = icons.temp_critical

	# Формат для вертикального отображения: иконка сверху, процент снизу
	if label_mode == 'temp':
		text = f"󰍛\n{str(cpu_temp)}°C"
		tooltip = f"󰍛 Name: {cpu_name}\n{percent_icon}Utilization: {str(cpu_percent)}%\n{temp_icon}Temp: {str(cpu_temp)}°C"
		critical = temp_critical
	else:
		text = f"󰍛\n{cpu_percent_formatted}%"
		tooltip = f"󰍛 Name: {cpu_name}\n{percent_icon}Utilization: {str(cpu_percent)}%\n{temp_icon}Temp: {str(cpu_temp)}°C"
		critical = percent_critical

	return {
		'text': text,
		'tooltip': tooltip,
		'critical': critical
	}

def get_ram_info():
	svmem = psutil.virtual_memory()
	total = str(round(svmem.total / (1024.0 ** 3), 2))
	used = round(svmem.used / (1000 ** 2) / 1000, 2)
	ram_percent = int(svmem.percent)
	# Ограничиваем максимум до 99% и форматируем как двузначное число
	ram_percent_display = min(ram_percent, 99)
	ram_percent_formatted = f"{ram_percent_display:02d}"
	critical = False

	if ram_percent < 40:
		icon = "󰾆 "
	elif ram_percent < 70:
		icon = "󰾅 "
	elif ram_percent < 90:
		icon = "󰓅 "
	else:
		critical = True
		icon = " "

	# Формат для вертикального отображения: иконка сверху, процент снизу
	text = f"󰍛\n{ram_percent_formatted}%"
	tooltip = f"{icon}Percent Utilization: {ram_percent}%\n 󰍛 Utilization: {str(used)}/{total} GB"

	return {
		'text': text,
		'tooltip': tooltip,
		'critical': critical
	}

def get_gpu_info(label_mode: str):
	percent_critical = False
	temp_critical = False

	try:
		gpu = GPUtil.getGPUs()[0]
		gpu_name = gpu.name
		gpu_percent: int = int(round(gpu.load * 100))
		gpu_temp: float = round(gpu.temperature, 2)

		icons = get_icon(gpu_percent, gpu_temp)
		percent_icon = icons.percent_icon
		percent_critical = icons.percent_critical
		temp_icon = icons.temp_icon
		temp_critical = icons.temp_critical
	except:
		try:
			first_gpu = pyamdgpuinfo.get_gpu(0)
			gpu_name = "N/A"
			gpu_percent = int(first_gpu.query_load())
			gpu_temp = first_gpu.query_temperature()
			icons = get_icon(gpu_percent, gpu_temp)
			percent_icon = icons.percent_icon
			percent_critical = icons.percent_critical
			temp_icon = icons.temp_icon
			temp_critical = icons.temp_critical
		except:
			gpu_name = 'N/A'
			gpu_percent = 'N/A'
			gpu_temp = 'N/A'
			percent_icon = "󰾆 "
			temp_icon = " "

	# Ограничиваем максимум до 99% и форматируем как двузначное число
	if gpu_percent != 'N/A':
		gpu_percent_display = min(gpu_percent, 99)
		gpu_percent_formatted = f"{gpu_percent_display:02d}"
	else:
		gpu_percent_formatted = "N/A"

	# Формат для вертикального отображения: иконка сверху, процент снизу
	if label_mode == 'temp':
		text = f"󰢮\n{str(gpu_temp)}°C"
		tooltip = f"󰢮 Name: {gpu_name}\n{percent_icon}Utilization: {str(gpu_percent)}%\n{temp_icon}Temp: {str(gpu_temp)}°C"
		critical = temp_critical
	else:
		text = f"󰢮\n{gpu_percent_formatted}%"
		tooltip = f"󰢮 Name: {gpu_name}\n{percent_icon}Utilization: {str(gpu_percent)}%\n{temp_icon}Temp: {str(gpu_temp)}°C"
		critical = percent_critical

	return {
		'text': text,
		'tooltip': tooltip,
		'critical': critical
	}

def get_system_info_config(config_path: str):
	os.makedirs(os.path.dirname(config_path), exist_ok=True)
	config = configparser.ConfigParser()

	if not os.path.isfile(config_path):
		config['DEFAULT'] = {
			'cpu-label-mode': 'utilization',
			'gpu-label-mode': 'utilization'
		}

		with open(config_path, 'w') as configfile:
			config.write(configfile)

		return 'utilization', 'utilization'


	config.read(config_path)

	cpu_label_mode = config.get('DEFAULT', 'cpu-label-mode', fallback='utilization')
	gpu_label_mode = config.get('DEFAULT', 'gpu-label-mode', fallback='utilization')

	if cpu_label_mode not in ['utilization', 'temp']:
		cpu_label_mode = 'utilization'
	
	if gpu_label_mode not in ['utilization', 'temp']:
		gpu_label_mode = 'utilization'

	return cpu_label_mode, gpu_label_mode

def set_system_info_config(config_path: str, cpu_mode: str, gpu_mode: str):
	os.makedirs(os.path.dirname(config_path), exist_ok=True)
	config = configparser.ConfigParser()

	if not os.path.isfile(config_path):
		config['DEFAULT'] = {
			'cpu-label-mode': 'utilization',
			'gpu-label-mode': 'utilization'
		}
	else:
		config.read(config_path)


	if cpu_mode in ['utilization', 'temp']:
		config['DEFAULT']['cpu-label-mode'] = cpu_mode
	else:
		config['DEFAULT']['cpu-label-mode'] = 'utilization'

	if gpu_mode in ['utilization', 'temp']:
		config['DEFAULT']['gpu-label-mode'] = gpu_mode
	else:
		config['DEFAULT']['gpu-label-mode'] = 'utilization'

	with open(config_path, 'w') as configfile:
		config.write(configfile)

if __name__ == "__main__":
	config_path = os.path.expanduser("~/.cache/meowrch/system-info.ini")
	SESSION_TYPE = (lambda s: s if s != "$XDG_SESSION_TYPE" else None)(expandvars("$XDG_SESSION_TYPE"))
	cpu_label_mode, gpu_label_mode = get_system_info_config(config_path)

	parser = argparse.ArgumentParser()
	parser.add_argument("--cpu",  action="store_true")
	parser.add_argument("--ram",  action="store_true")
	parser.add_argument("--gpu",  action="store_true")
	parser.add_argument("--click",  action="store_true")
	parser.add_argument("--normal-color", default="#a6e3a1")
	parser.add_argument("--critical-color", default="#f38ba8")

	args = parser.parse_args()

	if args.cpu:
		if args.click:
			set_system_info_config(
				config_path=config_path, 
				cpu_mode='temp' if cpu_label_mode == 'utilization' else 'utilization',
				gpu_mode=gpu_label_mode
			)
		else:
			cpu = get_cpu_info(label_mode=cpu_label_mode)
			color = args.critical_color if cpu['critical'] else args.normal_color
			del cpu['critical']
			
		if SESSION_TYPE == "x11":
			print("%{F" + color + "}" + cpu['text'] + "%{F-}")
		elif SESSION_TYPE == "wayland":
			cpu["text"] = f"<span color=\"{color}\">{cpu['text']}</span>"
			print(json.dumps(cpu))
		else:
			print("N/A")
	elif args.ram:
		ram = get_ram_info()
		color = args.critical_color if ram['critical'] else args.normal_color
		del ram['critical']

		if SESSION_TYPE == "x11":
			print("%{F" + color + "}" + ram['text'] + "%{F-}")
		elif SESSION_TYPE == "wayland":
			ram["text"] = f"<span color=\"{color}\">{ram['text']}</span>"
			print(json.dumps(ram))
		else:
			print("N/A")

	elif args.gpu:
		if args.click:
			set_system_info_config(
				config_path=config_path, 
				cpu_mode=cpu_label_mode,
				gpu_mode='temp' if gpu_label_mode == 'utilization' else 'utilization'
			)
		else:
			gpu = get_gpu_info(label_mode=gpu_label_mode)
			color = args.critical_color if gpu['critical'] else args.normal_color
			del gpu['critical']

			if SESSION_TYPE == "x11":
				print("%{F" + color + "}" + gpu['text'] + "%{F-}")
			elif SESSION_TYPE == "wayland":
				gpu["text"] = f"<span color=\"{color}\">{gpu['text']}</span>"
				print(json.dumps(gpu))
			else:
				print("N/A")
	else:
		print("Enter one of the arguments:\n--cpu to get information about the processor\n--ram to get information about RAM\n--gpu to get information about the graphics card")
