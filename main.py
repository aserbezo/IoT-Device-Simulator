import subprocess
from multiprocessing import Process


def run_script(script_name):
    subprocess.run(["python", script_name])


if __name__ == "__main__":
    scripts = ['first_car.py', 'second_car.py', 'third_car.py']

    processes = []
    for script in scripts:
        process = Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()