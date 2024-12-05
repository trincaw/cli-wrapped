from datetime import datetime
from termcolor import colored
from time import sleep

import subprocess

# exec "fish history --show-time" and get the output
result = subprocess.run(["fish", "-c", "history --show-time"], capture_output=True, text=True)
data = result.stdout

# parse the output of this year
cutoff_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
current_year = datetime.now().year
cutoff_date = datetime.strptime(f"{current_year}-01-01", "%Y-%m-%d")

lines = data.strip().split("\n")

# Filter out lines before the cutoff date
filtered_lines = []
i = 0
while i < len(lines):
    if lines[i].startswith("#"):
        timestamp_line = lines[i].lstrip("# ").strip()
        try:
            timestamp = datetime.strptime(timestamp_line, "%a %d %b %Y %I:%M:%S %p %Z")
        except ValueError:
            print(f"Could not parse timestamp: {timestamp_line}")
            i += 1
            continue
        if timestamp >= cutoff_date:
            if i + 1 < len(lines):
                filtered_lines.append(lines[i + 1])
        i += 2
    else:
        i += 1

lines = filtered_lines
lines_count = len(lines)

commands = {}
invocations = {}

while lines:
        command_line = lines.pop(0).strip()

        # Extract base command
        try:
            base_command = command_line.split()[0]
        except IndexError:
            print(f"Could not extract base command from: {command_line}")

        # Update counts
        commands[base_command] = commands.get(base_command, 0) + 1
        invocations[command_line] = invocations.get(command_line, 0) + 1

# order the commands by count
sorted_commands = sorted(commands.items(), key=lambda x: x[1], reverse=True)
sorted_invocations = sorted(invocations.items(), key=lambda x: x[1], reverse=True)

# clear output
print("\033[H\033[J")

print(f'This year you used {colored(lines_count, "red", attrs=["bold"])} commands, of which {colored(len(commands), "red", attrs=["bold"])} were unique.')
print("Let's see what you used the most...")
sleep(3)
print("")
print("Your top commands were:")
for command, count in sorted_commands[:5]:
    sleep(1)
    print(f"{colored(command, "cyan", attrs=["bold"])}: {count}")
print("")
sleep(3)
print("Your top invocations in the last year were:")
for invocation, count in sorted_invocations[:5]:
    sleep(1)
    print(f"{colored(invocation, "green", attrs=["bold"])}: {count}")