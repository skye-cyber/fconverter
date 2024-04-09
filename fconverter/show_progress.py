import time
import progressbar


def progress_show():
    total_iterations = 100

    # Create a progress bar
    bar = progressbar.ProgressBar(maxval=total_iterations,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()

    for i in range(1, total_iterations + 1):
        time.sleep(0.01)  # Simulating work
        bar.update(i)

    bar.finish()
    # print("Progress bar animation complete!")


if __name__ == "__main__":
    progress_bar_animation()
