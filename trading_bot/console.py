def num_to_print(num):
	color = "\u001b[30;43m"
	prefix = " "
	color_escape_code = "\u001b[0;0m"

	if num > 0:
		color = "\u001b[30;42m"
		prefix = "+"
	elif num < 0:
		color = "\u001b[30;41m"
		prefix = " "  # python prints the "-"

	return color + " " + (prefix + str(num)).rjust(7) + " " + color_escape_code
